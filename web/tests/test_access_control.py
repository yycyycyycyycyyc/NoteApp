import base64
import os
import unittest
from unittest.mock import patch

os.environ.setdefault("JWT_SECRET", "J" * 64)
os.environ.setdefault(
    "COMMENT_ENCRYPTION_KEY", base64.urlsafe_b64encode(b"C" * 32).decode()
)
os.environ.setdefault("EXPORT_HMAC_KEY", "H" * 64)

import app as notesapp


class FakeCursor:
    def __init__(self, note):
        self.note = note

    def execute(self, _query, _parameters):
        return None

    def fetchone(self):
        return dict(self.note) if self.note is not None else None


class FakeConnection:
    def __init__(self, note):
        self.note = note

    def cursor(self):
        return FakeCursor(self.note)

    def close(self):
        return None


class NoteAccessControlTests(unittest.TestCase):
    alice_note = {
        "id": 1,
        "student_id": 6,
        "class_id": 1,
        "grade": 16.2,
        "comment": "Alice comment",
        "student": "alice",
        "class_name": "Mathematics",
    }
    bob_note = {
        "id": 3,
        "student_id": 7,
        "class_id": 1,
        "grade": 12.6,
        "comment": "Bob comment",
        "student": "bob",
        "class_name": "Mathematics",
    }

    def request_as(self, identity, note):
        with (
            patch.object(notesapp, "current_identity", return_value=identity),
            patch.object(notesapp, "get_db", return_value=FakeConnection(note)),
            patch.object(notesapp, "decrypt_comment", side_effect=lambda value: value),
        ):
            return notesapp.app.test_client().get(f"/api/notes/{note['id']}")

    def test_unauthenticated_request_is_rejected(self):
        with patch.object(notesapp, "current_identity", return_value=None):
            response = notesapp.app.test_client().get("/api/notes/1")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json(), {"error": "unauthorized"})

    def test_student_can_read_own_note(self):
        identity = {"user_id": 6, "username": "alice", "role": "student"}
        response = self.request_as(identity, self.alice_note)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["student"], "alice")

    def test_student_cannot_read_another_students_note(self):
        identity = {"user_id": 6, "username": "alice", "role": "student"}
        response = self.request_as(identity, self.bob_note)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "not found"})

    def test_teacher_can_read_any_note(self):
        identity = {"user_id": 2, "username": "prof.turing", "role": "teacher"}
        response = self.request_as(identity, self.bob_note)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["student"], "bob")

    def test_admin_can_read_any_note(self):
        identity = {"user_id": 1, "username": "admin", "role": "admin"}
        response = self.request_as(identity, self.bob_note)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["student"], "bob")


if __name__ == "__main__":
    unittest.main()
