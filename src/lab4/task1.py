import sys


def _convert_to_int_set(data):
    """Безопасно преобразует данные в множество целых чисел"""
    if isinstance(data, set):
        if all(isinstance(x, int) for x in data):
            return data
        else:
            return {int(x) for x in data}
    elif isinstance(data, (list, tuple)):
        return {int(x) for x in data}
    elif isinstance(data, str):
        return {int(x.strip()) for x in data.split(",") if x.strip()}
    else:
        raise TypeError(f"Неподдерживаемый тип данных: {type(data)}")


class Movie:
    def __init__(self, movie_id, title):
        self.id = movie_id
        self.title = title


class UserHistory:
    def __init__(self, watched_movies):
        try:
            self.watched_movies = _convert_to_int_set(watched_movies)
        except (TypeError, ValueError) as e:
            self.watched_movies = set()
            print(f"Предупреждение: не удалось создать историю просмотров: {e}")

    def calculate_similarity(self, current_user_movies):
        try:
            current_set = _convert_to_int_set(current_user_movies)
        except (TypeError, ValueError):
            return 0.0

        if not current_set:
            return 0.0

        common = len(self.watched_movies.intersection(current_set))
        return common / len(current_set)

    def get_unwatched_movies(self, current_user_movies):
        try:
            current_set = _convert_to_int_set(current_user_movies)
        except (TypeError, ValueError):
            return self.watched_movies.copy()

        return self.watched_movies - current_set


class RecommendationSystem:
    def __init__(self, movies_file="movies.txt", history_file="history.txt"):
        self.movies_file = movies_file
        self.history_file = history_file
        self.movies = {}
        self.user_histories = []

    def load_movies(self):
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
                            print(f"Ошибка в строке {line_num}. ID {movie_id} уже зарегистрирован!\n")
                            continue

                        self.movies[movie_id] = Movie(movie_id, title)

                    except ValueError:
                        print(f"Ошибка в строке {line_num}: '{line}' - ID должен быть числом\nh3u")
                        continue

        except FileNotFoundError:
            print(f"Файл {self.movies_file} не найден")
            sys.exit(1)

    def load_histories(self):
        try:
            with open(self.history_file, encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        movie_ids = _convert_to_int_set(line)
                        if movie_ids:
                            self.user_histories.append(UserHistory(movie_ids))
                    except (ValueError, TypeError):
                        pass

        except FileNotFoundError:
            print(f"Файл {self.history_file} не найден")
            sys.exit(1)
        except Exception as e:
            print(f"Ошибка при чтении файла с историей: {e}")
            sys.exit(1)

    def get_recommendation(self, current_user_input):
        try:
            current_user_movies = _convert_to_int_set(current_user_input)
        except (ValueError, TypeError) as e:
            return f"Ошибка ввода: {str(e)}\n"

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
        print("Система рекомендаций фильмов\n")

        self.load_movies()
        self.load_histories()

        while True:
            user_input = input('Введите ID просмотренных фильмов через запятую (или "выход" для завершения): ').strip()

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
    movies_file = "movies.txt"
    history_file = "history.txt"

    system = RecommendationSystem(movies_file, history_file)
    system.run()


if __name__ == "__main__":
    main()
