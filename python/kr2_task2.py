def binchiling(x):
    return bin(x)[2:].zfill(3)

def find_in_table(x, curr_table):
    for i in range(len(curr_table)):
        if curr_table[i] == x:
            return i
    return -1

def gf_mult(a, b, mod_poly):
    """
    Умножение в поле GF(2^3).
    a, b: множители в двоичном представлении.
    mod_poly: модуль в двоичном представлении.
    """
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 0b1000:  # Проверка переполнения степени. (нахардкодили говна)
            a ^= mod_poly
    return result

def koroche_lambda(x, mod_poly, lambda_coeffs, ind, full_table):
    # Коэффициенты многочлена Lambda(x)
    gf_mult_res = []
    tmp_x = 1
    pred_res=[]
    machine_res=[]
    print(f"--------------- x = a^{ind} --------------")
    for i in range(len(lambda_coeffs)):
        pow1 = find_in_table(tmp_x, full_table)
        pow2 = find_in_table(lambda_coeffs[i], full_table)
        tmp_res = gf_mult(tmp_x, lambda_coeffs[i], mod_poly)
        tmp_str = f"x^{i} = a^{pow1} * a^{pow2} = a^{find_in_table(tmp_res, full_table)}"
        tmp_str += f" || {binchiling(tmp_x)} * {binchiling(lambda_coeffs[i])} = 0b{binchiling(tmp_res)}"
        print(tmp_str)
        gf_mult_res.append(tmp_res)
        tmp_x = gf_mult(tmp_x, x, mod_poly)
        
        tmp_arr: list[str] = []
        tmp_machine: list[str] = []
        if pow1 != 0:
            tmp_arr.append(f"a^{pow1}")
            tmp_machine.append(f"{binchiling(tmp_x)}")
        if pow2 != 0:
            tmp_arr.append(f"a^{pow2}")
            tmp_machine.append(f"{binchiling(lambda_coeffs[i])}")
        tmp_prod = " * ".join(tmp_arr)
        tmp_prod_machine = " * ".join(tmp_machine)
        if "*" in tmp_prod:
            tmp_prod = f"({tmp_prod})"
            tmp_prod_machine = f"({tmp_prod_machine})"
            
        pred_res.append(tmp_prod)
        machine_res.append(tmp_prod_machine)


    result = 0
    for i in range(len(gf_mult_res)):
        result ^= gf_mult_res[i]

    print(f"Bin res: 0b{binchiling(result)}")
    
    pred_res = reversed(pred_res)
    machine_res = reversed(machine_res)
    tmp_prod = " + ".join(pred_res)
    tmp_prod_machine = " + ".join(machine_res)
    print(f"λ(a^{ind}) = {tmp_prod} = {tmp_prod_machine} = {binchiling(result)}")
    return result

def find_roots(table, mod_poly, lambda_coeffs):
    roots = []
    for x in range(0, 7):  # Перебираем элементы GF(2^3), кроме 0.
        element = table[x]
        result = koroche_lambda(element, mod_poly, lambda_coeffs, x, table)
        if result == 0:
            roots.append(x)

    return roots

def main():
    # Модульное поле GF(2^3) задано многочленом p(x) = x^3 + x^2 + 1
    mod_poly = 0b1101
    # Таблица от 1 до a^6
    table = [1, 2, 4, 5, 7, 3, 6, 0]
    #table = [1, 2, 4, 3, 6, 7, 5, 0]
    # Lambda(x) = x^3 + (a^6)*x^2 + x + a^3
    # Коэффициенты многочлена Lambda(x)
    lambda_coef_indexes = [3, 0, 6, 0]

    lambda_coeffs = []
    for i in range(len(lambda_coef_indexes)):
        lambda_coeffs.append(table[lambda_coef_indexes[i]])

    roots = find_roots(table, mod_poly, lambda_coeffs)
    powers = []
    for i in range(len(table)):
        powers.append(f"a^{i}")

    print("Корни многочлена Lambda(x):", [powers[root] for root in roots])

if __name__ == "__main__":
    main()
