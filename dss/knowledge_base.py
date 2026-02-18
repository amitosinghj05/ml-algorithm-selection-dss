from dataclasses import dataclass
from typing import List, Dict, Any
import yaml


@dataclass
class Family:
    name: str
    examples: List[str]
    modalities: List[str]
    domains: List[str]
    tags: List[str]
    notes: List[str]


def load_kb(yaml_path: str) -> Dict[str, Any]:
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_families(yaml_path: str) -> List[Family]:
    kb = load_kb(yaml_path)
    families = []
    for item in kb.get("families", []):
        families.append(
            Family(
                name=item["name"],
                examples=item.get("examples", []),
                modalities=item.get("modalities", []),
                domains=item.get("domains", []),
                tags=item.get("tags", []),
                notes=item.get("notes", []),
            )
        )
    return families
