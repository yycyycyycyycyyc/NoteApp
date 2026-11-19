# Class 11 - CSRF: requests you never meant to send

## Student

- Yuchen Ye (叶与陈) - 2023901708

## Prediction

Before testing, I predicted the server would accept the request: it only checks *is this cookie
valid?*, never *did this request come from my own form?*. A `302` and a changed grade, without
the teacher clicking anything in NotesApp.

## Proof before the fix - a valid cookie is enough

Logged in as the Mathematics teacher (`prof.turing` / `teach123`), then sent a grade change
carrying **only** the cookie - no form, no page from NotesApp - and even claiming a foreign
origin:

```bash
curl -s -b teacher.jar -H "Origin: http://evil.example" \
     -d "note_id=10&grade=20&comment=Perfect work." \
     http://localhost:8080/grades
```

| Request | Result |
|---|---|
| `POST /grades` with cookie + `Origin: http://evil.example` | `302` - **accepted, saved** |
| `GET /dashboard` as **eve** | Mathematics grade is now **`20.0`** |

Eve is a student; only teachers write grades. The server never asked where the request came
from, so any page that makes the teacher's browser send this POST changes eve's grade. For a
real attacker the request starts on her own site and lands on NotesApp - `class11/prize.html`
is that page: one hidden form, no button, submitted by a one-line script the moment it opens.

## Fix - make the app ask for proof (three pieces)

### 1. One random secret per session, and a check on every POST - `web/app.py`

```python
import secrets

app.secret_key = SECRET_KEY
# Defence in depth: the browser keeps the session cookie off most cross-site POSTs.
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


def csrf_token():
    """One random secret per session. Our own forms print it; other sites cannot read it."""
    if "csrf" not in session:
        session["csrf"] = secrets.token_urlsafe(32)
    return session["csrf"]


app.jinja_env.globals["csrf_token"] = csrf_token


@app.before_request
def check_csrf():
    """Every state-changing POST must carry the session's token."""
    if request.method == "POST" and request.endpoint != "login":
        expected = session.get("csrf")
        sent = request.form.get("csrf_token", "")
        # Fail closed: no expected token means refuse (never compare "" with "").
        if not expected or not hmac.compare_digest(sent, expected):
            abort(400, "CSRF token missing or wrong")
```

The login POST stays exempt (it is how a session - and its token - gets created).

### 2. Print the stamp in every real form

The first line inside each `<form method="post" …>`:

```html
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
```

- `web/templates/teacher.html` - 1 form (the grade form)
- `web/templates/admin.html` - 3 forms (delete, create, ping)

Why Eve's page cannot simply copy the token: to read it she would have to **read a response
from `localhost:8080`**, and the same-origin policy forbids that. She can send requests blind;
she can never read the stamp.

## Verification

| Request | Actual result |
|---|---|
| Forged `POST /grades` (cookie only, no token) | **`400`** `CSRF token missing or wrong`; eve's grade unchanged |
| Real form path: `GET /teacher` prints a token, then `POST /grades` **with** it | `302`; the grade is saved |
| Real form path: `POST /grades` **without** the token | **`400`**, no write |
| Admin *Add user* with the token | `302`, user created |
| Admin *Add user* without the token | **`400`** |
| Admin *Ping* with the token, `host=127.0.0.1` | `200`, normal ping output |
| Admin *Ping* without the token | **`400`** |
| Same stored-XSS comment from Class 10 | still escaped (`&lt;script&gt;…`), no live tag |

The existing suite still passes: **13 tests run, 13 passed**.

### How this was run

Docker and a PostgreSQL server were not available on the machine used for the lab, so
`web/app.py` was run from this repository with a small SQLite-backed `psycopg2` shim (binding
`%s` parameters, dict rows). Application code, templates, comment encryption and sessions are
the real ones from this repository; only the database server is replaced. The forged request
was sent with `curl` carrying the teacher's cookie and `Origin: http://evil.example`, which is
the same request a cross-site page produces.

## The lesson

A session cookie proves **who** the browser belongs to; it says nothing about whether that
person **meant** to send this request. Anything that changes data needs a second check -
proof of intent, a secret only the app's own pages can print. `SameSite=Lax` is a seatbelt,
not the fix: the server must not depend on the browser to protect it.
