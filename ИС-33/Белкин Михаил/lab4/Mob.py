# -*- coding: utf-8 -*-

from turtle import Turtle


class Mob(Turtle):
    def __init__(self, coords, speed, color, shape, merge, wall_size):
        super().__init__()
        self.penup()

        self.__pos = coords
        self.goto(coords[1] * wall_size - merge[0], -coords[0] * wall_size + merge[1])

        self.speed(speed)
        self.shape(shape)
        self.color(color)
        self.w_merge, self.h_merge = merge
        self.wall_size = wall_size
        self.shapesize(wall_size / 20)

    def getPosition(self):
        return self.__pos

    def move(self, maze, height, width, target):
        path = self.Search_BestFirst(maze, height, width, self.__pos, target)
        if path:
            move_y, move_x = path[1]
            self.goto(move_x * self.wall_size - self.w_merge, -move_y * self.wall_size + self.h_merge)
            self.__pos = move_y, move_x

    def Search_BestFirst(self, maze, height, width, start, end):
        maze_ = []
        for i in range(height):
            maze_.append(maze[i][:])

        path = [start]  # Путь до выхода
        x, y = start

        while path:  # Пока есть путь
            if (x, y) == end:  # Если точка соответствует координатам выхода
                return path

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Перебираем все возможные перемещения
                nx, ny = x + dx, y + dy

                # Если соседняя позиция не выходит за границы лабиринта и не является стеной
                if 0 <= nx < height and 0 <= ny < width and maze_[nx][ny]:
                    path.append((nx, ny))  # Добавляем точку в путь до выхода
                    maze_[nx][ny] = 0  # Закрываем путь назад

                    x, y = nx, ny

                    break
            else:  # Если пришли в тупик
                path.pop()  # Удаляем последнюю точку из пути
                if path:
                    x, y = path[-1]  # Возвращаемся в предыдущую точку

        return []
