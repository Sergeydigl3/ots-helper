from dataclasses import dataclass

# Порождающий полином p(x) = x^3 + x^2 + 1 в двоичном виде: 0b1011
# POLY = 0b1101   
POLY = 0b1011   

GF_SIZE_INIT = 3
GF_size = 2**GF_SIZE_INIT
GF_mask = (1 << GF_SIZE_INIT) - 1

# Функция для умножения на x (сдвиг влево) с учетом порождающего полинома
def multiply_by_x(value):
    result = value << 1  # Умножение на x (сдвиг влево)
    if result & (1 << GF_SIZE_INIT):  # Если результат сдвига имеет старший бит (старше x^GF_SIZE_INIT)
        result ^= POLY  # Применяем XOR с порождающим полиномом
    return result & GF_mask  # Ограничиваем результат до GF_SIZE_INIT бит

# Функция для преобразования числа в полиномиальное представление
def to_polynomial(value):
    binary_repr = bin(value)[2:]  # Преобразование в двоичную строку
    terms = []
    for i, bit in enumerate(binary_repr):  # Итерируем от старшего бита к младшему
        if bit == '1':
            power = len(binary_repr) - i - 1  # Степень, начиная с самой старшей
            str_append = f"x^{power}" if power > 0 else "1"
            if power == 1: str_append = "x"
            terms.append(str_append)
    return " + ".join(terms) if terms else "0"

def show_bin(value: int):
    return bin(value)[2:].zfill(GF_SIZE_INIT)


print(f"Исходное полином: {to_polynomial(POLY)}")

@dataclass
class TableElement:
    degree_repr: int
    value: int
    bin_repr: str


table: list[TableElement] = []

table.append(TableElement(0, 0, show_bin(0)))
table.append(TableElement(1, 1, show_bin(1)))
for i in range(GF_size - 2):
    value = multiply_by_x(table[-1].value)
    degree_repr = table[-1].degree_repr << 1
    added = TableElement(degree_repr,value, show_bin(value))
    table.append(added)

# Вывод таблицы с измененным порядком столбцов
print("\nТаблица значений:")
print("Степенное представление | Полиномическое представление | Двоичное представление | Десятичное значение")
print("-" * 55)
for el in table:
    print(f"{to_polynomial(el.degree_repr):<30} | {to_polynomial(el.value):<30} | {el.bin_repr} | {el.value}")
    

# Инициализация таблиц для exp(k) и log(a)
exp_table = [0] * GF_size
log_table = [None] * GF_size

# Построение exp(k) и log(a)
# exp(k) - значение из таблицы, где degree_repr = x^k
# log(a) - обратный индекс для exp(k)
for k in range(GF_size - 1):
    # Найти элемент в первой таблице, где степень соответствует x^k
    element = next((el for el in table if el.degree_repr == (1 << k)), None)
    if element:
        exp_table[k] = element.value  # exp(k) = значение элемента
        log_table[element.value] = k  # log(value) = k

# Вывод таблицы

print("\nТаблица экспоненциального и логарифмического представления:")
print("k   | Exp(k)   | a   | Log(a)")
print("-" * 30)
for k in range(GF_size):
    exp_val = exp_table[k] if k < GF_size - 1 else 1  # exp(k), при k >= GF_size-1 exp(k) = 1
    log_val = log_table[k] if k < GF_size and log_table[k] is not None else "-Inf"  # log(a)
    print(f"{k:<4} | {exp_val:<8} | {k:<3} | {log_val}")
 
clear_array = [i.value for i in table][1:]
print(f"Clear array: {clear_array}")
