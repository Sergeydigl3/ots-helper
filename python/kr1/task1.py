import numpy as np
from itertools import product

def build_generator_matrix(H):
    """
    Построение порождающей матрицы G на основе проверочной матрицы H.
    """
    m, n = H.shape  # Размерности матрицы H
    k = n - m       # Количество информационных символов

    # Проверяем, можно ли представить H как [P^T | I_m]
    P_T = H[:, :k]  # Левая часть H (P транспонированное)
    I_m = H[:, k:]  # Правая часть H (должна быть I_m)

    if not np.array_equal(I_m, np.eye(m, dtype=int)):
        raise ValueError("Матрица H не находится в систематическом виде!")

    # Строим G как [I_k | P]
    I_k = np.eye(k, dtype=int)
    G = np.hstack((I_k, P_T.T))

    return G, k, n

def generate_codewords(G):
    """
    Генерация всех кодовых слов на основе порождающей матрицы G.
    """
    k = G.shape[0]  # Количество информационных символов
    codewords = []

    # Перебор всех возможных информационных векторов
    for message in product([0, 1], repeat=k):
        message = np.array(message)
        codeword = (message @ G) % 2  # Умножение и приведение по модулю 2
        codewords.append(codeword)

    return codewords

def hamming_distance(vec1, vec2):
    """
    Подсчет расстояния Хэмминга между двумя векторами.
    """
    return np.sum(vec1 != vec2)

def minimal_distance(codewords):
    """
    Нахождение минимального расстояния Хэмминга среди всех пар кодовых слов.
    """
    d_min = float('inf')
    for i in range(len(codewords)):
        for j in range(i + 1, len(codewords)):
            d = hamming_distance(codewords[i], codewords[j])
            if d > 0:  # Игнорируем сравнение слова с самим собой
                d_min = min(d_min, d)
    return d_min

def main():
    # Ввод проверочной матрицы H
    print("Введите проверочную матрицу H построчно (элементы через пробел, пустая строка для завершения ввода):")
    rows = []
    while True:
        line = input()
        if line.strip() == "":
            break
        rows.append(list(map(int, line.strip().split())))
    H = np.array(rows)

    print("\nПроверочная матрица H:")
    print(H)

    try:
        # Построение порождающей матрицы G
        G, k, n = build_generator_matrix(H)
        print("\nПорождающая матрица G:")
        print(G)

        # Параметры кода
        M = 2**k  # Количество кодовых слов
        R = k / n  # Скорость кода

        # Генерация кодовых слов
        codewords = generate_codewords(G)
        d_min = minimal_distance(codewords)

        # Вывод параметров кода
        print(f"\nПараметры кода:")
        print(f"Длина кода (N): {n}")
        print(f"Количество информационных символов (k): {k}")
        print(f"Количество кодовых слов (M): {M}")
        print(f"Скорость кода (R): {R:.3f}")
        print(f"Минимальное расстояние кода (d): {d_min}")

    except ValueError as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
