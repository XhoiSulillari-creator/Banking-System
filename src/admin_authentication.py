import json
import secrets
import time


class AdminAuthenticationService:
    def __init__(self, mailbox_file):
        self.mailbox_file = mailbox_file
        self.otp_lifetime = 300

    def request_otp(self, admin_id):
        otp = str(secrets.randbelow(900000) + 100000)

        data = {
            "admin_id": admin_id,
            "otp": otp,
            "created_at": time.time(),
            "used": False
        }

        with open(self.mailbox_file, "w") as file:
            json.dump(data, file, indent=4)

        return otp

    def authenticate(self, admin_id, otp):
        try:
            with open(self.mailbox_file, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return False

        if data["admin_id"] != admin_id:
            return False

        if data["used"]:
            return False

        if time.time() - data["created_at"] > self.otp_lifetime:
            return False

        if data["otp"] != otp:
            return False

        data["used"] = True

        with open(self.mailbox_file, "w") as file:
            json.dump(data, file, indent=4)

        return True