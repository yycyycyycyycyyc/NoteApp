# Class 8 - Fix broken access control (IDOR)

## Student

- Yuchen Ye (叶与陈) - 2023901708

## Prediction

Before testing, I predicted that changing the note id would return another
student's grade because the API checked authentication but not ownership.

## Proof before the fix

Logged in as `alice`, who owns notes 1 and 2:

| Request | Result |
|---|---|
| `GET /api/notes/1` | `200`; Alice, Mathematics, grade `16.2`, comment `Late submission, but good quality.` |
| `GET /api/notes/3` | `200`; **Bob**, Mathematics, grade `12.6`, comment `Solid work, keep it up.` |

This reproduced flaw #7: an authenticated student could change the numeric id
and read another student's note.

## Fix

After fetching a note, `api_notes` now compares the note's `student_id` with
the authenticated caller's `user_id`. A student may read only an owned note.
Teachers and administrators retain access to every note because that access is
required by their roles.

The handler returns **404 Not Found** for a cross-student request. A 403 would
also block access, but 404 reveals less information because it does not confirm
that the requested note id exists.

## Verification

Actual behavior after rebuilding the application on 12 November 2026:

| Caller and request | Actual result |
|---|---|
| Unauthenticated request | `401 Unauthorized` |
| Alice requests `/api/notes/3` (Bob's note) | `404 Not Found` |
| Alice requests `/api/notes/1` (her own note) | `200 OK`; her grade remains `16.2` |
| `prof.turing` requests `/api/notes/3` | `200 OK`; Bob's grade remains visible to the teacher |
| Administrator requests `/api/notes/3` | `200 OK` in the automated authorization test |

Automated regression tests are in `web/tests/test_access_control.py`. The full
suite passed: **13 tests run, 13 passed**.

The security lesson is that authentication answers *who is calling*, while
authorization answers *whether that caller may access this specific object*.
Both checks must be enforced by the server for every object request.
