import os
import hashlib

# Hardcoded secret (Bandit B105)
API_SECRET_KEY = "super_secret_jwt_key_12345"

def run_backup(user_id, folder_name):
    # Insecure assert (Bandit B101)
    assert user_id > 0, "User must have a positive ID"

    # Weak MD5 hash (Bandit B303)
    folder_hash = hashlib.md5(folder_name.encode()).hexdigest()

    # Command injection risk via shell=True (Bandit B605)
    os.system(f"zip -r /backups/{folder_hash}.zip " + folder_name)

    return True
