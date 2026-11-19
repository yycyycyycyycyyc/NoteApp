# Class 10 - Stored XSS: your words run in someone else's browser

## Student

- Yuchen Ye (叶与陈) - 2023901708

## Prediction

Before testing, I predicted the comment would come back to alice's page as a **live** tag: the
template switched autoescaping off, so the server would hand `<script>` to her browser as code
and it would run with **her** session, not the teacher's.

## Proof before the fix - the comment comes back as live code

`web/templates/dashboard.html` (line 15) and `web/templates/teacher.html` (line 55) both had:

```html
<td>{% autoescape false %}{{ n.comment }}{% endautoescape %}</td>
```

Logged in as the Mathematics teacher and saved a grade comment on **note 1** (alice's):

```bash
curl -s -b teacher.jar \
     --data-urlencode "note_id=1" --data-urlencode "grade=16.2" \
     --data-urlencode "comment=<script>alert('XSS by Eve')</script>" \
     http://localhost:8080/grades
```

Then fetched alice's dashboard as alice:

| Page | What the server sent |
|---|---|
| `GET /dashboard` (alice) | `<script>alert('XSS by Eve')</script>` - **raw, unescaped** |
| `GET /teacher` (teacher) | `<script>alert('XSS by Eve')</script>` - **raw, unescaped** |

A browser receiving that page does not display the text - it **runs** it. The teacher typed
it once; it fires for every reader of that note, with the reader's own session. That is stored
XSS, flaw #10.

## Fix - put the glass back

Both templates, one line each:

```html
<!-- before: escaping switched off -->
<td>{% autoescape false %}{{ n.comment }}{% endautoescape %}</td>

<!-- after: default autoescaping, the comment is shown, never run -->
<td>{{ n.comment }}</td>
```

The fix is not a blacklist of "dangerous words" - no list can cover every payload. It is
letting the template library do what it does by default: turn `<` into `&lt;`, so every
character is displayed and none is executed.

## Verification

Actual behaviour after the fix, same input:

| Request | Actual result |
|---|---|
| Same `<script>` comment saved, then `GET /dashboard` as alice | `&lt;script&gt;alert(&#39;XSS by Eve&#39;)&lt;/script&gt;` - escaped |
| Live `<script>alert` in the page | `0` occurrences (grep) |
| Same page fetched as the teacher (`GET /teacher`) | escaped as well, `0` live tags |
| Normal comment `score < 10 on part 1 & 2, see me` | displays correctly (`score &lt; 10 on part 1 &amp; 2, see me`) |

Both reader pages are safe and ordinary text still looks right. (The lab's Troubleshooting
notes that `curl` never executes JavaScript; the presence or absence of a **raw** `<script>`
in the response is the reliable command-line proof, which is what the table records.)

### How this was run

Docker and a PostgreSQL server were not available on the machine used for the lab, so
`web/app.py` was started from this repository with a small SQLite-backed `psycopg2` shim
(binding `%s` parameters, dict rows). The templates, the comment encryption and the
request handling are the real ones from this repository; only the database server is replaced.

## The lesson

Injection on the way **in** (SQL, the shell) is about building commands from user text.
Injection on the way **out** is about handing user text to a browser as code. Same rule in
both directions: **data stays data**. If rich text is genuinely needed, do not disable escaping
- sanitise server-side with an allow-list (e.g. `bleach`) and keep only safe tags.
