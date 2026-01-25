import sys
import os
import pytest

# === find source directory dynamically ===
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

SRC_PATH = None
for root, dirs, files in os.walk(PROJECT_ROOT):
    if "controllers.py" in files:
        SRC_PATH = root
        break

if SRC_PATH is None:
    raise RuntimeError("Cannot find controllers.py in project")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

import database
import controllers
from controllers import LibraryController


@pytest.fixture(autouse=True)
def isolate_json(monkeypatch):
    fake_data = {
        "users": [],
        "books": [],
        "loans": []
    }

    # 1. Chặn database layer
    monkeypatch.setattr(database, "load_data", lambda: fake_data)
    monkeypatch.setattr(database, "save_data", lambda data: None)

    # 2. Chặn controller layer (QUAN TRỌNG)
    monkeypatch.setattr(controllers, "load_data", lambda: fake_data)
    monkeypatch.setattr(controllers, "save_data", lambda data: None)

    # 3. Reset data cache nếu có
    monkeypatch.setattr(LibraryController, "data", fake_data, raising=False)
