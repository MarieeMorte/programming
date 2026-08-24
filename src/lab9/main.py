"""Демонстрация работы системы бронирования книг."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .crud import add_book, add_user, cancel_booking, create_booking
from .models import Base


def main() -> None:
    """Создаёт базу данных, добавляет данные и демонстрирует операции."""
    db_path = os.path.join(os.path.dirname(__file__), "library.db")
    engine = create_engine(f"sqlite:///{db_path}", echo=True)
    Base.metadata.create_all(engine)  # type: ignore

    session_factory = sessionmaker(bind=engine)
    session = session_factory()

    try:
        user1 = add_user(session, "Иван Петров", "ivan@example.com")
        user2 = add_user(session, "Мария Смирнова", "maria@example.com")
        print(f"Добавлены пользователи: {user1}, {user2}")

        book1 = add_book(session, "Война и мир", "Лев Толстой", copies=3)
        book2 = add_book(session, "Преступление и наказание", "Фёдор Достоевский", copies=1)
        print(f"Добавлены книги: {book1}, {book2}")

        booking1 = create_booking(session, user1.id, book1.id)  # type: ignore
        print(f"Создано бронирование: {booking1}")
        booking2 = create_booking(session, user2.id, book1.id)  # type: ignore
        print(f"Создано бронирование: {booking2}")

        try:
            create_booking(session, user1.id, book2.id)  # type: ignore
        except ValueError as e:
            print(f"Ожидаемая ошибка: {e}")

        cancel_booking(session, booking1.id)  # type: ignore
        print(f"Отменено бронирование {booking1.id}")

        session.refresh(book1)
        print(f"Доступно копий '{book1.title}': {book1.copies_available}")

    finally:
        session.close()


if __name__ == "__main__":
    main()
