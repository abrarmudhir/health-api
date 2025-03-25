from enum import Enum


class Sex(str, Enum):
    male = "male"
    female = "female"


class MedicationForm(str, Enum):
    powder = "powder"
    tablet = "tablet"
    capsule = "capsule"
    syrup = "syrup"


class RequestStatus(str, Enum):
    active = "active"
    on_hold = "on-hold"
    cancelled = "cancelled"
    completed = "completed"
