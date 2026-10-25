# NotesApp Password Audit

**Name:** Yuchen Ye  
**Student ID:** 2023901708  
**Date:** 25 October 2026

## Finding 1 - stored passwords (unsalted MD5)

- **Cracked:** 4/6 accounts in **0.164 ms** with the teacher-provided public wordlist.
- **Why those fell:** Their passwords were common wordlist entries, and MD5 makes guesses extremely cheap.
- **Held out:** `mariepw` was absent from the wordlist; the long random password had neither a dictionary entry nor a simple guess in this test.
- **Severity:** High, because a stolen unsalted MD5 table exposes common passwords almost immediately.
- **Fix:** Store unique, salted, deliberately expensive Argon2id hashes and encourage strong passwords.

## Finding 2 - the fix, measured

| Hash | Guesses / second | Guesses / day |
|---|---:|---:|
| MD5 | 2,504,475 | 216,386,640,000 |
| Argon2id | 24.84 | 2,146,176 |

Argon2id was approximately **100,808 times slower per guess** on this machine. With a stolen database, an attacker can test enormous MD5 dictionaries cheaply, while Argon2id makes every guess consume meaningful CPU and memory; weak passwords still matter, but the attack becomes far more expensive.

## Final state

Alice's first normal login upgraded `alicepw` to a value beginning with `$argon2id`. A second login succeeded through Argon2 verification. Other legacy accounts migrate on their next successful login, requiring no downtime.

The reproducible cracking scripts and the public wordlist are in `class5/crack/`.
