from __future__ import annotations

import logging


def get_logger() -> logging.Logger:
    return logging.getLogger("openharness.rwp")
