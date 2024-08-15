import uuid

import sqlalchemy as sa

from sqla_kata import domain, sample_data

metadata = sa.MetaData()

users_table = sa.Table(
    "users",
    metadata,
    sa.Column("user_id", sa.String, primary_key=True),
    sa.Column("name", sa.String, nullable=False),
)

tools_table = sa.Table(
    "tools",
    metadata,
    sa.Column("tool_id", sa.String, primary_key=True),
    sa.Column("name", sa.String, nullable=False),
    sa.Column("usage_instructions", sa.String),
)

bookings_table = sa.Table(
    "bookings",
    metadata,
    sa.Column("booking_id", sa.String, primary_key=True),
    sa.Column("start_date", sa.Date, nullable=False),
    sa.Column("end_date", sa.Date, nullable=False),
    sa.Column("tool_id", sa.String, sa.ForeignKey("tools.tool_id")),
    sa.Column("user_id", sa.String, sa.ForeignKey("users.user_id")),
)


def create_tables(engine: sa.Engine):
    with engine.connect() as conn:
        metadata.create_all(conn)


def save_bookings(
    engine: sa.Engine, bookings: domain.Bookings = sample_data.SAMPLE_BOOKINGS
) -> None:
    with engine.begin() as conn:
        conn.execute(
            sa.insert(users_table).values(
                [
                    {"user_id": str(uuid.uuid4()), "name": user_name}
                    for user_name in bookings
                ]
            )
        )
        conn.execute(
            sa.insert(tools_table).values(
                [
                    {
                        "tool_id": str(uuid.uuid4()),
                        "name": tool.name,
                        "usage_instructions": tool.usage_instructions,
                    }
                    for tool in set(
                        booking.tool
                        for user_bookings in bookings.values()
                        for booking in user_bookings
                    )
                ]
            )
        )
        conn.execute(
            sa.insert(bookings_table).values(
                [
                    {
                        "booking_id": str(uuid.uuid4()),
                        "start_date": booking.start_date,
                        "end_date": booking.end_date,
                        "tool_id": sa.select(tools_table.c.tool_id)
                        .where(tools_table.c.name == booking.tool.name)
                        .scalar_subquery(),
                        "user_id": sa.select(users_table.c.user_id)
                        .where(users_table.c.name == user)
                        .scalar_subquery(),
                    }
                    for user, bookings_ in bookings.items()
                    for booking in bookings_
                ]
            )
        )


def get_bookings(engine: sa.Engine) -> domain.Bookings:
    with engine.connect() as conn:
        users: dict[uuid.UUID, domain.User] = {
            user_id: domain.User(name)
            for user_id, name in conn.execute(
                sa.select(users_table.c.user_id, users_table.c.name)
            )
        }
        tools: dict[uuid.UUID, domain.Tool] = {
            tool_id: domain.Tool(
                name=domain.ToolName(name),
                usage_instructions=(
                    domain.UsageInstructions(usage_instructions)
                    if usage_instructions
                    else None
                ),
            )
            for tool_id, name, usage_instructions in conn.execute(
                sa.select(
                    tools_table.c.tool_id,
                    tools_table.c.name,
                    tools_table.c.usage_instructions,
                )
            )
        }
        bookings_result = conn.execute(
            sa.select(
                bookings_table.c.booking_id,
                bookings_table.c.start_date,
                bookings_table.c.end_date,
                bookings_table.c.tool_id,
                bookings_table.c.user_id,
            )
        )

    bookings_data: domain.Bookings = {}
    for _, start_date, end_date, tool_id, user_id in bookings_result:
        bookings_data.setdefault(users[user_id], []).append(
            domain.Booking(
                tool=tools[tool_id],
                start_date=domain.StartDate(start_date),
                end_date=domain.EndDate(end_date),
            )
        )

    return bookings_data
