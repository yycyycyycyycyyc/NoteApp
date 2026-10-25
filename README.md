# NotesApp

## Student

Yuchen Ye

A small grades application used throughout the Computer Security course. Teachers
record grades and comments for their classes, students read their own grades, and an
admin manages users and classes.

## Run it

You need Docker with the Compose plugin.

```
git clone https://github.com/yycyycyycyycyyc/NoteApp.git notesapp
cd notesapp
python3 create_comment_key.py
python3 create_export_key.py
docker compose up
```

The first start builds the image, launches PostgreSQL, and loads the seed data
automatically. Startup also migrates any legacy plaintext comments to AES-GCM ciphertext. The two generated keys remain in the Git-ignored `.env` file. When it is ready, open:

```
http://localhost:8080
```

## Test accounts

| Role    | Username      | Password   |
|---------|---------------|------------|
| Student | `alice`       | `alicepw`  |
| Teacher | `prof.turing` | `teach123` |
| Admin   | `admin`       | `admin123` |

(There are ~30 students in total; each student's password is their username + `pw`,
e.g. `bob` / `bobpw`.)

## Stack

- Python 3.11 + Flask (server-rendered Jinja2 pages and a small JSON API)
- PostgreSQL 15
- Docker Compose (`web` and `db` services)

## Coursework

- [Class 2 exploration and initial threat model](class2/README.md)
- [Class 3 symmetric encryption lab](class3/README.md)
- [Project 1 threat model](project1/README.md)
- [C3 encrypted grade comments](comment-encryption.md)
- [C4 HMAC-protected CSV exports](hmac-export.md)
- [C5a HTTPS traffic audit](class5/README.md)
- [C5b password storage audit](class5/password-audit.md)

## Reset

```
docker compose down -v   # wipes the database volume
docker compose up        # reloads the seed data
```

## Updating your fork

The course repository is sometimes updated. Your fork does **not** update by itself.
To pull the latest changes into your fork:

**Easiest (GitHub website):** open your fork, and if it says *"This branch is behind
KristenPire/NoteApp"*, click **Sync fork → Update branch**. Then, in your local clone:

```
git pull
```

**Command line (keeps your own commits):**

```
git remote add upstream https://github.com/KristenPire/NoteApp.git   # once
git fetch upstream
git merge upstream/main
git push
```

Then **rebuild**, because the app code is baked into the Docker image:

```
docker compose up --build
```

A plain `docker compose up` would keep running the old image.
