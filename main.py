import math
import timeit
import matplotlib.pyplot as plt


"""
Время вычислений (Baseline)  = 229.25 секунд
Шаг 1. Оставив представленный ниже код, переписать функции для нахождения чисел с помощью Cython, 
запустить timeit с аналогичными параметрами и сравнить два варианта, построить график.
С помощью annotate=True сгенерируйте html (где визуализировано взаимодействие с Python-интерпретатором) и приложите его к отчету. 
"""

"""
Шаг 2. Создать механизм распределения вычислений так, чтобы массив данных для вычисления распределялся
на несколько "вычислителей" и каждый вычислитель считал свое /map-reduce
1. Определить параметры: количество вычислителей, их тип (поток, процесс) и распределить по
 соответствующим очередям какие значения какому вычислителю идут. 
2. Отправить по очереди значения и дождаться пока все вычислители закончат работу
3. Оценить работу программы с потоками и процессами
Отобразить результаты вычислений в виде графиков и нанести на график время вычисления с помощью потоков и в процессов двух 
реализаций функции по разложению числа на множители Cython-реализацию и обычную (расположенную в файле ferma_fact.py)
Шаг 3. Работа с GIL
Перепишите многопоточное решение, но при реализации многопоточности убедитесь, 
что вы используете контекстный менеджер with nogil в Cython для освобождения GIL во время выполнения ресурсоёмких операций.
GIL — это механизм, который предотвращает одновременное выполнение нескольких потоков Python. 
Это может быть проблемой для многопоточных программ, выполняющих ресурсоёмкие операции.
При написании Cython-кода вы можете использовать конструкцию with nogil, чтобы освободить GIL
во время выполнения длительных операций. Это позволяет другим потокам продолжать выполнение.
Посмотрите соответствующий конспект лекций и код там. 
"""


def is_perfect_square(n):
    """Проверяет, является ли число полным квадратом."""
    if n < 0:
        return False
    root = int(math.isqrt(n))
    return root * root == n


def fermat_factorization(N, max_iter=10**7):
    """Разложение числа N на множители методом Ферма."""
    if N % 2 == 0:
        return 2, N // 2  # Если N четное, делим на 2

    x = math.isqrt(N) + 1  # Начинаем с ближайшего целого числа к √N
    count = 0
    while count < max_iter:
        y_squared = x * x - N
        if is_perfect_square(y_squared):
            y = int(math.isqrt(y_squared))
            return (x - y, x + y)  # Возвращаем найденные множители
        x += 1 # Увеличиваем x
        count += 1
    return None  


# Пример использования
if __name__ == '__main__':
    
        # TEST_LST = [101, 9973, 104729, 101909, 609133, 1300039, 9999991, 99999959, 99999971, 3000009, 700000133,
    #             61335395416403926747]
    #
    # res = [fermat_factorization(i) for i in TEST_LST]
    # print(res)

    # Набор тестовых чисел различной сложности для факторизации
    TEST_LST = [101, 9973, 104729, 101909, 609133, 1300039, 9999991, 99999959, 99999971, 3000009, 700000133,
                61335395416403926747]

    # Измерение времени выполнения Python-версии
    py_time = timeit.repeat(
        "res = [fermat_factorization(i) for i in TEST_LST]",
        number=10, repeat=1, globals=globals()
    )
    print("Время Python:", py_time)

    # Измерение времени выполнения Cython-версии
    cy_time = None
    try:
        from fermat_cy import fermat_factorization_cy
        
        _MAX_ITER_VALUE = 10**7  # Максимальное число итераций

        stmt_for_cython = "res = [fermat_factorization_cy(i, _MAX_ITER_VALUE) for i in TEST_LST]"
        
        cy_globals = {
            'fermat_factorization_cy': fermat_factorization_cy,
            'TEST_LST': TEST_LST,
            '_MAX_ITER_VALUE': _MAX_ITER_VALUE
        }

        cy_time = timeit.repeat(
            stmt_for_cython,
            number=10, 
            repeat=1, 
            globals=cy_globals
        )
        print("Время Cython:", cy_time)
    except ImportError:
        print("Ошибка: модуль Cython не скомпилирован. Выполните команду: python setup.py build_ext --inplace")

    # Визуализация результатов сравнения
    try:
        if cy_time is not None:
            plt.bar(['Python', 'Cython'], [py_time[0], cy_time[0]])
            plt.ylabel('Время выполнения (сек)')
            plt.title('Сравнение производительности: Python vs Cython')
            plt.show()
        else:
            print("График не построен: результаты Cython недоступны")
    except Exception as e:
        print("Ошибка построения графика:", e)