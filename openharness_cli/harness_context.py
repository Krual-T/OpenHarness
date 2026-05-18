
import contextvars
import functools
import inspect
from pathlib import Path
from typing import Optional

from .models import HarnessConfig

_current: contextvars.ContextVar[Optional[HarnessContext]] = contextvars.ContextVar(
    "harness_ctx", default=None
)


class HarnessContext:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root.resolve()
        self._config: Optional[HarnessConfig] = None

    @property
    def config(self) -> HarnessConfig:
        if self._config is None:
            self._config = HarnessConfig(repo_root=self.repo_root)
        return self._config

    @property
    def task_packages_root(self) -> Path:
        return self.config.task_packages_root

    @property
    def archived_task_packages_root(self) -> Path:
        return self.config.archived_task_packages_root

    def activate(self) -> HarnessContext:
        _current.set(self)
        return self

    @classmethod
    def current(cls) -> HarnessContext:
        ctx = _current.get()
        if ctx is None:
            raise RuntimeError("No active HarnessContext — call HarnessContext(...).activate() first")
        return ctx


def harness(func):
    """Inject HarnessContext as the first argument from the active context.

    Only injects when the first parameter is annotated as ``HarnessContext``.
    Otherwise validates that a context is active but does not modify arguments.
    """
    sig = inspect.signature(func)
    params = list(sig.parameters.values())

    if params and params[0].annotation is HarnessContext:

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(HarnessContext.current(), *args, **kwargs)

        return wrapper

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        HarnessContext.current()
        return func(*args, **kwargs)

    return wrapper
