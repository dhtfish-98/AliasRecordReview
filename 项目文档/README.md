> 目录已整理：文档在「项目文档」，构建、缓存与暂存输入在「Build」。从仓库根目录运行 `python3 构建.py --build`；如需使用本文原有源码命令，先运行 `python3 构建.py --stage --ci`，再进入 `Build/源码`。暂存会恢复原输入路径。现有版本和历史验证记录按各自提交理解。

# AliasRecordReview

New implementation author: **dhtfish98**. Current package version: **1.0.3**.

Highlights malformed alias declarations and network-mount indicators without resolving targets or disclosing paths. Nested aliases and unknown tags remain OPEN.

## Supported project scope

Finder Alias versions 2/3 fixed layouts and bounded aligned tags, Unicode lengths/encodings, CNID-path/high-resolution-date/home-prefix widths and explicit terminator.

This repository implements that entire selected standalone scope. It does not claim that the original upstream platform has been rewritten in full.

## Use

```sh
python -m pip install .
aliasrecordreview examples/valid.bin
```

Supply one local regular file. The file CLI requires OS `O_NOFOLLOW` and `O_NONBLOCK` support; missing safety flags return OPEN before opening the path. This file-reader contract was verified on macOS/Linux; native Windows file reading is outside the validated profile. No symlinks or automatic artifact discovery are accepted. The CLI prints JSON; exit 0 means supported checks completed, exit 1 means a structural failure, and exit 2 means unsupported/incomplete analysis. Each successful read includes the input SHA-256 and byte count. Paths, contents, report messages and identities are suppressed. The input is never modified.

## Explicit limits and boundaries

Input limit: 16 MiB. Record limit: 100,000. Additional format-specific limits are enforced in the source.

Excluded capabilities: Bookmark files, file resolution, network mounting, native OS APIs, creation/writing and recursive disk-image aliases.

PASS only describes the recorded checks. It does not prove real-world safety, historical activity, authenticity, applicant contribution or CVP approval. CVP application suitability/qualification remains OPEN until the applicant supplies the real authorized work, relevant restriction evidence and identity/organization facts.

## Provenance and validation

See [ORIGIN.md](<ORIGIN.md>), [SOURCE_MANIFEST.json](<../SOURCE_MANIFEST.json>), [VALIDATION.md](<VALIDATION.md>) and the preserved [LICENSE](<LICENSE>).
