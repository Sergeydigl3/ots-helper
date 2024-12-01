# task3
# Таблицы для GF(2^4)
exp_table = [1, 2, 4, 8, 3, 6, 12, 11, 5, 10, 7, 14, 15, 13, 9, 1]
log_table = [0, 0, 1, 4, 2, 8, 5, 10, 3, 14, 9, 7, 6, 13, 11, 12]


def gf_add(a, b):
    """Сложение в GF(2^4) эквивалентно XOR"""
    return a ^ b


def gf_mul(a, b):
    """Умножение в GF(2^4) с использованием таблиц логарифмов и экспонент"""
    if a == 0 or b == 0:
        return 0
    return exp_table[(log_table[a] + log_table[b]) % 15]


def gf_div(a, b):
    """Деление в GF(2^4) с использованием таблиц логарифмов и экспонент"""
    if a == 0:
        return 0
    if b == 0:
        raise ZeroDivisionError("Division by zero in GF(2^4)")
    return exp_table[(log_table[a] - log_table[b]) % 15]


# Принятая последовательность
# v = [0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0]
# v = [0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0]
v = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1]


def calculate_syndromes(v):
    """Вычисление синдромов S1, S2, S3, S4"""
    syndromes = []
    print("\n1) Вычисление синдромов:")
    for i in range(1, 5):
        s = 0
        terms = []
        for j in range(len(v)):
            if v[j] != 0:
                term = gf_mul(v[j], exp_table[(i * j) % 15])
                terms.append(f"a^{(i * j) % 15}")
                s = gf_add(s, term)
        syndrome_exp = f"a^{log_table[s]}" if s != 0 else "0"
        print(f"S{i} = v(a^{i}) = {' + '.join(terms)} = {syndrome_exp}")
        syndromes.append(s)
    return syndromes


def berlekamp_massey(syndromes):
    """Алгоритм Берлекэмпа-Месси для нахождения локатора ошибок"""
    print("\n2) Многочлен локаторов ошибок:")
    n = len(syndromes)
    λ = [1]
    B = [1]
    L = 0
    m = 1
    b = 1

    for i in range(n):
        discr = syndromes[i]
        discr_terms = []
        for j in range(1, L + 1):
            term = gf_mul(λ[j], syndromes[i - j])
            discr = gf_add(discr, term)
            discr_terms.append(f"λ{j}*S{i-j+1}")
        discr_exp = f"a^{log_table[discr]}" if discr != 0 else "0"
        # print(f"Δ{i+1} = S{i+1} + {' + '.join(discr_terms)} = {discr_exp}")

        if discr == 0:
            m += 1
        else:
            T = λ[:]
            factor = gf_div(discr, b)
            # print(f"Обновление: factor = Δ{i+1} / b = {discr_exp} / a^{log_table[b]} = a^{log_table[factor]}")
            for j in range(len(B)):
                if j + m < len(λ):
                    λ[j + m] = gf_add(λ[j + m], gf_mul(factor, B[j]))
                else:
                    λ.append(gf_mul(factor, B[j]))

            if 2 * L <= i:
                L = i + 1 - L
                B = T
                b = discr
                m = 1
            else:
                m += 1

    for i, coef in enumerate(λ):
        coef_exp = f"a^{log_table[coef]}" if coef != 0 else "0"
        print(f"λ{i} = {coef:04b} = {coef_exp}")
    return λ


def find_error_positions(λ: list[int]):
    """Нахождение позиций ошибок по корням локатора ошибок с учетом работы в поле GF(2^4)"""
    print("\n3) Проверка корней многочлена λ(x):")
    positions = []

    # Нужно получить вот такую строку как ниже
    # Там должно быть λ(x) = 1 + λ1 * x + λ2 * x^2  = 1 + a^1 * x + a^10 * x^2
    str_elements: list[str] = []
    str_result = "1"  # Многочлен всегда начинается с единицы (λ0 = 1)
    for i in range(1, len(λ)):
        if λ[i] != 0:
            λ_exp = f"a^{log_table[λ[i]]}" if λ[i] != 1 else "1"
            x_str = f"x^{i}"
            if i == 1:
                x_str = "x"
            str_elements.append(f"{λ_exp} * {x_str}")
    str_result += " + " + " + ".join(str_elements)
    print(f"λ(x) = 1 + λ1 * x + λ2 * x^2 = {str_result}")
    for i in range(15):
        x = exp_table[i]
        result = 0
        terms = []
        detailed_terms = []
        for j in range(len(λ)):
            term = gf_mul(λ[j], exp_table[(i * j) % 15])
            result = gf_add(result, term)
            terms.append(f"λ{j}*a^{(i*j)%15}")
            if λ[j] != 0:
                λ_exp = f"a^{(log_table[λ[j]] + (i*j) % 15) % 15}" if λ[j] != 1 else "1"
                detailed_terms.append(f"{λ_exp}")
            else:
                detailed_terms.append("0")
        result_exp = f"a^{log_table[result]}" if result != 0 else "0"
        print(
            f"λ(a^{i}) = {' + '.join(terms)} = {' + '.join(detailed_terms)} = {result_exp}"
        )
        if result == 0:
            print(f"Корень найден: r = a^{i}")
            positions.append(exp_table[(15 - i) % 15])
            if len(positions) == 2:
                print("Два корня найдены. Все что ниже писать не нужно!!!")
    return positions


def find_roots_from_locators(locators):
    """Вычисление корней как обратных элементов локаторов"""
    roots = [gf_div(1, loc) for loc in locators]
    return roots


def main():
    print("1) Принятая последовательность v(x):")
    print("v(x) =", "".join(map(str, v)))

    syndromes = calculate_syndromes(v)

    λ = berlekamp_massey(syndromes)

    error_locators = find_error_positions(λ)

    error_roots = find_roots_from_locators(error_locators)
    print("\n3) Корни многочлена Lambda(x):")
    for i, root in enumerate(error_roots):
        print(f"r{i+1} = {root:04b} = a^{log_table[root]}")

    print("\n4) Локаторы ошибок:")
    for i, loc in enumerate(error_locators):
        print(f"X{i+1} = {loc:04b} = a^{log_table[loc]}")

    error_positions = [log_table[x] for x in error_locators]
    print("\n5) Позиции ошибок:")
    for i, pos in enumerate(error_positions):
        print(f"i{i+1} = Log(X{i+1}) = {pos}")


# Запускаем программу
main()
