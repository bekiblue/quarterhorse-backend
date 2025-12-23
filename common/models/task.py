from dataclasses import dataclass, field
from typing import ClassVar

from rococo.models.versioned_model import VersionedModel


@dataclass
class Task(VersionedModel):
    """
    Represents a task in the TodoMVC application.
    
    Each task belongs to a person and can be marked as completed.
    Tasks have a title completion status.
    """
    use_type_checking: ClassVar[bool] = True
    
    person_id: str = field(default=None)
    title: str = field(default="")
    description: str = field(default="")
    completed: bool = field(default=False)
