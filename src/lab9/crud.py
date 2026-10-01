"""
Функции для работы с базой данных: добавление пользователей, книг,
создание и отмена бронирований.
"""

from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from .models import Book, Booking, User


def add_user(session: Session, name: str, email: str) -> User:
    """Добавляет нового пользователя."""
    existing = session.query(User).filter(User.email == email).first()
    if existing:
        raise ValueError(f"Пользователь с email '{email}' уже существует.")
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    return user


def add_book(session: Session, title: str, author: str, copies: int = 1) -> Book:
    """Добавляет новую книгу с указанным количеством доступных копий."""
    book = Book(title=title, author=author, copies_available=copies)
    session.add(book)
    session.commit()
    return book


def create_booking(session: Session, user_id: int, book_id: int) -> Booking:
    """Создаёт бронирование для пользователя на книгу."""
    user = session.get(User, user_id)
    if not user:
        raise ValueError(f"Пользователь с id {user_id} не найден.")
    book = session.get(Book, book_id)
    if not book:
        raise ValueError(f"Книга с id {book_id} не найдена.")
    if book.copies_available <= 0:
        raise ValueError(f"Нет доступных копий книги '{book.title}'.")

    booking = Booking(user_id=user_id, book_id=book_id, booking_date=date.today())
    book.copies_available -= 1
    session.add(booking)
    session.commit()
    return booking


def cancel_booking(session: Session, booking_id: int) -> None:
    """Отменяет бронирование по его id."""
    booking = session.get(Booking, booking_id)
    if not booking:
        raise ValueError(f"Бронирование с id {booking_id} не найдено.")
    book = booking.book
    book.copies_available += 1
    session.delete(booking)
    session.commit()


def get_user_bookings(session: Session, user_id: int) -> list[Booking]:
    """Возвращает все бронирования пользователя."""
    user = session.get(User, user_id)
    if not user:
        raise ValueError(f"Пользователь с id {user_id} не найден.")
    return user.bookings # type: ignore


def get_book_by_title(session: Session, title: str) -> Optional[Book]:
    """Находит книгу по точному названию (возвращает первую)."""
    return session.query(Book).filter(Book.title == title).first()
