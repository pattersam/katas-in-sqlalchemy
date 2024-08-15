"""
Plain python _domain_ entities.
"""

import dataclasses
import datetime
import typing as t

User = t.NewType("User", str)
ToolName = t.NewType("ToolName", str)
UsageInstructions = t.NewType("UsageInstructions", str)
StartDate = t.NewType("StartDate", datetime.date)
EndDate = t.NewType("EndDate", datetime.date)


@dataclasses.dataclass(frozen=True, slots=True)
class Tool:
    name: ToolName
    usage_instructions: UsageInstructions | None = None


@dataclasses.dataclass(frozen=True, slots=True)
class Booking:
    tool: Tool
    start_date: StartDate
    end_date: EndDate

    def __repr__(self) -> str:
        return f"{self.tool.name} booked from {self.start_date} till {self.end_date}"

Bookings = dict[User, list[Booking]]  # deliberately modelled weirdly
