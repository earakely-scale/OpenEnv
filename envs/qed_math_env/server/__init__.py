# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""QED Math Environment server components."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .qed_math_environment import QEDMathEnvironment

__all__ = ["QEDMathEnvironment"]


def __getattr__(name: str):
    """Import the environment only when requested, not in verifier workers."""
    if name == "QEDMathEnvironment":
        from .qed_math_environment import QEDMathEnvironment

        globals()[name] = QEDMathEnvironment
        return QEDMathEnvironment
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
