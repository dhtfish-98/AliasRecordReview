# New implementation author: dhtfish98.
import argparse
import hashlib
import json
import os
import stat
import struct

MAX_BYTES = 16 * 1024 * 1024
MAX_RECORDS = 100000


class Invalid(ValueError):
    pass


class Unsupported(ValueError):
    pass


def require(ok, code):
    if not ok:
        raise Invalid(code)


def unpack(fmt, data, offset=0):
    require(
        offset >= 0 and offset + struct.calcsize(fmt) <= len(data), "truncated_field"
    )
    return struct.unpack_from(fmt, data, offset)


def text(data, encoding="utf-8"):
    try:
        return data.decode(encoding)
    except UnicodeError:
        raise Invalid("invalid_text_encoding") from None


def inspect(data):
    if not isinstance(data, bytes):
        raise TypeError("input must be bytes")
    digest = hashlib.sha256(data).hexdigest()
    try:
        require(len(data) <= MAX_BYTES, "input_limit")
        result = analyze(data)
        result.setdefault("status", "PASS")
        result.setdefault("complete", result["status"] == "PASS")
        result.setdefault("findings", [])
    except Unsupported as exc:
        result = {"status": "OPEN", "complete": False, "findings": [str(exc)]}
    except Invalid as exc:
        result = {"status": "FAIL", "complete": False, "findings": [str(exc)]}
    result.update(
        {
            "input_sha256": digest,
            "input_bytes": len(data),
            "claim": "Recorded format checks only; no authenticity, runtime or CVP approval conclusion.",
        }
    )
    return result


def read_local(path):
    nofollow = getattr(os, "O_NOFOLLOW", None)
    nonblock = getattr(os, "O_NONBLOCK", None)
    if not isinstance(nofollow, int) or not nofollow or not isinstance(nonblock, int) or not nonblock:
        raise Unsupported("safe_local_read_flags_unavailable")
    fd = os.open(path, os.O_RDONLY | nofollow | nonblock)
    try:
        info = os.fstat(fd)
        require(stat.S_ISREG(info.st_mode), "regular_file_required")
        require(info.st_size <= MAX_BYTES, "input_limit")
        with os.fdopen(fd, "rb", closefd=False) as stream:
            data = stream.read(MAX_BYTES + 1)
        require(len(data) <= MAX_BYTES, "input_limit")
        after = os.fstat(fd)
        require(
            (info.st_size, info.st_mtime_ns, info.st_ino)
            == (after.st_size, after.st_mtime_ns, after.st_ino),
            "input_changed_during_read",
        )
        return data
    finally:
        os.close(fd)


def main():
    parser = argparse.ArgumentParser(
        description="Read an explicitly supplied local evidence file and print a private-safe JSON report."
    )
    parser.add_argument("input")
    args = parser.parse_args()
    try:
        report = inspect(read_local(args.input))
    except Unsupported as exc:
        report = {"status": "OPEN", "complete": False, "findings": [str(exc)]}
    except (OSError, Invalid):
        report = {
            "status": "FAIL",
            "complete": False,
            "findings": ["input_read_failed"],
        }
    print(json.dumps(report, sort_keys=True, ensure_ascii=True))
    return {"PASS": 0, "FAIL": 1, "OPEN": 2}[report["status"]]


def analyze(data):
    app, size, version = unpack(">4sHH", data)
    if version not in (2, 3):
        raise Unsupported("unsupported_alias_version")
    require(size == len(data), "alias_size_mismatch")
    fixed = 150 if version == 2 else 58
    require(size >= fixed + 2, "alias_header_length")
    if version == 2:
        values = unpack(">h28pI2shI64pII4s4shhI2s10s", data, 8)
        (
            kind,
            vol,
            created,
            fs,
            disk,
            parent,
            name,
            cnid,
            target_created,
            creator,
            code,
            up,
            down,
            attrs,
            fsid,
            reserved,
        ) = values
        require(data[10] <= 27 and data[50] <= 63, "pascal_string_length")
        volume_length = len(vol)
        name_length = len(name)
    else:
        kind, created, fs, disk, parent, cnid, target_created, attrs, reserved = unpack(
            ">hQ4shIIQI14s", data, 8
        )
        volume_length = name_length = 0
    require(kind in (0, 1) and 0 <= disk <= 5, "invalid_alias_kind_or_disk_type")
    offset = fixed
    tags = []
    seen = set()
    unknown = False
    recursive = False
    terminated = False
    while offset < len(data):
        require(len(tags) < MAX_RECORDS, "tag_limit")
        (tag,) = unpack(">h", data, offset)
        offset += 2
        if tag == -1:
            require(
                offset == len(data)
                or (offset + 2 == len(data) and data[offset:] == b"\0\0"),
                "data_after_alias_terminator",
            )
            terminated = True
            break
        require(tag >= 0, "invalid_alias_tag")
        (length,) = unpack(">H", data, offset)
        offset += 2
        require(offset + length + (length & 1) <= len(data), "alias_tag_bounds")
        require(tag not in seen, "duplicate_alias_tag")
        seen.add(tag)
        payload = data[offset : offset + length]
        tag_offset = offset - 4
        offset += length + (length & 1)
        if length & 1:
            require(data[offset - 1] == 0, "nonzero_tag_padding")
        if tag in (14, 15):
            (chars,) = unpack(">H", payload)
            require(length == 2 + chars * 2, "unicode_tag_length")
            value = text(payload[2:], "utf-16-be")
            require("\0" not in value, "unicode_tag_null")
            if tag == 14:
                name_length = len(value)
            else:
                volume_length = len(value)
        elif tag == 1:
            require(length % 4 == 0, "cnid_path_length")
        elif tag in (16, 17):
            require(length == 8, "highres_date_length")
        elif tag == 21:
            require(length == 2, "home_prefix_length")
        elif tag in (18, 19, 0):
            value = text(payload)
            require("\0" not in value, "path_tag_null")
        elif tag == 20:
            recursive = True
        elif tag not in (2, 3, 4, 5, 6, 9, 10):
            unknown = True
        tags.append({"tag": tag, "offset": tag_offset, "bytes": length})
    require(terminated, "missing_alias_terminator")
    partial = unknown or recursive
    findings = []
    if unknown:
        findings.append("unknown_tag_semantics")
    if recursive:
        findings.append("nested_alias_not_followed")
    return {
        "version": version,
        "target_kind": kind,
        "disk_type": disk,
        "network_mount_declared": disk == 1 or bool(seen & {3, 4, 5, 9, 10}),
        "target_name_characters": name_length,
        "volume_name_characters": volume_length,
        "tags": tags,
        "status": "OPEN" if partial else "PASS",
        "complete": not partial,
        "findings": findings,
        "scope": "Alias v2/v3 fixed fields and tag envelopes; no resolution, mounting, bookmark parsing or private path disclosure.",
    }
