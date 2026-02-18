from dataclasses import dataclass

@dataclass
class UserNeeds:
    domain: str
    modality: str
    goal: str

    interpretability: bool
    privacy_sensitive: bool
    limited_labels: bool
    real_time: bool
