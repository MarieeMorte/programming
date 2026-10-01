"""Определение моделей SQLAlchemy для системы бронирования книг."""
# pylint: disable=too-few-public-methods

from datetime import date
from typing import List

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""


class User(Base):
    """Модель пользователя библиотеки."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    bookings: Mapped[List["Booking"]] = relationship(
        "Booking", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"


class Book(Base):
    """Модель книги."""

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    copies_available: Mapped[int] = mapped_column(Integer, default=0)

    bookings: Mapped[List["Booking"]] = relationship(
        "Booking", back_populates="book", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<Book(id={self.id}, title='{self.title}', author='{self.author}', "
            f"copies_available={self.copies_available})>"
        )


class Booking(Base):
    """Модель бронирования книги пользователем."""

    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    booking_date: Mapped[date] = mapped_column(Date, default=date.today)

    user: Mapped["User"] = relationship("User", back_populates="bookings")
    book: Mapped["Book"] = relationship("Book", back_populates="bookings")

    def __repr__(self) -> str:
        return (
            f"<Booking(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, "
            f"booking_date={self.booking_date})>"
        )
