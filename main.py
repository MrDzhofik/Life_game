import pygame
import copy


class Board:
    # создание поля
    def __init__(self, width, height, left=10, top=10, cell_size=30):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.set_view(left, top, cell_size)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        color = ["black","green",  "white", "blue", "yellow","red"]
        for j in range(self.width):
            for i in range(self.height):
                pygame.draw.rect(screen, pygame.Color(color[self.board[i][j]]),
                                 (self.left + self.cell_size * j, self.top + self.cell_size * i,
                                  self.cell_size, self.cell_size))
                pygame.draw.rect(screen, (255, 255, 255), (self.left + self.cell_size * j, self.top + self.cell_size * i,
                                                           self.cell_size, self.cell_size), 1)
    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_y < 0 or cell_x >= self.width or cell_y >= self.height:
            return None
        return cell_y, cell_x

    def on_click(self, cell):
        pass

    def on_click_line(self, cell):
        pass

    def get_click(self, mouse_pos, msb):
        cell = self.get_cell(mouse_pos)
        if cell:
            if msb == 1:
                self.on_click(cell)
            else:
                self.on_click_line(cell)


class Life(Board):
    def __init__(self, width, height, left=10, top=10, cell_size=30):
        super().__init__(width, height, left, top, cell_size)

    def on_click(self, cell):
        self.board[cell[0]][cell[1]] = (self.board[cell[0]][cell[1]] + 1) % 2

    def next_move(self):
        # сохраняем поле
        tmp_board = copy.deepcopy(self.board)
        # пересчитываем
        for y in range(self.height):
            for x in range(self.width):
                # сумма окружающих клеток
                s = 0
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                            continue
                        s += self.board[y + dy][x + dx]
                s -= self.board[y][x]
                if s == 3:
                    tmp_board[y][x] = 1
                elif s < 2 or s > 3:
                    tmp_board[y][x] = 0
        # обновляем поле
        self.board = copy.deepcopy(tmp_board)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Игра «Жизнь»')

    board = Life(53, 40, 0, 0, 15)
    game_on = False
    speed = 10
    ticks = 0
    fps = 60
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                game_on = not game_on
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.get_click(event.pos, 1)
                if event.button == 4:
                    speed += 1
                if event.button == 5:
                    speed -= 1
        # отрисовка и изменение свойств объектов
        board.render()
        # обновление экрана
        if ticks >= speed:
            if game_on:
                board.next_move()
            ticks = 0
        pygame.display.flip()
        clock.tick(fps)
        ticks +=1

    pygame.quit()