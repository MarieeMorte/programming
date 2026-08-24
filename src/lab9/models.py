"""Определение моделей SQLAlchemy для системы бронирования книг."""
# pylint: disable=too-few-public-methods

from datetime import date

from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):  # type: ignore
    """Модель пользователя библиотеки."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    bookings = relationship(
        "Booking", back_populates="user", cascade="all, delete-orphan"
    )  # type: ignore

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"


class Book(Base):  # type: ignore
    """Модель книги."""

    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    copies_available = Column(Integer, default=0)

    bookings = relationship(
        "Booking", back_populates="book", cascade="all, delete-orphan"
    )  # type: ignore

    def __repr__(self) -> str:
        return (
            f"<Book(id={self.id}, title='{self.title}', author='{self.author}', "
            f"copies_available={self.copies_available})>"
        )


class Booking(Base):  # type: ignore
    """Модель бронирования книги пользователем."""

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    booking_date = Column(Date, default=date.today)

    user = relationship("User", back_populates="bookings")  # type: ignore
    book = relationship("Book", back_populates="bookings")  # type: ignore

    def __repr__(self) -> str:
        return (
            f"<Booking(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, "
            f"booking_date={self.booking_date})>"
        )
