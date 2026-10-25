# Class 2 - NotesApp exploration and initial threat model

**Student:** Yuchen Ye

**Student ID:** 2023901708

This report models the original NotesApp architecture by reading and exercising the application routes. The browser talks only to Flask; Flask talks to PostgreSQL and, for the admin diagnostic, to an external ping target.

## Trust boundaries

- **TB1 - Browser / Flask:** untrusted HTTP input enters the server and responses return to users.
- **TB2 - Flask / PostgreSQL:** application queries and stored grades, comments, accounts, and roles cross the database boundary.
- **TB3 - Web container / external target and Docker host:** the ping feature crosses the network boundary; the mounted Docker socket and project directory cross into the host security boundary.

## Numbered flow list

| # | Sender -> receiver | Data |
|---:|---|---|
| 1 | Browser -> Flask | Login username and password |
| 2 | Flask -> PostgreSQL | Account lookup query |
| 3 | PostgreSQL -> Flask | Account id, username, role and password value |
| 4 | Flask -> Browser | Login result, session cookie and redirect |
| 5 | Student -> Flask | Dashboard request |
| 6 | Flask -> PostgreSQL | Student grade query |
| 7 | PostgreSQL -> Flask | Grade, class and comment rows |
| 8 | Flask -> Student | Dashboard HTML |
| 9 | Student -> Flask | Individual note API request |
| 10 | Flask -> PostgreSQL | Note-by-id query |
| 11 | PostgreSQL -> Flask | Selected note row |
| 12 | Flask -> Student | Note JSON response |
| 13 | Teacher -> Flask | Teacher page request |
| 14 | Flask -> PostgreSQL | Classes, notes and students queries |
| 15 | PostgreSQL -> Flask | Teaching data set |
| 16 | Flask -> Teacher | Teacher page HTML |
| 17 | Teacher -> Flask | Create or update grade form |
| 18 | Flask -> PostgreSQL | INSERT or UPDATE grade/comment |
| 19 | PostgreSQL -> Flask | Write completion status |
| 20 | Flask -> Teacher | Redirect after write |
| 21 | Teacher -> Flask | CSV export request |
| 22 | Flask -> PostgreSQL | Export query |
| 23 | PostgreSQL -> Flask | Export rows |
| 24 | Flask -> Teacher | Downloaded CSV |
| 25 | Admin -> Flask | User management or ping input |
| 26 | Flask -> PostgreSQL | User/class query or account change |
| 27 | Flask -> External target | ICMP ping request |
| 28 | Flask -> Admin | Admin page, database result or ping output |

The [data-flow diagram](data-flow-diagram.md), [STRIDE analysis](STRIDE.md), machine-readable [model](model.json), and rendered [PDF report](Session02-NotesApp-Model.pdf) contain the submission evidence.
