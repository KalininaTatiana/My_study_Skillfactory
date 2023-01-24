# найти первое отрицательное число, не хранящееся в кеше
a = 0
b = 0

while id(a) == id(b):
    a -= 1
    b -= 1

print(a)

print("")

text = input("Введите текст:")
unique = set(text)
print("Количество уникальных символов: ", len(unique))

def linear_solve(a, b):
    return b / a
print(linear_solve(2, 9))
print(linear_solve(0, 1))