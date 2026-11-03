# Plan: what hash functions are used for

**Status: plan only.** This file describes documents that haven't been written. It will be replaced by a topic index before this work is merged.

## What the topic will answer

The word "hash" covers functions with very different promises. A password store, a hash table, and a game world that regenerates from a seed all use one, and each needs something different from it. This topic will start from that question and give each use its own short document, with this file as the hub.

## Planned documents

| Document | Question | Figure or demo |
| --- | --- | --- |
| `what-a-hash-promises.md` | What can a hash guarantee, and which guarantees does each use need? | A table of uses against the properties each one relies on |
| `sha-256-step-by-step.md` | How does SHA-256 turn input bytes into a digest? | One short input followed through padding, the message schedule, and the rounds |
| `fast-hashes-and-hash-tables.md` | What do non-cryptographic hashes give up for speed, and why do hash tables seed them? | Keys landing in buckets, with and without deliberately chosen collisions |
| `salting-passwords.md` | Which attacks does a salt stop, and which does it leave open? | Two users with the same password, shown with and without salts |
| `hashes-in-procedural-generation.md` | How can a seed and a coordinate produce the same world every time without storing it? | A small interactive grid that changes with the seed and stays the same when revisited |
| `verifying-files-and-content-addressing.md` | How do digests detect changed files, and how does Git name objects by their contents? | A one-byte change producing a completely different digest |

Bloom filters stay in [#93](https://github.com/pomodorozhong/rabbit-holes/issues/93). The documents above will link to that work when it exists, rather than cover it here.

## Sources to start from

- [NIST's Secure Hash Standard](https://csrc.nist.gov/pubs/fips/180-4/upd1/final) for SHA-256.
- [xxHash](https://github.com/Cyan4973/xxHash) and the [SipHash paper](https://www.aumasson.jp/siphash/siphash.pdf) for fast and seeded hashing.
- [OWASP's password storage guidance](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) and [the Argon2 RFC](https://www.rfc-editor.org/rfc/rfc9106.html) for salting and deliberately slow functions.
- [Red Blob Games on terrain from noise](https://www.redblobgames.com/maps/terrain-from-noise/) as a starting point for procedural generation. Finding out how hashes feed that noise is part of the research.
- [Git's object model](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects) for content addressing.
- The references already listed in [#10](https://github.com/pomodorozhong/rabbit-holes/issues/10).

## Work left to do

1. Write the six documents in `topics/hashing/`.
2. Replace this plan with a hub that links each document and lists the questions it answers.
3. Add the topic to the root `README.md`.

## How it will be checked

- Run every example, and compare the SHA-256 walkthrough against a real digest.
- View each figure rendered, and try the interactive grid in a browser.
- Check every link and read the sources behind each claim.
- Run `git diff --check` and review the writing against the explanatory-writing skill.
