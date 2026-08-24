"""Unit-тесты для CRUD-операций системы бронирования книг."""

import unittest
from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.lab9.crud import (
    add_book,
    add_user,
    cancel_booking,
    create_booking,
    get_book_by_title,
    get_user_bookings,
)
from src.lab9.models import Base, Booking


class TestLibraryCRUD(unittest.TestCase):
    """Набор тестов для проверки работы с библиотекой."""

    def setUp(self) -> None:
        """Создаём временную in-memory базу и сессию."""
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)  # type: ignore
        self.session_factory = sessionmaker(bind=self.engine)
        self.session = self.session_factory()

    def tearDown(self) -> None:
        """Закрываем сессию."""
        self.session.close()

    def test_add_user(self) -> None:
        """Проверяем добавление пользователя и уникальность email."""
        user = add_user(self.session, "Alice", "alice@example.com")
        self.assertEqual(user.name, "Alice")
        self.assertEqual(user.email, "alice@example.com")
        with self.assertRaises(ValueError) as ctx:
            add_user(self.session, "Bob", "alice@example.com")
        self.assertIn("уже существует", str(ctx.exception))

    def test_add_book(self) -> None:
        """Проверяем добавление книги."""
        book = add_book(self.session, "1984", "George Orwell", copies=5)
        self.assertEqual(book.title, "1984")
        self.assertEqual(book.author, "George Orwell")
        self.assertEqual(book.copies_available, 5)

    def test_create_booking_success(self) -> None:
        """Успешное создание бронирования и уменьшение копий."""
        user = add_user(self.session, "John", "john@example.com")
        book = add_book(self.session, "Dune", "Frank Herbert", copies=2)
        booking = create_booking(self.session, user.id, book.id)  # type: ignore
        self.assertIsInstance(booking, Booking)
        self.assertEqual(booking.user_id, user.id)  # type: ignore
        self.assertEqual(booking.book_id, book.id)  # type: ignore
        self.assertEqual(booking.booking_date, date.today())
        self.session.refresh(book)
        self.assertEqual(book.copies_available, 1)

    def test_create_booking_no_copies(self) -> None:
        """Ошибка при попытке забронировать книгу без доступных копий."""
        user = add_user(self.session, "Jane", "jane@example.com")
        book = add_book(self.session, "The Hobbit", "J.R.R. Tolkien", copies=0)
        with self.assertRaises(ValueError) as ctx:
            create_booking(self.session, user.id, book.id)  # type: ignore
        self.assertIn("Нет доступных копий", str(ctx.exception))

    def test_create_booking_user_not_found(self) -> None:
        """Ошибка при несуществующем пользователе."""
        book = add_book(self.session, "The Hobbit", "J.R.R. Tolkien", copies=1)
        with self.assertRaises(ValueError) as ctx:
            create_booking(self.session, 999, book.id)  # type: ignore
        self.assertIn("не найден", str(ctx.exception))

    def test_create_booking_book_not_found(self) -> None:
        """Ошибка при несуществующей книге."""
        user = add_user(self.session, "Jane", "jane@example.com")
        with self.assertRaises(ValueError) as ctx:
            create_booking(self.session, user.id, 999)  # type: ignore
        self.assertIn("не найдена", str(ctx.exception))

    def test_cancel_booking_success(self) -> None:
        """Отмена бронирования и увеличение копий."""
        user = add_user(self.session, "Alice", "alice@example.com")
        book = add_book(self.session, "Brave New World", "Aldous Huxley", copies=1)
        booking = create_booking(self.session, user.id, book.id)  # type: ignore
        booking_id = booking.id  # type: ignore
        cancel_booking(self.session, booking_id)  # type: ignore
        self.assertIsNone(self.session.get(Booking, booking_id))  # type: ignore
        self.session.refresh(book)
        self.assertEqual(book.copies_available, 1)

    def test_cancel_booking_not_found(self) -> None:
        """Ошибка при отмене несуществующего бронирования."""
        with self.assertRaises(ValueError) as ctx:
            cancel_booking(self.session, 999)
        self.assertIn("не найдено", str(ctx.exception))

    def test_get_user_bookings(self) -> None:
        """Проверяем получение списка бронирований пользователя."""
        user = add_user(self.session, "Bob", "bob@example.com")
        book1 = add_book(self.session, "Book1", "Author1", copies=2)
        book2 = add_book(self.session, "Book2", "Author2", copies=2)
        booking1 = create_booking(self.session, user.id, book1.id)  # type: ignore
        booking2 = create_booking(self.session, user.id, book2.id)  # type: ignore

        bookings = get_user_bookings(self.session, user.id)  # type: ignore
        self.assertEqual(len(bookings), 2)
        self.assertIn(booking1, bookings)
        self.assertIn(booking2, bookings)

    def test_get_book_by_title(self) -> None:
        """Поиск книги по названию."""
        add_book(self.session, "Clean Code", "Robert C. Martin", copies=3)
        book = get_book_by_title(self.session, "Clean Code")
        self.assertIsNotNone(book)
        if book:  # для mypy
            self.assertEqual(book.author, "Robert C. Martin")
        self.assertIsNone(get_book_by_title(self.session, "Nonexistent"))


if __name__ == "__main__":
    unittest.main()
