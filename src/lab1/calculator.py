"""
Модуль calculator.py
Простой консольный калькулятор с проверкой операторов и отрицательных чисел.
"""

import re


def tokenize(expr):
    """
    Разбивает строковое выражение на отдельные токены.

    Токены могут быть числами (целыми или дробными), операторами
    (+, -, *, /, //, %, **) или скобками '(' и ')'.

    Args:
        expr (str): Строка с арифметическим выражением.

    Returns:
        list[str]: Список токенов в порядке появления в выражении.

    Raises:
        None
    """
    token_pattern = r"\d+\.\d+|\d+|//|\*\*|[%+\-*/()]"
    return re.findall(token_pattern, expr)


def check_sequence(tokens):
    """
    Проверяет корректность последовательности операторов в списке токенов.

    Основные правила:
    - Два бинарных оператора подряд запрещены.
    - Бинарный оператор не может стоять первым, кроме унарного минуса.
    - Унарный минус разрешён только перед числом или скобкой.

    Args:
        tokens (list[str]): Список токенов арифметического выражения.

    Raises:
        ValueError: Если найдена некорректная последовательность операторов.
    """
    operators = {"+", "-", "*", "/", "//", "%", "**"}
    prev = None
    for i, token in enumerate(tokens):
        if token in operators:
            if prev in operators or prev is None:
                if (token == "-"
                        and (i + 1 < len(tokens))
                        and (tokens[i + 1].isdigit() or tokens[i + 1] == "(")):
                    continue
                raise ValueError("Ошибка: некорректная последовательность операторов")
        prev = token


def main():
    """
    Основная функция консольного калькулятора.

    Поведение:
    - Выводит приветствие и инструкции.
    - Читает выражения пользователя с клавиатуры.
    - Проверяет разрешённые символы и последовательность операторов.
    - Проверяет отрицательные числа в бинарных операциях (должны быть в скобках).
    - Вычисляет результат с помощью eval().
    - Обрабатывает ошибки деления на ноль и синтаксические ошибки.
    - Выводит результат или сообщение об ошибке.
    - Выход из программы по вводу 'exit'.

    Returns:
        None
    """
    print("Добро пожаловать в упрощённый консольный калькулятор!")
    print("Поддерживаются операции: +, -, *, /, //, %, ** и скобки.")
    print("Введите выражение и нажмите Enter. Для выхода введите 'exit'.\n")

    while True:
        expr = input("Введите выражение: ").strip()
        if expr.lower() == "exit":
            print("До свидания!")
            break
        if not expr:
            print("Пустой ввод. Попробуйте ещё раз.\n")
            continue

        if not re.fullmatch(r"[\d\s+\-*/%().]+", expr):
            print("Ошибка ввода: запрещённые символы.\n")
            continue

        tokens = tokenize(expr)
        try:
            check_sequence(tokens)
        except ValueError as error:
            print(str(error) + "\n")
            continue

        if re.search(r"[*/%+\-]\s*-\s*\d", expr):
            print(
                "Ошибка: отрицательные числа в бинарных операциях должны быть в скобках,"
                " если не стоят на первой позиции, например, 3 * (-5).\n"
            )
            continue

        try:
            result = eval(expr)  # pylint: disable=eval-used
        except ZeroDivisionError:
            print("Ошибка: деление на ноль запрещено.\n")
            continue
        except SyntaxError:
            print("Ошибка ввода: синтаксическая ошибка в выражении.\n")
            continue
        except NameError:
            print("Ошибка ввода: запрещённые символы или идентификаторы.\n")
            continue

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        print("Результат:", result, "\n")


if __name__ == "__main__":
    main()
