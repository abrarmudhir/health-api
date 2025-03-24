import enum


class SexEnum(enum.Enum):
    male = "male"
    female = "female"


class MedicationFormEnum(enum.Enum):
    powder = "powder"
    tablet = "tablet"
    capsule = "capsule"
    syrup = "syrup"


class RequestStatusEnum(enum.Enum):
    active = "active"
    on_hold = "on-hold"
    cancelled = "cancelled"
    completed = "completed"
