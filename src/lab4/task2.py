import sys
from typing import List, Tuple


class Respondent:
    """Класс для представления респондента."""

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __lt__(self, other: "Respondent") -> bool:
        """Определяет порядок сортировки:
        сначала по возрасту (убывание), затем по имени (возрастание)."""
        if self.age == other.age:
            return self.name < other.name
        return self.age > other.age


class AgeGroup:
    """Класс для представления возрастной группы."""

    def __init__(self, min_age: int, max_age: int = None):
        self.min_age = min_age
        self.max_age = max_age
        self.respondents: List[Respondent] = []

    def add_respondent(self, respondent: Respondent) -> None:
        """Добавляет респондента в группу."""
        self.respondents.append(respondent)

    def sort_respondents(self) -> None:
        """Сортирует респондентов в группе по убыванию возраста,
        а при равенстве - по возрастанию имени."""
        self.respondents.sort()

    def is_empty(self) -> bool:
        """Проверяет, пуста ли группа."""
        return len(self.respondents) == 0

    def get_name(self) -> str:
        """Возвращает строковое представление диапазона возраста группы."""
        if self.max_age is None:
            return f"{self.min_age}+"
        return f"{self.min_age}-{self.max_age}"

    def __str__(self) -> str:
        """Строковое представление группы для вывода."""
        self.sort_respondents()
        respondents_str = ", ".join(str(r) for r in self.respondents)
        return f"{self.get_name()}: {respondents_str}"


class AgeGroupManager:
    """Управляет распределением респондентов по возрастным группам."""

    def __init__(self, limits: List[int]):
        self.limits = sorted(limits)
        self.groups = self._create_groups()

    def _create_groups(self) -> List[AgeGroup]:
        """Создаёт возрастные группы на основе границ."""
        groups = [AgeGroup(0, self.limits[0])]

        for i in range(1, len(self.limits)):
            min_age = self.limits[i - 1] + 1
            max_age = self.limits[i]
            groups.append(AgeGroup(min_age, max_age))

        groups.append(AgeGroup(self.limits[-1] + 1, None))

        return groups

    def add_respondent(self, name: str, age: int) -> None:
        """Добавляет респондента в соответствующую возрастную группу."""
        respondent = Respondent(name, age)

        for group in self.groups:
            if group.max_age is None:
                if age >= group.min_age:
                    group.add_respondent(respondent)
                    break
            else:
                if group.min_age <= age <= group.max_age:
                    group.add_respondent(respondent)
                    break

    def get_non_empty_groups(self) -> List[AgeGroup]:
        """Возвращает только непустые группы в порядке от старшей к младшей."""
        result = []
        for group in reversed(self.groups):
            if not group.is_empty():
                result.append(group)
        return result


def read_respondents() -> List[Tuple[str, int]]:
    """Читает данные респондентов из стандартного ввода."""
    respondents = []

    print("Введите данные респондентов (ФИО,возраст), по одному на строку.")
    print("Для завершения ввода введите 'END'.")

    while True:
        try:
            line = input().strip()
            if line == "END":
                break

            if not line:
                continue

            if "," not in line:
                print(f"Ошибка: некорректный формат строки '{line}'. Ожидается 'ФИО,возраст'")
                continue

            name, age_str = line.split(",", 1)
            name = name.strip()
            age_str = age_str.strip()

            if not name:
                print(f"Ошибка: отсутствует ФИО в строке '{line}'")
                continue

            try:
                age = int(age_str)
                if age < 0 or age > 123:
                    print(f"Ошибка: возраст {age} вне допустимого диапазона (0-123)")
                    continue

                respondents.append((name, age))

            except ValueError:
                print(f"Ошибка: возраст должен быть числом в строке '{line}'")
                continue

        except EOFError:
            break

    return respondents


def main() -> None:
    """Основная функция программы."""
    if len(sys.argv) < 2:
        print(
            "В качестве аргументов указывается последовательность чисел, "
            "задающих границы возрастных групп."
        )
        print("Пример: ./src/lab4/task2.py 18 25 35 45 60 80 100")
        sys.exit(1)

    try:
        limits = [int(arg) for arg in sys.argv[1:]]

        if limits != sorted(limits):
            print("Предупреждение: границы были автоматически отсортированы")
            limits.sort()

        if any(b <= 0 for b in limits):
            print("Ошибка: границы возрастных групп должны быть положительными числами")
            sys.exit(1)

    except ValueError:
        print("Ошибка: все границы возрастных групп должны быть целыми числами")
        sys.exit(1)

    manager = AgeGroupManager(limits)

    respondents = read_respondents()

    for name, age in respondents:
        manager.add_respondent(name, age)

    print("\nРезультат группировки:")

    non_empty_groups = manager.get_non_empty_groups()

    if not non_empty_groups:
        print("Нет респондентов для отображения")
    else:
        for group in non_empty_groups:
            print(group)


if __name__ == "__main__":
    main()
