from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):            # Проверка равенства точек
        return self.x == other.x and self.y == other.y

    def __repr__(self):                 # Вывод точек в консоль, проверка, есть ли точка в списке
        return f"({self.x}, {self.y})"


class BoardException(Exception):        # Создаем собственные классы исключений (общий)
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):      # Исключение, чтобы размещать корабли, не для пользователя
    pass


class Ship:
    def __init__(self, bow, l, o):      # нос, длина корабля, ориентация(гориз-верт)
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):  # Проверка на попадание
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):      # hid - нужно ли скрывать наше поле? + размер
        self.size = size
        self.hid = hid

        self.count = 0      # количество пораженных кораблей

        self.field = [["O"] * size for _ in range(size)]  # клетка, в которой будут храниться состояния, 0 - клетка не занята

        self.busy = []      # занятые точки. Либо кораблем, либо промахи
        self.ships = []     # список кораблей доски. Пока пустой, потом добавлять с помощью метода add

    def add_ship(self, ship):       # Размещение корабля

        for d in ship.dots:
            if self.out(d) or d in self.busy:  # проверка, что точка не выходит за границы и не занята
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)     # добавить точку в список занятых

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):        # контур корабля, verb - нужно ли ставить точки вокруг кораблей?
        near = [                                # в этом списке все точки вокруг той, в которой находимся
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:         # Проверка всех точек по соседству с кораблем
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."  # показываем, что точка занята
                    self.busy.append(cur)               # добавить точку в список занятых

    def __str__(self):          # вывод корабля на доску
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"     # номер строки, затем клетки строки

        if self.hid:        # нужно ли скрывать корабли?
            res = res.replace("■", "O")  # меняем корабли на пустые символы
        return res

    def out(self, d):       # находится ли точка за пределами доски?
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):      # стрельба по доске
        if self.out(d):     # выходит ли точка за границы? Иначе исключение
            raise BoardOutException()

        if d in self.busy:  # занята ли точка? иначе исключение
            raise BoardUsedException()

        self.busy.append(d)  # делаем точку занятой, если она такой не была

        for ship in self.ships:      # здесь вызов метода shooten
            if ship.shooten(d):
                ship.lives -= 1      # если подстрелен, вычитаем количество жизней и ставим Х
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:     # если кончились жизни, сначала прибавляем к счетчику уничтоженных кораблей 1
                    self.count += 1
                    self.contour(ship, verb=True)   # обозначаем точками контур корабля (True)
                    print("Корабль уничтожен!")
                    return False        # дальше ход не нужно делать
                else:
                    print("Корабль ранен!")
                    return True         # нужно повторить ход

        self.field[d.x][d.y] = "."      # если ни один корабль не был поражен
        print("Мимо!")
        return False

    def begin(self):        # Важно, чтобы при начале игры список бизи обнулился, теперь тут также хранятся точки, куда стрелял игрок
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):      # Метод не определяем, он должен быть у потомков класса
        raise NotImplementedError()

    def move(self):     # пытаемся сделать выстрел
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target) # если выстрел успешен, возвращаем повторить его
                return repeat
            except BoardException as e:     # если выстрел  прошел плохо, вызываем соотв исключение
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))   # генератор случайных точек для ИИ
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()  # Запрос координат

            if len(cords) != 2:     # проверка, что введено две координаты
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):      # проверка, что это числа
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)    # вернем числа (у нас индексация с 0, а у пользователя с 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()        # генератор доски для игрока
        co = self.random_board()        # генератор доски для компьютера
        co.hid = True                   # для компьютера корабли скрыты (параметр хид)

        self.ai = AI(co, pl)        # создаем двух игроков
        self.us = User(pl, co)

    def random_board(self):     # Гарантированно создает доску со случайными кораблями
        board = None
        while board is None:
            board = self.try_board()
        return board

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]        # список с длинами кораблей
        board = Board(size=self.size)       # создаем доску
        attempts = 0                # количество попыток, счетчик
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):     # Игровой цикл
        num = 0         # Номер хода
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)        # Вывод досок пользователя и компьютера
            if num % 2 == 0:            # Если номер хода четный - пользователь, нечетный - компьютер
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:      # Если кораблю поражен, можно повторить ход
                num -= 1

            if self.ai.board.count == len(self.ai.board.ships):
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == len(self.us.board.ships):
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):        # Метод, который все это совмещает
        self.greet()
        self.loop()


g = Game()
g.start()
