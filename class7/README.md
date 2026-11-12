# Class 7 - Fix the NotesApp login

## Student

- Yuchen Ye (叶与陈) - 2023901708

## Prediction

**NO.** The old forged tokens will not work after the fix. A token using
`alg: none` has no valid seal, while a token signed with the old `s3cr3t`
secret cannot match the HMAC produced by the new random secret.

## Three fixes

1. **Reject `none`:** `verify_jwt` returns no identity unless the header's
   algorithm is exactly `HS256`.
2. **Pin HS256:** the server chooses HS256 and does not use a token-supplied
   algorithm to select a verification method.
3. **Use a long secret:** `create_jwt_secret.py` writes a random 256-bit value
   to the Git-ignored `.env` file. The application refuses to start if the
   value is shorter than 32 characters.

The real secret is deliberately not committed to Git.

## Test

Run:

```bash
python3 create_jwt_secret.py
docker compose build web
docker compose run --rm web python -m unittest discover -s tests -v
```

Actual security checks (run locally on 30 October 2026):

| Attempt | HTTP result |
|---|---|
| Forged token with `alg: none` | `401 Unauthorized` - rejected |
| Forged HS256 token signed with `s3cr3t` | `401 Unauthorized` - rejected |
| Token issued after a real Alice login | `200 OK` - accepted |

The full automated suite also passed: **8 tests run, 8 passed**.

This closes flaw #4 without storing the new JWT secret in the repository.
