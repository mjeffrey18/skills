# Encrypted files in a rebase

Detection check and marker table for step 2. A textual merge corrupts these files - over ciphertext for filter tools (git-crypt, transcrypt), over the MAC or checksum for sops, ansible-vault, age and gpg - so the only safe automatic outcome is one side wins.

## The check

Run the attribute check for all conflicted paths at once, then peek at the blob headers of the paths it did not settle. The stage blobs are the source of truth; the worktree copy may already be rewritten by a filter or rerere.

```bash
git check-attr filter diff merge -- <paths>          # any value other than "unspecified" means encrypted
git show :2:<path> | head -c 64 | od -c | head -3    # upstream side
git show :3:<path> | head -c 64 | od -c | head -3    # the user's commit's side
```

A path is plain only when every attribute is unspecified, its name does not mark it as a secret, and both headers are readable text with none of the markers below.

| Signal               | Encrypted when                                                                                                                      |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Name                 | `.enc`, `.age`, `.gpg`, `.asc`, `.pgp`, `.secret`, `.vault` extension, or under `secrets/`; or a `.sops.yaml` rule matches the path |
| Attribute            | `filter`/`diff`/`merge` set (`git-crypt`, `crypt`, `binary`, `-merge`, `-diff`)                                                     |
| git-crypt header     | `\0GITCRYPT\0`                                                                                                                      |
| transcrypt header    | `U2FsdGVk` (`Salted__` in base64)                                                                                                   |
| sops content         | `sops:` block with `mac:`; `ENC[AES256_GCM,data:...]` values; `sops_` keys in dotenv/ini                                            |
| ansible-vault header | `$ANSIBLE_VAULT;1.1;AES256` (or `1.2;AES256;label`)                                                                                 |
| age header           | `age-encryption.org/v1`                                                                                                             |
| gpg header           | `-----BEGIN PGP MESSAGE-----` or a binary packet header                                                                             |

A `.sops.yaml` match with a plaintext blob means someone committed the file unencrypted; treat it as encrypted and tell the user.
