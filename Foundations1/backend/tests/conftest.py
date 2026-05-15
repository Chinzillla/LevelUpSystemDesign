import importlib
import sys
import pytest


@pytest.fixture()
def client(tmp_path, monkeypatch):
    test_database = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_NAME", str(test_database))

    for module_name in ["app", "db", "routes.auth", "routes.health"]:
        sys.modules.pop(module_name, None)

    app_module = importlib.import_module("app")
    app_module.app.config.update(TESTING=True)

    with app_module.app.test_client() as test_client:
        yield test_client