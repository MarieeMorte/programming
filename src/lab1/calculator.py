import re

def tokenize(expr):
    token_pattern = r'\d+\.\d+|\d+|//|\*\*|[%+\-*/()]'
    return re.findall(token_pattern, expr)

def check_sequence(tokens):
    operators = {'+', '-', '*', '/', '//', '%', '**'}
    prev = None
    for i, token in enumerate(tokens):
        if token in operators:
            if prev in operators or prev is None:
                if token == '-' and (i + 1 < len(tokens)) and (tokens[i+1].isdigit() or tokens[i+1] == '('):
                    continue
                else:
                    raise ValueError("Ошибка: некорректная последовательность операторов")
        prev = token

def main():
    print("Добро пожаловать в упрощённый консольный калькулятор!")
    print("Поддерживаются операции: +, -, *, /, //, %, ** и скобки.")
    print("Введите выражение и нажмите Enter. Для выхода введите 'exit'.\n")

    while True:
        expr = input("Введите выражение: ").strip()
        if expr.lower() == 'exit':
            print("До свидания!")
            break
        if not expr:
            print("Пустой ввод. Попробуйте ещё раз.\n")
            continue

        if not re.fullmatch(r'[\d\s+\-*/%().]+', expr):
            print("Ошибка ввода: запрещённые символы.\n")
            continue

        tokens = tokenize(expr)
        try:
            check_sequence(tokens)
        except ValueError as ve:
            print(str(ve) + "\n")
            continue

        if re.search(r'[*/%+\-]\s*-\s*\d', expr):
            print("Ошибка: отрицательные числа в бинарных операциях должны быть в скобках, если не стоят на первой позиции, например, 3 * (-5).\n")
            continue

        try:
            result = eval(expr)
        except ZeroDivisionError:
            print("Ошибка: деление на ноль запрещено.\n")
            continue
        except Exception:
            print("Ошибка ввода: синтаксическая ошибка в выражении.\n")
            continue

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        print("Результат:", result, "\n")

if __name__ == "__main__":
    main()
