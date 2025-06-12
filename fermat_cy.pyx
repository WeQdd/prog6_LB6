import math

def fermat_factorization_cy(object number, object max_iterations):
    """Реализация алгоритма факторизации Ферма в Cython"""
    # Проверяем, является ли число четным
    if number % 2 == 0:
        return 2, number // 2

    # Находим начальное значение для перебора - целую часть корня из N плюс 1
    start_value = math.isqrt(number) + 1
    iteration_count = 0
    
    # Ищем такое значение x, что x^2 - N является точным квадратом
    while iteration_count < max_iterations:
        square_diff = start_value * start_value - number
        if square_diff >= 0:
            root = math.isqrt(square_diff)
            # Проверяем, получили ли мы точный квадрат
            if root * root == square_diff:
                # Возвращаем найденные множители
                return (start_value - root, start_value + root)
        start_value += 1
        iteration_count += 1
    return None  # Не удалось найти разложение за указанное число итераций
