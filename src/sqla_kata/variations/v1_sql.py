import uuid

import sqlalchemy as sa

from sqla_kata import domain, sample_data


def create_tables(engine: sa.Engine) -> None:
    with engine.connect() as conn:
        conn.execute(
            sa.text(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id UUID NOT NULL,
                    name TEXT NOT NULL,
                    PRIMARY KEY (user_id)
                )
                """
            )
        )
        conn.execute(
            sa.text(
                """
                -- CREATE TABLE tools (  -- 👈🚨 problem: can only be run once
                CREATE TABLE IF NOT EXISTS tools (  -- ✅ solution
                    tool_id UUID NOT NULL,
                    name TEXT NOT NULL,
                    usage_instructions TEXT,
                    PRIMARY KEY (tool_id)
                )
                """
            )
        )
        conn.execute(
            sa.text(
                """
                CREATE TABLE IF NOT EXISTS bookings (
                    booking_id UUID NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    -- transcipt_id INTEGER NOT NULL,  -- 👈🚨 problem: spot the typo
                    tool_id INTEGER NOT NULL,  -- ✅ solution
                    user_id UUID NOT NULL,
                    PRIMARY KEY (booking_id),
                    FOREIGN KEY(tool_id) REFERENCES tools (tool_id) ON DELETE CASCADE,
                    FOREIGN KEY(user_id) REFERENCES users (user_id)
                )
                """
            )
        )
        conn.commit()


def save_bookings(
    engine: sa.Engine, bookings: domain.Bookings = sample_data.SAMPLE_BOOKINGS
) -> None:
    user_rows: dict[uuid.UUID, domain.User] = {
        uuid.uuid4(): user_name for user_name in bookings
    }
    tool_rows: dict[uuid.UUID, domain.Tool] = {
        uuid.uuid4(): tool
        for tool in set(
            booking.tool
            for user_bookings in bookings.values()
            for booking in user_bookings
        )
    }
    booking_rows: dict[uuid.UUID, tuple[domain.User, domain.Booking]] = {
        uuid.uuid4(): (user, booking)
        for user, bookings_ in bookings.items()
        for booking in bookings_
    }
    with engine.connect() as conn:
        # insert users
        conn.execute(
            sa.text(
                """
                INSERT INTO users (user_id, name)
                VALUES (:user_id, :name)
                """
            ),
            [
                {"user_id": str(user_id), "name": user_name}
                for user_id, user_name in user_rows.items()
            ],
        )
        # insert tools
        conn.execute(
            sa.text(
                """
                INSERT INTO tools (tool_id, name, usage_instructions)
                VALUES (:tool_id, :name, :usage_instructions)
                """
            ),
            [
                {
                    "tool_id": str(tool_id),
                    "name": tool.name,
                    "usage_instructions": tool.usage_instructions,
                }
                for tool_id, tool in tool_rows.items()
            ],
        )
        # insert bookings
        conn.execute(
            sa.text(
                """
                INSERT INTO bookings (booking_id, start_date, end_date, tool_id, user_id)
                VALUES (
                    :booking_id,
                    :start_date,
                    :end_date,
                    (SELECT tool_id FROM tools WHERE name = :tool_name),
                    (SELECT user_id FROM users WHERE name = :user_name)
                )
                """
            ),
            [
                {
                    "booking_id": str(booking_id),
                    "start_date": booking.start_date,
                    "end_date": booking.end_date,
                    "tool_name": booking.tool.name,
                    "user_name": user,
                }
                for booking_id, (user, booking) in booking_rows.items()
            ],
        )
        conn.commit()


def get_bookings(engine: sa.Engine) -> domain.Bookings:
    with engine.connect() as conn:
        users = {
            user_id: domain.User(name)
            for user_id, name in conn.execute(
                sa.text("SELECT user_id, name FROM users")
            )
        }

        tools = {
            tool_id: domain.Tool(
                name=domain.ToolName(name),
                usage_instructions=(
                    domain.UsageInstructions(usage_instructions)
                    if usage_instructions
                    else None
                ),
            )
            for tool_id, name, usage_instructions in conn.execute(
                sa.text("SELECT tool_id, name, usage_instructions FROM tools")
            )
        }

        # get bookings
        bookings_result = conn.execute(
            sa.text(
                """
                SELECT booking_id, start_date, end_date, tool_id, user_id
                FROM bookings
                """
            )
        )

    # build `domain.Bookings` object
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
