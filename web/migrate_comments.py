"""Idempotently encrypt every legacy plaintext comment in NotesApp."""
from app import get_db
from comment_crypto import encrypt_comment, PREFIX


def main():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, comment FROM notes WHERE comment IS NOT NULL")
    changed = 0
    for row in cur.fetchall():
        if not row["comment"].startswith(PREFIX):
            cur.execute("UPDATE notes SET comment = %s WHERE id = %s", (encrypt_comment(row["comment"]), row["id"]))
            changed += 1
    conn.close()
    print(f"encrypted {changed} legacy comments")


if __name__ == "__main__":
    main()
