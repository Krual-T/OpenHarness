from __future__ import annotations

import sys
from pathlib import Path

TESTS_ROOT = Path(__file__).resolve().parent
if str(TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(TESTS_ROOT))

from openharness_cases.test_cli_workflows import *
from openharness_cases.test_entrypoint import *
from openharness_cases.test_protocol_docs import *
from openharness_cases.test_task_package_core import *
