# Font lock

**Status:** locked for architecture proofs  
**License:** SIL Open Font License 1.1  
**Source family:** Cormorant Garamond by Christian Thalmann / Cormorant
Project, distributed through Google Fonts
**Static-file source commit:** `bcf5515652e4d99eb3e42e41ed5f4285a315a175`
in [google-fonts-bower/cormorantgaramond-bower](https://github.com/google-fonts-bower/cormorantgaramond-bower)

The repository carries the exact static font files used by
`scripts/build_volume_proof.py`, together with `assets/fonts/OFL.txt`:

| File | SHA-256 |
|---|---|
| `assets/fonts/CormorantGaramond-Regular.ttf` | `7c1aace7373d5603eb520713a8d69e71e7ed75ca95965cb3872f6a74c399eff9` |
| `assets/fonts/CormorantGaramond-SemiBold.ttf` | `4fcd2d97820dac2be5f9c24d7fbd264a08f89b16a0d12fcc80541b3fbd44ee92` |
| `assets/fonts/CormorantGaramond-Italic.ttf` | `6458bdd71b7ffaa7e2bf44a3ff66d2bb49de4841958d853cfcb779c7b1ddc890` |
| `assets/fonts/OFL.txt` | `60700d351cac4650c51f3f9db318d2a420f8b45052dba2715eb5fec41f0f6956` |

The upstream family record identifies Cormorant Garamond as OFL-licensed and
records the Cormorant project source at commit
`6d210fd3550b7358ca62d6ba3e354ec1ec940813`. The license permits embedding and
redistribution with the book artifacts; the license text remains in the
repository for downstream print packaging.

Verify the lock after replacing any file:

```sh
shasum -a 256 assets/fonts/CormorantGaramond-Regular.ttf \
  assets/fonts/CormorantGaramond-SemiBold.ttf \
  assets/fonts/CormorantGaramond-Italic.ttf assets/fonts/OFL.txt
```

Static Regular, SemiBold, and Italic files are used directly by the current
ReportLab proof builder, avoiding dependence on variable-font instance support
in downstream PDF tools.
