import datetime

from sqla_kata import domain

HAMMER = domain.Tool(domain.ToolName("Hammer"), domain.UsageInstructions("bang"))
WRENCH = domain.Tool(domain.ToolName("Wrench"))

SAMPLE_BOOKINGS: domain.Bookings = {
    domain.User("Alice"): [
        domain.Booking(
            tool=WRENCH,
            start_date=domain.StartDate(datetime.date(1970, 1, 1)),
            end_date=domain.EndDate(datetime.date(1970, 1, 2)),
        ),
        domain.Booking(
            tool=HAMMER,
            start_date=domain.StartDate(datetime.date(1980, 1, 1)),
            end_date=domain.EndDate(datetime.date(1980, 5, 8)),
        ),
    ],
    domain.User("Bob"): [
        domain.Booking(
            tool=HAMMER,
            start_date=domain.StartDate(datetime.date(1990, 1, 1)),
            end_date=domain.EndDate(datetime.date(1995, 1, 1)),
        ),
        domain.Booking(
            tool=HAMMER,
            start_date=domain.StartDate(datetime.date(2000, 1, 1)),
            end_date=domain.EndDate(datetime.date(2020, 1, 1)),
        ),
    ],
}
