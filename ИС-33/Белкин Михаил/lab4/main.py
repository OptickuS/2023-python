# -*- coding: utf-8 -*-

from Avatar import Avatar
from Mob import Mob

import turtle

H_MERGE = 495
W_MERGE = 800
WALL_SIZE = 2


def main():
    # Имя файла с лабиринтом
    input_file_name = "maze-for-u.txt"

    # Лабиринты
    maze = []
    avatar_maze = []
    mob_maze = []

    # Открываем файл с лабиринтом и считываем его в матрицу
    with open(input_file_name, "r", encoding="utf-8") as f:
        file = f.readlines()

        height = len(file)
        width = len(file[0]) - 1

        for line in file:
            tmp_line = [0 if sym == "#" else 1 for sym in line[:-1]]
            maze.append(tmp_line[:])
            avatar_maze.append(tmp_line[:])
            mob_maze.append(tmp_line[:])

    # Ввод исходных данных
    print("Координаты аватара:")
    avatar_ = (int(input(f"[0 <= x <= {width - 1}]: ")), int(input(f"[0 <= y <= {height - 1}]: ")))

    print("\nКоординаты моба:")
    mob_ = (int(input(f"[0 <= x < {width - 1}]: ")), int(input(f"[0 <= y < {height - 1}]: ")))

    print("\nКоординаты выхода:")
    exit_ = (int(input(f"[0 <= y < {width - 1}]: ")), int(input(f"[0 <= y < {height - 1}]: ")))

    turtle.setup(width=1700, height=1000)

    wall = turtle.Turtle()
    wall.shape('square')
    wall.color('black')
    wall.shapesize(WALL_SIZE / 20)
    wall.penup()
    wall.speed(5)

    for y in range(height):
        for x in range(width):
            if maze[y][x] == 0:
                wall.goto(x * WALL_SIZE - W_MERGE, -y * WALL_SIZE + H_MERGE)
                wall.stamp()

    avatar = Avatar(avatar_, 5, 'blue', 'circle', avatar_maze, height, width, exit_, (W_MERGE, H_MERGE), WALL_SIZE)
    mob = Mob(mob_, 5, 'red', 'circle', (W_MERGE, H_MERGE), WALL_SIZE)

    while avatar.getPosition() != exit_ and avatar.getPosition() != mob.getPosition():
        if avatar.getPosition() != exit_ and avatar.getPosition() != mob.getPosition():
            avatar.move()
        if avatar.getPosition() != exit_ and avatar.getPosition() != mob.getPosition():
            mob.move(mob_maze, height, width, avatar.getPosition())


if __name__ == "__main__":
    main()

"""
INPUT:

0
1
212
605
599
798

--- OR ---

0
1
146
631
599
798
"""
