import uuid

import sqlalchemy as sa
from sqlalchemy import orm

from sqla_kata import domain, sample_data


class Base(orm.DeclarativeBase):
    """Base class for all ORM models.

    https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#establishing-a-declarative-base
    """

    type_annotation_map = {
        domain.User: sa.String,
        domain.ToolName: sa.String,
        domain.UsageInstructions: sa.String,
        domain.StartDate: sa.Date,
        domain.EndDate: sa.Date,
    }


class User(Base):
    __tablename__ = "users"
    user_id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    name: orm.Mapped[domain.User] = orm.mapped_column(unique=True)
    bookings: orm.Mapped[list["Booking"]] = orm.relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Tool(Base):
    __tablename__ = "tools"
    tool_id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    name: orm.Mapped[domain.ToolName] = orm.mapped_column(unique=True)
    usage_instructions: orm.Mapped[domain.UsageInstructions | None]
    bookings: orm.Mapped[list["Booking"]] = orm.relationship(
        back_populates="tool", cascade="all, delete-orphan"
    )


class Booking(Base):
    __tablename__ = "bookings"

    booking_id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    start_date: orm.Mapped[domain.StartDate]
    end_date: orm.Mapped[domain.StartDate]

    tool_id: orm.Mapped[sa.UUID] = orm.mapped_column(sa.ForeignKey("tools.tool_id"))
    tool: orm.Mapped[Tool] = orm.relationship(back_populates="bookings")

    user_id: orm.Mapped[sa.UUID] = orm.mapped_column(sa.ForeignKey("users.user_id"))
    user: orm.Mapped[User] = orm.relationship(back_populates="bookings", cascade="all")


def create_tables(engine: sa.Engine) -> None:
    Base.metadata.create_all(engine)


def get_or_add[T](session: orm.Session, orm_model: type[T], **kwargs) -> T:
    """
    Looks for an existing `orm_model` in the session, otherwise instantiates
    it and adds it to the session.

    This is just a experiment for learning & convenience purposes.

    It's not expected to be useful in production code, especially because of
    how it uses `kwargs` as both filter & instantiation arguments.
    """
    instance = session.query(orm_model).filter_by(**kwargs).one_or_none()
    if instance is not None:
        return instance
    new_instance = orm_model(**kwargs)
    session.add(new_instance)
    return new_instance


def save_bookings(
    engine: sa.Engine, bookings: domain.Bookings = sample_data.SAMPLE_BOOKINGS
) -> None:
    with orm.Session(engine) as session:
        session.add_all(
            Booking(
                start_date=booking.start_date,
                end_date=booking.end_date,
                user=get_or_add(session, User, name=user),
                tool=get_or_add(
                    session,
                    Tool,
                    name=booking.tool.name,
                    usage_instructions=booking.tool.usage_instructions,
                ),
            )
            for user, bookings_ in bookings.items()
            for booking in bookings_
        )
        session.commit()


def get_bookings(engine: sa.Engine) -> domain.Bookings:
    with orm.Session(engine) as session:
        return {
            user.name: [
                domain.Booking(
                    domain.Tool(booking.tool.name, booking.tool.usage_instructions),
                    domain.StartDate(booking.start_date),
                    domain.EndDate(booking.end_date),
                )
                for booking in user.bookings
            ]
            for user in session.query(User)
        }
