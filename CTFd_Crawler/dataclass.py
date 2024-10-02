from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ApiResult:
    success: bool
    data: dict


@dataclass
class Challenge:
    id: int
    name: str
    category: str
    description: str
    files: Optional[List[str]] = None


@dataclass
class Important:
    name: str
    url: str
    token: str
