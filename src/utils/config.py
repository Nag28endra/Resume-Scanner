import os
from typing import Any, Dict, Optional

import yaml


def load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def load_config(path: Optional[str] = None) -> Dict[str, Any]:
    path = path or os.getenv("RESUME_SCREENER_CONFIG", "configs/model.yaml")
    return load_yaml(path)
