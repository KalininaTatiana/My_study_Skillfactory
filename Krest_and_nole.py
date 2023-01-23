person1 = input("Введите имя первого игрока:")
person2 = input("Введите имя второго игрока:")
print(f"Приветствую, {person1} и {person2}! Приятной игры!")

board = list(range(1, 10))

wins_coord = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)]


def draw_board():
    print('-------------')
    for i in range(3):
        print('|', board[0 + i * 3], '|', board[1 + i * 3], '|', board[2 + i * 3], '|')
    print('-------------')


def take_input(player_token):
    while True:
        value = input('Куда поставить: ' + player_token + ' ?')
        if value not in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
            print('Ошибочный код, повторите ввод')
            continue
        value = int(value)
        if str(board[value - 1]) in 'X0':
            print('Эта клетка занята')
            continue
        board[value - 1] = player_token
        break


def check_win():
    for each in wins_coord:
        if board[each[0] - 1] == "X" and board[each[1] - 1] == "X" and board[each[2] - 1] == "X":
            return person1
        if board[each[0] - 1] == "0" and board[each[1] - 1] == "0" and board[each[2] - 1] == "0":
            return person2


def main():
    counter = 0
    while True:
        draw_board()
        if counter % 2 == 0:
            take_input('X')
        else:
            take_input('0')
        if counter > 3:
            winner = check_win()
            if winner:
                draw_board()
                print(f'Поздравляю, {winner}, это победа!')
                break
        counter += 1
        if counter > 8:
            draw_board()
            print('Увы, ничья =(')
            break

main()
