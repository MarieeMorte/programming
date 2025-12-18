"""
Модульные тесты для приложения разбивки респондентов по возрастным группам.
"""

import sys
import unittest
from io import StringIO

from src.lab4.task2 import AgeGroup, AgeGroupManager, Respondent, main, read_respondents


class TestRespondent(unittest.TestCase):
    """Тесты для класса Respondent."""

    def test_initialization(self):
        """Тест инициализации респондента."""
        respondent = Respondent("Иванов Иван Иванович", 30)
        self.assertEqual(respondent.name, "Иванов Иван Иванович")
        self.assertEqual(respondent.age, 30)

    def test_str_representation(self):
        """Тест строкового представления респондента."""
        respondent = Respondent("Петров Петр Петрович", 25)
        self.assertEqual(str(respondent), "Петров Петр Петрович (25)")

    def test_comparison_different_ages(self):
        """Тест сравнения респондентов с разным возрастом."""
        younger = Respondent("А", 20)
        older = Respondent("Б", 30)
        self.assertTrue(older < younger)
        self.assertFalse(younger < older)

    def test_comparison_same_age(self):
        """Тест сравнения респондентов с одинаковым возрастом."""
        first = Respondent("Абрамов", 25)
        second = Respondent("Борисов", 25)
        self.assertTrue(first < second)
        self.assertFalse(second < first)


class TestAgeGroup(unittest.TestCase):
    """Тесты для класса AgeGroup."""

    def test_initialization_with_max_age(self):
        """Тест инициализации группы с максимальным возрастом."""
        group = AgeGroup(0, 18)
        self.assertEqual(group.min_age, 0)
        self.assertEqual(group.max_age, 18)
        self.assertEqual(group.respondents, [])

    def test_initialization_without_max_age(self):
        """Тест инициализации группы без максимального возраста."""
        group = AgeGroup(80, None)
        self.assertEqual(group.min_age, 80)
        self.assertIsNone(group.max_age)

    def test_add_respondent(self):
        """Тест добавления респондента в группу."""
        group = AgeGroup(0, 18)
        respondent = Respondent("Тестов Тест Тестович", 15)
        group.add_respondent(respondent)
        self.assertEqual(len(group.respondents), 1)
        self.assertEqual(group.respondents[0], respondent)

    def test_is_empty(self):
        """Тест проверки пустоты группы."""
        group = AgeGroup(0, 18)
        self.assertTrue(group.is_empty())

        group.add_respondent(Respondent("Тестов", 15))
        self.assertFalse(group.is_empty())

    def test_get_name_with_max_age(self):
        """Тест получения имени группы с максимальным возрастом."""
        group = AgeGroup(0, 18)
        self.assertEqual(group.get_name(), "0-18")

    def test_get_name_without_max_age(self):
        """Тест получения имени группы без максимального возраста."""
        group = AgeGroup(80, None)
        self.assertEqual(group.get_name(), "80+")

    def test_sort_respondents(self):
        """Тест сортировки респондентов в группе."""
        group = AgeGroup(20, 30)

        respondent1 = Respondent("Борисов", 25)
        respondent2 = Respondent("Абрамов", 30)
        respondent3 = Respondent("Владимиров", 22)

        group.add_respondent(respondent1)
        group.add_respondent(respondent2)
        group.add_respondent(respondent3)

        group.sort_respondents()

        self.assertEqual(group.respondents[0], respondent2)
        self.assertEqual(group.respondents[1], respondent1)
        self.assertEqual(group.respondents[2], respondent3)

    def test_str_representation(self):
        """Тест строкового представления группы."""
        group = AgeGroup(20, 30)
        group.add_respondent(Respondent("Иванов", 25))
        group.add_respondent(Respondent("Петров", 30))

        expected = "20-30: Петров (30), Иванов (25)"
        self.assertEqual(str(group), expected)


class TestAgeGroupManager(unittest.TestCase):
    """Тесты для класса AgeGroupManager."""

    def test_create_groups(self):
        """Тест создания возрастных групп по границам."""
        manager = AgeGroupManager([18, 25, 35])
        groups = manager.groups

        self.assertEqual(len(groups), 4)

        self.assertEqual(groups[0].min_age, 0)
        self.assertEqual(groups[0].max_age, 18)

        self.assertEqual(groups[1].min_age, 19)
        self.assertEqual(groups[1].max_age, 25)

        self.assertEqual(groups[2].min_age, 26)
        self.assertEqual(groups[2].max_age, 35)

        self.assertEqual(groups[3].min_age, 36)
        self.assertIsNone(groups[3].max_age)

    def test_add_respondent_to_correct_group(self):
        """Тест добавления респондента в правильную группу."""
        manager = AgeGroupManager([18, 25, 35])

        manager.add_respondent("Младший", 15)
        self.assertEqual(len(manager.groups[0].respondents), 1)

        manager.add_respondent("Средний", 20)
        self.assertEqual(len(manager.groups[1].respondents), 1)

        manager.add_respondent("Старший", 30)
        self.assertEqual(len(manager.groups[2].respondents), 1)

        manager.add_respondent("Ветеран", 40)
        self.assertEqual(len(manager.groups[3].respondents), 1)

    def test_get_non_empty_groups(self):
        """Тест получения непустых групп в правильном порядке."""
        manager = AgeGroupManager([18, 25, 35])

        manager.add_respondent("Ребенок", 10)
        manager.add_respondent("Взрослый", 30)
        manager.add_respondent("Пенсионер", 70)

        non_empty_groups = manager.get_non_empty_groups()

        self.assertEqual(len(non_empty_groups), 3)

        self.assertEqual(non_empty_groups[0].get_name(), "36+")
        self.assertEqual(non_empty_groups[1].get_name(), "26-35")
        self.assertEqual(non_empty_groups[2].get_name(), "0-18")

    def test_empty_groups_are_filtered(self):
        """Тест фильтрации пустых групп."""
        manager = AgeGroupManager([18, 25, 35])

        non_empty_groups = manager.get_non_empty_groups()
        self.assertEqual(len(non_empty_groups), 0)


class TestReadRespondents(unittest.TestCase):
    """Тесты для функции чтения респондентов."""

    def test_read_valid_respondents(self):
        """Тест чтения корректных данных респондентов."""
        original_stdin = sys.stdin

        try:
            test_input = StringIO(
                "Иванов Иван Иванович,30\nПетров Петр Петрович,25\nEND\n"
            )
            sys.stdin = test_input

            respondents = read_respondents()

            self.assertEqual(len(respondents), 2)
            self.assertEqual(respondents[0], ("Иванов Иван Иванович", 30))
            self.assertEqual(respondents[1], ("Петров Петр Петрович", 25))
        finally:
            sys.stdin = original_stdin

    def test_skip_empty_lines(self):
        """Тест пропуска пустых строк."""
        original_stdin = sys.stdin

        try:
            test_input = StringIO(
                "Иванов Иван Иванович,30\n\nПетров Петр Петрович,25\nEND\n"
            )
            sys.stdin = test_input

            respondents = read_respondents()

            self.assertEqual(len(respondents), 2)
            self.assertNotIn(("", 0), respondents)
        finally:
            sys.stdin = original_stdin

    def test_handle_invalid_format(self):
        """Тест обработки некорректного формата строки."""
        original_stdin = sys.stdin

        try:
            test_input = StringIO(
                "Некорректная строка без запятой\nИванов Иван,30\nEND\n"
            )
            sys.stdin = test_input

            respondents = read_respondents()

            self.assertEqual(len(respondents), 1)
            self.assertEqual(respondents[0], ("Иванов Иван", 30))
        finally:
            sys.stdin = original_stdin

    def test_handle_missing_name(self):
        """Тест обработки строки без ФИО."""
        original_stdin = sys.stdin

        try:
            test_input = StringIO(",30\nИванов Иван,30\nEND\n")
            sys.stdin = test_input

            respondents = read_respondents()

            self.assertEqual(len(respondents), 1)
        finally:
            sys.stdin = original_stdin

    def test_handle_non_numeric_age(self):
        """Тест обработки нечислового возраста."""
        original_stdin = sys.stdin

        try:
            test_input = StringIO("Иванов Иван,не_число\nПетров Петр,25\nEND\n")
            sys.stdin = test_input

            respondents = read_respondents()

            self.assertEqual(len(respondents), 1)
            self.assertEqual(respondents[0], ("Петров Петр", 25))
        finally:
            sys.stdin = original_stdin

    def test_handle_age_out_of_range(self):
        """Тест обработки возраста вне допустимого диапазона."""
        original_stdin = sys.stdin

        try:
            test_input = StringIO(
                "Иванов Иван,-5\nПетров Петр,150\nСидоров Сидор,50\nEND\n"
            )
            sys.stdin = test_input

            respondents = read_respondents()

            self.assertEqual(len(respondents), 1)
            self.assertEqual(respondents[0], ("Сидоров Сидор", 50))
        finally:
            sys.stdin = original_stdin


class TestMainFunction(unittest.TestCase):
    """Тесты для основной функции программы."""

    def test_main_successful_execution(self):
        """Тест успешного выполнения программы."""
        original_argv = sys.argv
        original_stdin = sys.stdin

        try:
            sys.argv = ["task2.py", "18", "25", "35"]

            test_input = StringIO(
                "Иванов Иван Иванович,30\nПетров Петр Петрович,20\n"
                "Сидоров Сидор Сидорович,10\nEND\n"
            )
            sys.stdin = test_input

            output = StringIO()
            original_stdout = sys.stdout
            sys.stdout = output

            main()

            sys.stdout = original_stdout

            output_str = output.getvalue()

            self.assertIn("26-35: Иванов Иван Иванович (30)", output_str)
            self.assertIn("19-25: Петров Петр Петрович (20)", output_str)
            self.assertIn("0-18: Сидоров Сидор Сидорович (10)", output_str)
        finally:
            sys.argv = original_argv
            sys.stdin = original_stdin

    def test_main_no_respondents(self):
        """Тест выполнения программы без респондентов."""
        original_argv = sys.argv
        original_stdin = sys.stdin

        try:
            sys.argv = ["task2.py", "18", "25", "35"]
            test_input = StringIO("END\n")
            sys.stdin = test_input

            output = StringIO()
            original_stdout = sys.stdout
            sys.stdout = output

            main()

            sys.stdout = original_stdout
            output_str = output.getvalue()

            self.assertIn("Нет респондентов для отображения", output_str)
        finally:
            sys.argv = original_argv
            sys.stdin = original_stdin

    def test_main_no_arguments(self):
        """Тест выполнения программы без аргументов командной строки."""
        original_argv = sys.argv

        try:
            sys.argv = ["task2.py"]

            try:
                main()
                self.fail("Expected SystemExit but it didn't happen")
            except SystemExit as system_exit:
                self.assertEqual(system_exit.code, 1)
        finally:
            sys.argv = original_argv

    def test_main_invalid_arguments(self):
        """Тест выполнения программы с некорректными аргументами."""
        original_argv = sys.argv

        try:
            sys.argv = ["task2.py", "18", "not_a_number", "35"]

            try:
                main()
                self.fail("Expected SystemExit but it didn't happen")
            except SystemExit as system_exit:
                self.assertEqual(system_exit.code, 1)
        finally:
            sys.argv = original_argv

    def test_main_non_positive_boundaries(self):
        """Тест выполнения программы с неположительными границами."""
        original_argv = sys.argv

        try:
            sys.argv = ["task2.py", "18", "0", "35"]

            try:
                main()
                self.fail("Expected SystemExit but it didn't happen")
            except SystemExit as system_exit:
                self.assertEqual(system_exit.code, 1)
        finally:
            sys.argv = original_argv


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты"""

    def test_complete_workflow(self):
        """Тест полного рабочего процесса."""
        manager = AgeGroupManager([18, 25, 35, 45, 60, 80, 100])

        respondents = [
            ("Кошельков Захар Брониславович", 105),
            ("Дьячков Нисон Иринеевич", 88),
            ("Иванов Варлам Якунович", 88),
            ("Старостин Ростислав Ермолаевич", 50),
            ("Ярилова Розалия Трофимовна", 29),
            ("Соколов Андрей Сергеевич", 15),
            ("Егоров Алан Петрович", 7),
        ]

        for name, age in respondents:
            manager.add_respondent(name, age)

        non_empty_groups = manager.get_non_empty_groups()

        self.assertEqual(len(non_empty_groups), 5)

        self.assertEqual(non_empty_groups[0].get_name(), "101+")
        self.assertEqual(non_empty_groups[1].get_name(), "81-100")
        self.assertEqual(non_empty_groups[2].get_name(), "46-60")
        self.assertEqual(non_empty_groups[3].get_name(), "26-35")
        self.assertEqual(non_empty_groups[4].get_name(), "0-18")

        oldest_group = non_empty_groups[0]
        self.assertEqual(len(oldest_group.respondents), 1)
        self.assertEqual(
            str(oldest_group.respondents[0]), "Кошельков Захар Брониславович (105)"
        )

        second_group = non_empty_groups[1]
        self.assertEqual(len(second_group.respondents), 2)
        self.assertEqual(
            str(second_group.respondents[0]), "Дьячков Нисон Иринеевич (88)"
        )
        self.assertEqual(
            str(second_group.respondents[1]), "Иванов Варлам Якунович (88)"
        )


if __name__ == "__main__":
    unittest.main()
