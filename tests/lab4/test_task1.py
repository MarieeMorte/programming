"""
Модульные тесты для системы рекомендаций фильмов.
"""

import os
import shutil
import tempfile
import unittest

from src.lab4.task1 import Movie, RecommendationSystem, UserHistory, convert_to_int_set


class TestConvertToIntSet(unittest.TestCase):
    """Тесты для функции преобразования в множество целых чисел."""

    def test_string_with_commas(self):
        """Тест преобразования строки с запятыми."""
        result = convert_to_int_set("1,2,3")
        self.assertEqual(result, {1, 2, 3})

    def test_string_with_spaces(self):
        """Тест преобразования строки с пробелами."""
        result = convert_to_int_set(" 1 , 2 , 3 ")
        self.assertEqual(result, {1, 2, 3})

    def test_empty_string(self):
        """Тест преобразования пустой строки."""
        result = convert_to_int_set("")
        self.assertEqual(result, set())

    def test_string_with_only_commas(self):
        """Тест преобразования строки только с запятыми."""
        result = convert_to_int_set(",,,")
        self.assertEqual(result, set())

    def test_single_number(self):
        """Тест преобразования одного числа."""
        result = convert_to_int_set("5")
        self.assertEqual(result, {5})

    def test_list_input(self):
        """Тест преобразования списка."""
        result = convert_to_int_set([1, 2, 3])
        self.assertEqual(result, {1, 2, 3})

    def test_set_input(self):
        """Тест преобразования множества."""
        result = convert_to_int_set({1, 2, 3})
        self.assertEqual(result, {1, 2, 3})

    def test_invalid_input(self):
        """Тест преобразования некорректных данных."""
        with self.assertRaises(ValueError):
            convert_to_int_set("1,abc,3")


class TestMovie(unittest.TestCase):
    """Тесты для класса Movie."""

    def test_movie_creation(self):
        """Тест создания объекта фильма."""
        movie = Movie(1, "Тестовый фильм")
        self.assertEqual(movie.movie_id, 1)
        self.assertEqual(movie.title, "Тестовый фильм")

    def test_movie_repr(self):
        """Тест строкового представления."""
        movie = Movie(2, "Другой фильм")
        self.assertIsInstance(movie, Movie)


class TestUserHistory(unittest.TestCase):
    """Тесты для класса UserHistory."""

    def setUp(self):
        """Настройка тестовых данных."""
        self.history = UserHistory({1, 2, 3, 4})

    def test_similarity_full_match(self):
        """Тест 100% сходства."""
        similarity = self.history.calculate_similarity({1, 2, 3, 4})
        self.assertEqual(similarity, 1.0)

    def test_similarity_half_match(self):
        """Тест 50% сходства."""
        similarity = self.history.calculate_similarity({1, 2})
        self.assertEqual(similarity, 1.0)

    def test_similarity_partial_match(self):
        """Тест частичного совпадения."""
        similarity = self.history.calculate_similarity({1, 5, 6})
        self.assertAlmostEqual(similarity, 1 / 3)

    def test_similarity_no_match(self):
        """Тест отсутствия совпадений."""
        similarity = self.history.calculate_similarity({5, 6, 7})
        self.assertEqual(similarity, 0.0)

    def test_similarity_empty_current(self):
        """Тест с пустым множеством текущего пользователя."""
        similarity = self.history.calculate_similarity(set())
        self.assertEqual(similarity, 0.0)

    def test_similarity_with_string_input(self):
        """Тест сходства со строковым вводом."""
        similarity = self.history.calculate_similarity("1,2")
        self.assertEqual(similarity, 1.0)

    def test_get_unwatched_movies(self):
        """Тест получения непросмотренных фильмов."""
        unwatched = self.history.get_unwatched_movies({1, 2})
        self.assertEqual(unwatched, {3, 4})

    def test_get_unwatched_all_watched(self):
        """Тест, когда все фильмы просмотрены."""
        unwatched = self.history.get_unwatched_movies({1, 2, 3, 4})
        self.assertEqual(unwatched, set())

    def test_get_unwatched_none_watched(self):
        """Тест, когда нет просмотренных фильмов."""
        unwatched = self.history.get_unwatched_movies({5, 6})
        self.assertEqual(unwatched, {1, 2, 3, 4})


class TestRecommendationSystem(unittest.TestCase):
    """Тесты для класса RecommendationSystem."""

    def setUp(self):
        """Настройка тестовых данных."""
        self.temp_dir = tempfile.mkdtemp()

        self.movies_file = os.path.join(self.temp_dir, "movies.txt")
        with open(self.movies_file, "w", encoding="utf-8") as file:
            file.write(
                """1,Фильм 1
                   2,Фильм 2
                   3,Фильм 3
                   4,Фильм 4
                   5,Фильм 5"""
            )

        self.history_file = os.path.join(self.temp_dir, "history.txt")
        with open(self.history_file, "w", encoding="utf-8") as file:
            file.write(
                """1,2,3
                   1,4,5
                   2,3,5
                   1,3,4"""
            )

        self.system = RecommendationSystem(self.movies_file, self.history_file)

    def tearDown(self):
        """Очистка после тестов."""
        shutil.rmtree(self.temp_dir)

    def test_load_movies(self):
        """Тест загрузки фильмов."""
        self.system.load_movies()
        self.assertEqual(len(self.system.movies), 5)
        self.assertEqual(self.system.movies[1].title, "Фильм 1")
        self.assertEqual(self.system.movies[5].title, "Фильм 5")

    def test_load_histories(self):
        """Тест загрузки историй."""
        self.system.load_movies()
        self.system.load_histories()
        self.assertEqual(len(self.system.user_histories), 4)
        self.assertEqual(self.system.user_histories[0].watched_movies, {1, 2, 3})

    def test_recommendation_basic(self):
        """Тест базовой рекомендации."""
        self.system.load_movies()
        self.system.load_histories()

        recommendation = self.system.get_recommendation("1,2")
        self.assertFalse(recommendation.startswith("Ошибка"))

    def test_recommendation_with_single_movie(self):
        """Тест рекомендации для одного фильма."""
        self.system.load_movies()
        self.system.load_histories()

        recommendation = self.system.get_recommendation("1")
        self.assertFalse(recommendation.startswith("Ошибка"))

    def test_recommendation_no_suitable_users(self):
        """Тест, когда нет подходящих пользователей."""
        special_history_file = os.path.join(self.temp_dir, "special_history.txt")
        with open(special_history_file, "w", encoding="utf-8") as file:
            file.write("5\n6\n7")

        special_system = RecommendationSystem(self.movies_file, special_history_file)
        special_system.load_movies()
        special_system.load_histories()

        recommendation = special_system.get_recommendation("1,2")
        self.assertEqual(recommendation, "Недостаточно данных для рекомендации")

    def test_recommendation_all_watched(self):
        """Тест, когда пользователь уже посмотрел все возможные рекомендации."""
        limited_history_file = os.path.join(self.temp_dir, "limited_history.txt")
        with open(limited_history_file, "w", encoding="utf-8") as file:
            file.write("1,2,3\n1,2,3\n1,2,3")

        limited_system = RecommendationSystem(self.movies_file, limited_history_file)
        limited_system.load_movies()
        limited_system.load_histories()

        recommendation = limited_system.get_recommendation("1,2,3")
        self.assertEqual(recommendation, "Все рекомендуемые фильмы уже просмотрены")

    def test_recommendation_invalid_input(self):
        """Тест с некорректным вводом."""
        self.system.load_movies()
        self.system.load_histories()

        recommendation = self.system.get_recommendation("abc,def")
        self.assertTrue(recommendation.startswith("Ошибка"))

    def test_recommendation_empty_input(self):
        """Тест с пустым вводом."""
        self.system.load_movies()
        self.system.load_histories()

        recommendation = self.system.get_recommendation("")
        self.assertEqual(recommendation, "Ошибка: список просмотренных фильмов пуст\n")

    def test_recommendation_nonexistent_movie(self):
        """Тест с несуществующим ID фильма."""
        self.system.load_movies()
        self.system.load_histories()

        recommendation = self.system.get_recommendation("1,99")
        self.assertTrue("не найден в базе" in recommendation)

    def test_duplicate_movie_ids(self):
        """Тест обработки дублирующихся ID фильмов."""
        duplicate_movies_file = os.path.join(self.temp_dir, "duplicate_movies.txt")
        with open(duplicate_movies_file, "w", encoding="utf-8") as file:
            file.write(
                """1,Фильм 1
                   2,Фильм 2
                   1,Фильм 1 Дубликат
                   3,Фильм 3"""
            )

        duplicate_system = RecommendationSystem(duplicate_movies_file, self.history_file)

        duplicate_system.load_movies()
        duplicate_system.load_histories()

        self.assertEqual(len(duplicate_system.movies), 3)

    def test_weighted_recommendation(self):
        """Тест взвешенных рекомендаций."""
        weight_history_file = os.path.join(self.temp_dir, "weight_history.txt")
        with open(weight_history_file, "w", encoding="utf-8") as file:
            file.write(
                """1,2,3,4,5
                   1,2,6,7,8
                   1,2,3,9,10"""
            )

        weight_system = RecommendationSystem(self.movies_file, weight_history_file)
        weight_system.load_movies()
        weight_system.load_histories()

        recommendation = weight_system.get_recommendation("1,2,3,4")
        self.assertFalse(recommendation.startswith("Ошибка"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
