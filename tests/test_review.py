import struct, unittest
from aliasrecordreview import inspect


def sample(version=2, tag=None):
    if version == 2:
        fixed = struct.pack(
            ">h28pI2shI64pII4s4shhI2s10s",
            0,
            b"SyntheticVolume",
            1,
            b"H+",
            0,
            2,
            b"PrivateTarget",
            3,
            1,
            b"????",
            b"????",
            -1,
            -1,
            0,
            b"\0" * 2,
            b"\0" * 10,
        )
    else:
        fixed = struct.pack(
            ">hQ4shIIQI14s", 0, 65536, b"H+\0\0", 0, 2, 3, 65536, 0, b"\0" * 14
        )
    extra = b""
    if tag is not None:
        t, p = tag
        extra = struct.pack(">hH", t, len(p)) + p + (b"\0" if len(p) & 1 else b"")
    raw = (
        b"\0" * 4 + b"\0" * 2 + struct.pack(">H", version) + fixed + extra + b"\xff\xff"
    )
    return raw[:4] + struct.pack(">H", len(raw)) + raw[6:]


class Tests(unittest.TestCase):
    def test_versions(self):
        for v in (2, 3):
            self.assertEqual(inspect(sample(v))["status"], "PASS")

    def test_unicode(self):
        self.assertEqual(
            inspect(sample(tag=(14, b"\0\1\0x")))["target_name_characters"], 1
        )

    def test_private(self):
        self.assertNotIn("PrivateTarget", str(inspect(sample())))

    def test_size(self):
        self.assertEqual(inspect(sample() + b"0")["status"], "FAIL")

    def test_truncated(self):
        d = sample()
        for i in range(len(d)):
            self.assertNotEqual(inspect(d[:i])["status"], "PASS")

    def test_unknown(self):
        self.assertEqual(inspect(sample(tag=(123, b"x")))["status"], "OPEN")

    def test_nested(self):
        self.assertEqual(inspect(sample(tag=(20, b"opaque")))["status"], "OPEN")

    def test_bad_unicode(self):
        self.assertEqual(inspect(sample(tag=(14, b"\0\2\0x")))["status"], "FAIL")

    def test_unsupported_version(self):
        d = bytearray(sample())
        struct.pack_into(">H", d, 6, 8)
        self.assertEqual(inspect(bytes(d))["status"], "OPEN")

    def test_upstream_writer_v2(self):
        from pathlib import Path

        d = (
            Path(__file__).resolve().parents[1] / "examples/upstream_writer_v2.bin"
        ).read_bytes()
        self.assertEqual(inspect(d)["status"], "PASS")
