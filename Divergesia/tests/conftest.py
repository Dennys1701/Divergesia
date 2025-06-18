

import os
import pytest

@pytest.fixture(autouse=True)
def set_qt_env():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    yield
