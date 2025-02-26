"""Vendorized dependencies.

Color has been moved from pydantic to pydantic-extra-types.  However, we can't easily
require pydantic-extra-types because it pins pydantic to >2.0.0.  So, in order to
retain compatibility with pydantic 1.x and 2.x without getting the color warning, and
without accidentally pinning pydantic, we vendor the two Color classes here.
"""

import pydantic.version

if pydantic.version.VERSION.startswith("2"):
    from ._pydantic_color_v2 import Color  # noqa
else:
    from ._pydantic_color_v1 import Color  # type: ignore # noqa

__all__ = ["Color"]
