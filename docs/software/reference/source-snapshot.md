---
title: "Source snapshot and provenance"
status: needs-review
owner_team: software-team
primary_contact: null
last_reviewed: null
review_cycle: 12 months
safety_level: informational
tags: [software, controls]
---

# Source snapshot and provenance

This documentation was prepared from the user-supplied archives and example on 2026-09-29. The supplied `aimdl-documentation.zip` is the documentation baseline. GitHub access was blocked by organization SAML enforcement, so no remote commit SHA or claim of matching current GitHub HEAD is made.

## Input archive fingerprints

| Input | SHA-256 |
| --- | --- |
| `maxima.zip` | `4960ae8d03e00abba045e489c25f98c45ce4c777c0373f751b90f06bd9ceb32e` |
| `aimdas.zip` | `5f1e32656596f439d9de468a86cc3e3f72171be3e995f54b317b01eebdcf07ec` |
| `helix.zip` | `e5ef03d773e462feeedba360278c450194cac49285f1a1fbd2f6ab249866bf72` |
| `sphinx.zip` | `750d5eb10faa67bfc91dda3eaa6c773b28aa7c34bf479ef7e51c6562c0b7c0cd` |
| `aimdds.zip` | `6a8ba51dc9ba24396939fe0e11ad7e214033606248a78ccc93a59cd8fcace162` |
| `aimdrc.zip` | `6a5f98260b94137c94878b13ba1a7d9ee87ed39efc82d3f6c8c1b48526be7553` |
| `coord.zip` | `2423fde3765e3be359a10025565069dbc9fc027038092766242207a17588f0d4` |
| `aimdrm.zip` | `c92696060888a75c5cd2c538dbf231caaf66e1c910be57d007cad73e013e67ae` |
| `errors.pdf` | `1d352c53e6b5a1a9218dbf93ca15e02840714e8ed80ff3d10ea8ebcd2551f197` |
| `SMHM.json` | `5353acee300d8008a4b4eab46d9b6dad81285d2f6851bfa4005f036b5f9ee2fd` |
| `aimdl-documentation.zip` | `6b2f0883d48a9e64c82d62b0e27f9000cfd52dcd1963290403c3d2a78d0a763c` |

## Source precedence

Implementation files take precedence for behavior. README files supply deployment examples; conflicting or incomplete README claims are called out in [source review notes](source-review.md). AIMDDS's central registry supplies canonical error metadata. The supplied PDF was checked for its code set; it contains the same 170 codes. The full [SMHM example](../examples/smhm.json) is preserved byte-for-byte.

No device connections, production database writes or operational runs were performed. Vendor API/SDK mappings describe calls made by the supplied adapters rather than an independent vendor-specification guarantee.

## Coverage boundaries

Included: AIMDAS, AIMDDS, AIMDRM, AIMDRC, MAXIMA, HELIX, SPHINX, COORD, the error PDF and SMHM run script. Not supplied: the database service repository, robotics PLC program, deployed vendor configuration, profilometer/engraver controllers, and complete native installation media/procedures for every instrument. Existing instrument documentation remains linked for those operational boundaries.
