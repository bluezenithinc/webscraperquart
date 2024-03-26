from typing import Literal, TypeAlias
from quart import Quart


Mode = Literal["dev", "test", "prod"]
App: TypeAlias = Quart
