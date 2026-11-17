# Class 9 - Injection: your words become commands, then take the power away

## Student

- Yuchen Ye (叶与陈) - 2023901708

## Prediction

Before testing, I predicted the login would accept `admin' -- ` (the quote closes the
username literal, `--` comments out the rest of the sentence) and hand me the admin
session without a password. For the ping box I predicted that `;` would end the ping
command and let me run anything I typed after it.

## Proof before the fix - SQL injection in `login()`

`web/app.py` built the query by gluing the username into it:

```python
query = (
    "SELECT id, username, role, password FROM users "
    "WHERE username = '" + username + "'"
)
cur.execute(query)
```

### The lab payload no longer works in *this* app - and why

`admin' -- ` with password `anything`:

| Request | Result |
|---|---|
| `POST /login` username `admin' -- ` | `200`; `Invalid credentials` |
| `GET /admin` with that cookie | `302` redirect to `/login` |

The quote *does* cut the literal and the row for `admin` comes back, but Class 5 moved
the password check out of SQL into Python (`ph.verify(stored, password)` over Argon2).
The injection now bypasses the **lookup**, not the **verification** - so the session is
still refused. This is a useful side effect of that fix, but not a fix for flaw #8: the
injection is still there and only needs one more SELECT column.

### The bypass that does work

`UNION` lets me append my own row, and because the row I return carries a `password`
value I chose, the Argon2 branch is never taken and the fallback
`hmac.compare_digest(stored, password)` compares my string with itself.

| Request | Result |
|---|---|
| `POST /login` username `x' UNION SELECT 1,'admin','admin','p' -- `, password `p` | `302` to `/` |
| `GET /admin` with that cookie | `200`; **admin console** (user list, class list) |

The SQL the database actually ran was:

```sql
SELECT id, username, role, password FROM users WHERE username = 'x'
UNION SELECT 1,'admin','admin','p' -- '
```

I am `user_id=1`, `role=admin`: password free, no account needed.

## Fix - stop gluing (flaw #8)

```python
# after: the username is bound, never parsed
query = "SELECT id, username, role, password FROM users WHERE username = %s"
cur.execute(query, (username,))
```

`%s` is a placeholder for the driver, not string formatting: the value is sent in a
separate envelope marked *"this is data"*. The same input is now just a username
nobody has.

## Proof before the fix - command injection in `admin_ping()`

```python
cmd = "ping -c 1 " + host
subprocess.run(cmd, shell=True, ...)
```

Logged in as the real admin, `host = 127.0.0.1; id; head -2 /etc/passwd`:

```
PING 127.0.0.1 ... 1 packets transmitted, 1 received, 0% packet loss
uid=1234(user) gid=1234(user) groups=1234(user)
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
```

The ping box was meant to ping a host; `;` let me run two more commands and read a
file. On this machine the app runs as a normal user (`uid=1234`); inside the class
container (root, see flaw #13) the same request returns `uid=0(root)`.

## Fix - no shell, one argument (flaw #9)

```python
# after: host is a single argument, from start to finish
if not re.fullmatch(r"[A-Za-z0-9.-]+", host):
    return render_template(..., ping_result=f"invalid host: {host!r}")
result = subprocess.run(
    ["ping", "-c", "1", host],
    capture_output=True, text=True, timeout=10,
)
```

Without `shell=True` there is no shell left to read `;`: the whole string is one
argument. The host allow-list is a second wall (defence in depth), not the barrier -
the argument list alone closes the hole.

## Verification

Actual behaviour after the fix, same inputs:

| Request | Actual result |
|---|---|
| `POST /login` `x' UNION SELECT 1,'admin','admin','p' -- ` / `p` | `200`; `Invalid credentials` |
| `GET /admin` with that cookie | `302` redirect; no admin console |
| `POST /login` `admin' -- ` / `anything` | `200`; `Invalid credentials` |
| `POST /admin/ping` `127.0.0.1; id; head -2 /etc/passwd` | `200`; `invalid host: '127.0.0.1; id; ...'`, no `id` output, no file |
| `POST /login` `admin` / `admin123` | `302`; admin console `200` |
| `POST /login` `alice` / `alicepw` | `302`; her dashboard with her grades |
| `POST /admin/ping` `127.0.0.1` | `200`; normal ping statistics |

Both real features still work; only the injected input became inert.

### How this was run

Docker and a PostgreSQL server were not available on the machine used for the lab, so
the app was started from this repository with a small SQLite-backed `psycopg2` shim
(`connect()` + `%s` binding + dict rows). The application code, templates, Argon2
password handling and the shell behaviour are the real ones from this repository; the
shim only replaces the database server. The `shell=True` command execution is real, so
the `uid`/`/etc/passwd` output above comes from the actual patched process.

## The lesson

SQL and the shell are two languages with one bug: user text glued into a command
string, so an interpreter reads it as grammar instead of as an answer. The fix is
always the same shape - pass data as data, in its own envelope: a placeholder and a
value tuple for the database, an argument vector for the process. The same bug waits
in file paths, template engines, LDAP and stored XSS.
