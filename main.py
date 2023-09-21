from random import randrange
from time import sleep


class GameMechanics(Exception):
    pass


class BoardOutException(GameMechanics):
    pass


class CellOccupied(GameMechanics):
    pass


class InputError(GameMechanics):
    pass


class DontShootTwice(GameMechanics):
    pass


class FailBoard(GameMechanics):
    pass


class Ship:
    def __init__(self, len, nose = None,  direction = None):
        self.len = len
        self.nose = nose
        self.direction = direction

    def get_ship(self):
        ship = [self.nose]
        if self.len == 1:
            return ship
        elif self.len == 2:
            if self.direction == "vertical":
                ship += [[self.nose[0] + 1, self.nose[1]]]
            elif self.direction == "horizontal":
                ship += [[self.nose[0], self.nose[1] + 1]]
        else:
            for i in range(1, 3):
                if self.direction == "vertical":
                    ship += [[self.nose[0] + i, self.nose[1]]]
                elif self.direction == "horizontal":
                    ship += [[self.nose[0], self.nose[1] + i]]
        return ship

    def get_len(self):
        return self.len

    def set_ship(self, ban_list):
        x = int(input("Введите координату носа по х: "))
        y = int(input("Введите координату носа по y: "))
        if 0 < x <= 6 and 0 < y <= 6:
            pass
        else:
            raise BoardOutException
        if [x, y] in ban_list:
            raise CellOccupied
        else:
            self.nose = [x, y]
        if self.len == 3:
            self.direction = str(input("Введите направление корабля vertical или horizontal: "))
            if self.direction == "horizontal":
                if [x, y + 1] not in ban_list and [x, y + 2] not in ban_list:
                    if y + 1 < 7 and y + 2 < 7:
                        ban_list += [x,y],[x+1,y],[x,y+1],[x+1,y+1],[x-1,y],[x,y-1],[x-1,y-1],[x-1,y+1],[x+1,y-1],[x,y+2],[x-1,y+2],[x+1,y+2],[x+1,y+3],[x,y+3],[x-1,y+3]
                    else:
                        raise BoardOutException
                else:
                    raise CellOccupied
            elif self.direction == "vertical":
                if [x + 1, y] not in ban_list and [x + 2, y] not in ban_list:
                    if x + 1 < 7 and x + 2 < 7:
                        ban_list += [x,y],[x+1,y],[x,y+1],[x+1,y+1],[x-1,y],[x,y-1],[x-1,y-1],[x-1,y+1],[x+1,y-1],[x+2,y],[x+2,y+1],[x+2,y-1],[x+3,y],[x+3,y+1],[x+3,y-1]
                    else:
                        raise BoardOutException
                else:
                    raise CellOccupied
            else:
                raise InputError
        elif self.len == 2:
            self.direction = str(input("Введите направление корабля vertical или horizontal: "))
            if self.direction == "horizontal":
                if [x, y + 1] not in ban_list:
                    if y + 1 < 7:
                        ban_list +=[x,y],[x+1,y],[x,y+1],[x+1,y+1],[x-1,y],[x,y-1],[x-1,y-1],[x-1,y+1],[x+1,y-1],[x,y+2],[x-1,y+2],[x+1,y+2]
                    else:
                        raise BoardOutException
                else:
                    raise CellOccupied
            elif self.direction == "vertical":
                if [x + 1, y] not in ban_list:
                    if x + 1 < 7:
                        ban_list += [x,y],[x+1,y],[x,y+1],[x+1,y+1],[x-1,y],[x,y-1],[x-1,y-1],[x-1,y+1],[x+1,y-1],[x+2,y],[x+2,y+1],[x+2,y-1]
                    else:
                        raise BoardOutException
                else:
                    raise CellOccupied
            else:
                raise InputError
        else:
            ban_list += [x,y],[x+1,y],[x,y+1],[x+1,y+1],[x-1,y],[x,y-1],[x-1,y-1],[x-1,y+1],[x+1,y-1]



class Board:
    def __init__(self, hid, board = None, ship_list = []):
        self.board = [["O"] * 6 for _ in range(6)]
        self.ship_list = ship_list
        self.hid = hid

    def import_list(self, list):
        self.ship_list = list


    def print_board(self):
        if self.hid == False:
            print(' |1|2|3|4|5|6|')
            for i in range(6):
                print(f"{i + 1}|", end='')
                for j in range(6):
                    print(f"{self.board[i][j]}|", end='')
                print()
        else:
            print(' |1|2|3|4|5|6|')
            for i in range(6):
                print(f"{i + 1}|", end='')
                for j in range(6):
                    if self.board[i][j] == '■':
                        print(f"O|", end='')
                    else:
                        print(f"{self.board[i][j]}|", end='')
                print()
    def add_ship(self, pos, size):
        if size == 1:
            self.board[pos[0][0] - 1][pos[0][1] - 1] = "■"
            self.ship_list += pos
        elif size == 2:
            for i in range(2):
                self.board[pos[i][0] - 1][pos[i][1] - 1] = "■"
            self.ship_list += pos
        else:
            for i in range(3):
                self.board[pos[i][0] - 1][pos[i][1] - 1] = "■"
            self.ship_list += pos

    def get_ship_list(self):
        return self.ship_list

    def living_ships(self):
        counter = 0
        for i in self.ship_list:
            if self.board[i[0] - 1][i[1] - 1] == "■":
                counter += 1
        if counter == 0:
            return False
        else:
            return True

    def shot(self, dot, shot_list):

        if dot not in shot_list:
            hit = False
            if self.board[dot[0] - 1][dot[1] - 1] == "■":
                sleep(0.5)
                print("Попал")
                sleep(1)
                hit = True
                self.board[dot[0] - 1][dot[1] - 1] = "X"
                self.print_board()
            else:
                sleep(0.5)
                print('Мимо')
                sleep(1)
                self.board[dot[0] - 1][dot[1] - 1] = "T"
            shot_list += [dot]
            print(shot_list)
            if hit == True:
                return True
            else:
                return False
        else:
            raise DontShootTwice




class Player:
    def __init__(self, board, enemy_board):
        self.board = board
        self.enemy_board = enemy_board

    def ask(self):
        pass

    def move(self):
        valid = False
        while valid == False:
            try:
                self.ask()
            except Exception as e:
                print(f"Ошибка {e} попробуйте еще раз")
            else:
                valid = True

class User(Player):
    def ask(self):
        x = int(input("Введите координаты точки по х куда желаете произвести выстрел: "))
        y = int(input("Введите координаты точки по y куда желаете произвести выстрел: "))
        if 0 < x <= 6 and 0 < y <= 6:
            return [x, y]
        else:
            raise BoardOutException

class AI(Player):
    def ask(self):
        x = randrange(1, 7)
        y = randrange(1, 7)
        return [x, y]


class Game:
    def __init__(self, User_board = None, AI_board = None, user = None,  AI = None, ship_list = []):
        self.user = User
        self.User_board = User_board
        self.AI = AI
        self.AI_board = AI_board
        self.ship_list = ship_list

    def random_board(self, board, ban_list):
        iter = 0
        counter = 0
        while counter != 7:
            if iter > 1000:
                return False
            x = randrange(1, 7)
            y = randrange(1, 7)
            if [x, y] in ban_list:
                iter += 1
                continue
            tmp = randrange(1, 3)
            if tmp == 1:
                direction = "horizontal"
            else:
                direction = "vertical"
            if counter < 1:
                if direction == "horizontal":
                    if [x, y + 1] not in ban_list and [x, y + 2] not in ban_list:
                        if y + 1 < 7 and y + 2 < 7:
                            ban_list += [x, y], [x + 1, y], [x, y + 1], [x + 1, y + 1], [x - 1, y], [x, y - 1], [x - 1,
                                                                                                                 y - 1], [x - 1,
                                                                                                                          y + 1], [
                                x + 1, y - 1], [x, y + 2], [x - 1, y + 2], [x + 1, y + 2], [x + 1, y + 3], [x, y + 3], [x - 1,
                                                                                                                        y + 3]
                            ship = [[x, y], [x, y + 1], [x, y + 2]]
                            board.add_ship(ship, 3)
                            self.ship_list += [x, y], [x, y + 1], [x, y + 2]
                            counter += 1
                        else:
                            iter += 1
                            continue
                    else:
                        iter += 1
                        continue
                else:
                    if [x + 1, y] not in ban_list and [x + 2, y] not in ban_list:
                        if x + 1 < 7 and x + 2 < 7:
                            ban_list += [x, y], [x + 1, y], [x, y + 1], [x + 1, y + 1], [x - 1, y], [x, y - 1], [x - 1,
                                                                                                                 y - 1], [x - 1,
                                                                                                                          y + 1], [
                                x + 1, y - 1], [x + 2, y], [x + 2, y + 1], [x + 2, y - 1], [x + 3, y], [x + 3, y + 1], [x + 3,
                                                                                                                     y - 1]
                            ship = [[x, y], [x + 1, y], [x + 2, y]]
                            board.add_ship(ship, 3)
                            self.ship_list += [x, y], [x + 1, y], [x + 2, y]
                            counter += 1
                        else:
                            iter += 1
                            continue
                    else:
                        iter += 1
                        continue
            elif counter < 3:
                if direction == "horizontal":
                    if [x, y + 1] not in ban_list:
                        if y + 1 < 7:
                            ban_list += [x, y], [x + 1, y], [x, y + 1], [x + 1, y + 1], [x - 1, y], [x, y - 1], [x - 1,
                                                                                                                 y - 1], [x - 1,
                                                                                                                          y + 1], [
                                x + 1, y - 1], [x, y + 2], [x - 1, y + 2], [x + 1, y + 2]

                            ship = [[x, y], [x, y + 1]]
                            board.add_ship(ship, 2)
                            self.ship_list += [x, y], [x, y + 1]
                            counter += 1
                        else:
                            iter += 1
                            continue
                    else:
                        iter += 1
                        continue
                else:
                    if [x + 1, y] not in ban_list:
                        if x + 1 < 7:
                            ban_list += [x, y], [x + 1, y], [x, y + 1], [x + 1, y + 1], [x - 1, y], [x, y - 1], [x - 1,
                                                                                                                 y - 1], [x - 1,
                                                                                                                          y + 1], [
                                x + 1, y - 1], [x + 2, y], [x + 2, y + 1], [x + 2, y - 1]

                            ship = [[x, y], [x + 1, y]]
                            board.add_ship(ship, 2)
                            self.ship_list += [x, y], [x + 1, y]
                            counter += 1
                        else:
                            iter += 1
                            continue
                    else:
                        iter += 1
                        continue
            elif counter < 7:
                ban_list += [x, y], [x + 1, y], [x, y + 1], [x + 1, y + 1], [x - 1, y], [x, y - 1], [x - 1, y - 1], [x - 1,
                                                                                                                     y + 1], [
                    x + 1, y - 1]
                ship = [[x, y]]
                board.add_ship(ship, 1)
                self.ship_list += [[x, y]]
                counter += 1
        return True
    def get_ship_list(self):
        return self.ship_list


    def greet(self):
        print("Добро пожаловать в Морской бой!!! \n"
              "Для начала вам нужно заполнить доску кораблями \n"
              "Нажмите Enter чтобы продолжить")
        input()
    def loop(self):
        board1 = Board(False)
        ban_list1 = []
        shot_list1 = []
        shot_list2 = []
        print("Создадим однопалубные корабли")
        ship1 = Ship(1)
        ship2 = Ship(1)
        ship3 = Ship(1)
        ship4 = Ship(1)
        list_ = [ship1, ship2, ship3, ship4]
        for i in list_:
            while True:
                try:
                    sleep(0.5)
                    i.set_ship(ban_list1)
                    board1.add_ship(i.get_ship(), i.get_len())
                    board1.print_board()
                    sleep(0.5)
                except Exception:
                    print("Клетка занята, попробуйте еще раз")
                else:
                    break
        print("Создадим двухпалубные корабли")
        ship5 = Ship(2)
        ship6 = Ship(2)
        list_ = [ship5, ship6]
        for i in list_:
            while True:
                try:
                    sleep(0.5)
                    i.set_ship(ban_list1)
                    board1.add_ship(i.get_ship(), i.get_len())
                    board1.print_board()
                    sleep(0.5)
                except Exception:
                    print("Клетка занята, попробуйте еще раз")
                else:
                    break
        print("Создадим трехпалубник")
        ship7 = Ship(3)
        while True:
            try:
                sleep(0.5)
                ship7.set_ship(ban_list1)
                board1.add_ship(ship7.get_ship(), ship7.get_len())
                board1.print_board()
                sleep(0.5)
            except Exception:
                print("Клетка занята, попробуйте еще раз")
            else:
                break
        print("Далее будет сгенерирована случайная доска для AI")
        while True:
            try:
                board2 = Board(True)
                ban_list2 = []
                if game.random_board(board2, ban_list2) == False:
                    raise FailBoard
            except Exception:
                continue
            else:
                break
        sleep(1)
        print("Ваш ход первый")
        player1 = User(board2, board1)
        player2 = AI(board1,board2)
        while True:
            while True:
                board2.print_board()
                try:
                    if board2.shot(player1.ask(), shot_list2) == False:
                        break
                except DontShootTwice:
                    print("Ошибка, попробуйте еще раз")
            print("Доска AI")
            board2.print_board()
            board2.import_list(game.get_ship_list())
            if board2.living_ships() == False:
                print("Игрок победил")
                break
            while True:
                try:
                    if board1.shot(player2.ask(), shot_list1) == False:
                        break
                except DontShootTwice:
                    pass
            print("Доска Игрока")
            board1.print_board()
            if board1.living_ships() == False:
                print("AI победил")
                break




    def start(self):
        self.greet()
        self.loop()

game = Game()
game.start()