import tempfile
import unittest
from pathlib import Path

import plate


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload
        self.text = str(payload)
        self.status_code = 200

    def json(self):
        return self._payload

    def raise_for_status(self):
        return None


class FakeSession:
    def __init__(self):
        self.calls = []

    def request(self, method, url, params=None, data=None, headers=None, timeout=None):
        call = {
            "method": method,
            "url": url,
            "params": params or {},
            "data": data or {},
            "headers": headers or {},
            "timeout": timeout,
        }
        self.calls.append(call)

        route = call["params"].get("r")
        token = call["headers"].get("x-token")
        if route == "/user/user-info":
            return FakeResponse({"data": {"user_id": 1001 if token == "token-a" else 1002}})
        if route == "/user/like":
            return FakeResponse({"msg": "liked"})
        if route == "/user-clear-plate/clear-plate":
            return FakeResponse({"msg": "checked"})
        if route == "/user-clear-plate/clear-plate-supplement":
            return FakeResponse({"msg": "supplemented"})
        return FakeResponse({"msg": "ok"})

    def close(self):
        return None


class ClearPlateTests(unittest.TestCase):
    def test_run_once_creates_token_file_without_network(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = plate.ClearPlateConfig(
                token_file=Path(tmpdir) / "tokens.txt",
                log_file=Path(tmpdir) / "plate_log.txt",
                request_delay_seconds=0,
            )
            session = FakeSession()

            self.assertEqual(plate.run_once(config, session), 0)
            self.assertTrue(config.token_file.exists())
            self.assertEqual(session.calls, [])

    def test_run_once_uses_multi_tokens_supplements_and_mutual_likes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            token_file = Path(tmpdir) / "tokens.txt"
            token_file.write_text("token-a\n# comment\ntoken-b\n", encoding="utf-8")
            config = plate.ClearPlateConfig(
                token_file=token_file,
                log_file=Path(tmpdir) / "plate_log.txt",
                group_id=42,
                longitude=118.0,
                latitude=24.0,
                supplement_days=2,
                request_delay_seconds=0,
                location_jitter=0,
            )
            session = FakeSession()

            self.assertEqual(plate.run_once(config, session), 0)
            routes = [call["params"]["r"] for call in session.calls]

            self.assertEqual(routes.count("/user/user-info"), 2)
            self.assertEqual(routes.count("/user/like"), 2)
            self.assertEqual(routes.count("/user-clear-plate/clear-plate"), 2)
            self.assertEqual(routes.count("/user-clear-plate/clear-plate-supplement"), 4)

            checkin_calls = [
                call for call in session.calls if call["params"]["r"] == "/user-clear-plate/clear-plate"
            ]
            self.assertEqual(checkin_calls[0]["data"]["group_id"], "42")
            self.assertEqual(checkin_calls[0]["data"]["location"], "24.000000,118.000000")


if __name__ == "__main__":
    unittest.main()
