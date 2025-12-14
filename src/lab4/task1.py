"""
Система рекомендаций фильмов для кинотеатра "Сокол".

Анализирует историю просмотров пользователей и рекомендует фильмы
на основе предпочтений похожих пользователей.
"""
import sys


def convert_to_int_set(data):
    """Безопасно преобразует данные в множество целых чисел"""
    if isinstance(data, set):
        if all(isinstance(x, int) for x in data):
            return data
        return {int(x) for x in data}

    if isinstance(data, (list, tuple)):
        return {int(x) for x in data}

    if isinstance(data, str):
        return {int(x.strip()) for x in data.split(",") if x.strip()}

    raise TypeError(f"Неподдерживаемый тип данных: {type(data)}")


class Movie:  # pylint: disable=too-few-public-methods
    """
    Класс для представления фильма.

    Хранит идентификатор и название фильма для использования в системе рекомендаций.
    """

    def __init__(self, movie_id, title):
        self.movie_id = movie_id
        self.title = title


class UserHistory:
    """
    Представляет историю просмотров пользователя.

    Хранит множество просмотренных фильмов
    и предоставляет методы для вычисления сходства с другим пользователем
    и получения рекомендаций на основе общих предпочтений.
    """

    def __init__(self, watched_movies):
        try:
            self.watched_movies = convert_to_int_set(watched_movies)
        except (TypeError, ValueError) as error:
            self.watched_movies = set()
            print(f"Предупреждение: не удалось создать историю просмотров: {error}")

    def calculate_similarity(self, current_user_movies):
        """
        Вычисляет степень сходства с другим пользователем.
        """
        try:
            current_set = convert_to_int_set(current_user_movies)
        except (TypeError, ValueError):
            return 0.0

        if not current_set:
            return 0.0

        common = len(self.watched_movies.intersection(current_set))
        return common / len(current_set)

    def get_unwatched_movies(self, current_user_movies):
        """
        Возвращает фильмы, просмотренные другим пользователем, и не просмотренные текущим.
        """
        try:
            current_set = convert_to_int_set(current_user_movies)
        except (TypeError, ValueError):
            return self.watched_movies.copy()

        return self.watched_movies - current_set


class RecommendationSystem:
    """Основная система рекомендаций фильмов."""

    def __init__(self, movies_file="movies.txt", history_file="history.txt"):
        self.movies_file = movies_file
        self.history_file = history_file
        self.movies = {}
        self.user_histories = []

    def load_movies(self):
        """
        Загружает список фильмов из файла.

        Читает файл с фильмами, парсит каждую строку и создает объекты Movie.
        Пропускает строки с некорректным форматом или дублирующимися ID.
        """
        try:
            with open(self.movies_file, "r", encoding="utf-8") as file:
                line_num = 0
                for line in file:
                    line_num += 1
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split(",", 1)
                    if len(parts) != 2:
                        print(f"Ошибка в строке {line_num}: '{line}' - неверный формат\n")
                        continue

                    try:
                        movie_id = int(parts[0].strip())
                        title = parts[1].strip()

                        if movie_id in self.movies:
                            print(
                                f"Ошибка в строке {line_num}. ID {movie_id} уже зарегистрирован!\n"
                            )
                            continue

                        self.movies[movie_id] = Movie(movie_id, title)

                    except ValueError:
                        print(f"Ошибка в строке {line_num}: '{line}' - ID должен быть числом\nh3u")
                        continue

        except FileNotFoundError:
            print(f"Файл {self.movies_file} не найден")
            sys.exit(1)

    def load_histories(self):
        """
        Загружает истории просмотров пользователей из файла.

        Читает файл с историями,
        преобразует каждую строку в множество ID и создает объекты UserHistory.
        Пропускает пустые и некорректные строки.
        """
        try:
            with open(self.history_file, encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        movie_ids = convert_to_int_set(line)
                        if movie_ids:
                            self.user_histories.append(UserHistory(movie_ids))
                    except (ValueError, TypeError):
                        pass

        except FileNotFoundError:
            print(f"Файл {self.history_file} не найден")
            sys.exit(1)

    def get_recommendation(self, current_user_input):
        """
        Генерирует рекомендацию на основе введённых фильмов.
        """
        try:
            current_user_movies = convert_to_int_set(current_user_input)
        except (ValueError, TypeError) as error:
            return f"Ошибка ввода: {str(error)}\n"

        if not current_user_movies:
            return "Ошибка: список просмотренных фильмов пуст\n"

        for movie_id in current_user_movies:
            if movie_id not in self.movies:
                return f"Ошибка: фильм с ID {movie_id} не найден в базе\n"

        suitable_histories = []
        for history in self.user_histories:
            similarity = history.calculate_similarity(current_user_movies)
            if similarity >= 0.5:
                suitable_histories.append((history, similarity))

        if not suitable_histories:
            return "Недостаточно данных для рекомендации"

        movie_weights = {}

        for history, weight in suitable_histories:
            unwatched_movies = history.get_unwatched_movies(current_user_movies)
            for movie_id in unwatched_movies:
                if movie_id in self.movies:
                    movie_weights[movie_id] = movie_weights.get(movie_id, 0.0) + weight

        if not movie_weights:
            return "Все рекомендуемые фильмы уже просмотрены"

        recommended_movie_id = max(movie_weights, key=lambda m_id: movie_weights[m_id])

        return self.movies[recommended_movie_id].title

    def run(self):
        """
        Запускает интерактивный режим работы системы.

        Загружает данные и входит в цикл диалога с пользователем,
        запрашивая фильмы для рекомендации.
        """
        print("Система рекомендаций фильмов\n")

        self.load_movies()
        self.load_histories()

        while True:
            user_input = input(
                'Введите ID просмотренных фильмов через запятую (или "выход" для завершения): '
            ).strip()

            if user_input.lower() == "выход":
                print("До свидания!")
                break

            if not user_input:
                print("\nОшибка: введите хотя бы один ID фильма\n")
                continue

            result = self.get_recommendation(user_input)

            if result.startswith("Ошибка"):
                print(f"\n{result}")
            else:
                print(f"Рекомендация: {result}\n")


def main():
    """
    Точка входа в программу.

    Создаёт и запускает систему рекомендаций фильмов.
    Использует файлы movies.txt и history.txt по умолчанию.
    """
    movies_file = "movies.txt"
    history_file = "history.txt"

    system = RecommendationSystem(movies_file, history_file)
    system.run()


if __name__ == "__main__":
    main()
