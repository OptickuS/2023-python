# -*- coding: utf-8 -*-

from turtle import Turtle


# Класс узла
class Node:
    def __init__(self, parent=None, pos=None):  # Конструктор узла
        self.parent = parent  # Родитель из которого можно попасть в этот узел
        self.pos = pos  # Координаты узла

        self.g = 0  # Стоимость пути от начального узла до этого узла
        self.h = 0  # Эвристическое приближение стоимости пути от этого узла до конечного узла
        self.f = 0  # Минимальная стоимость перехода в этот узел

    def __eq__(self, other):  # Перегрузка оператора равенства (==)
        return self.pos == other.pos


class Avatar(Turtle):
    def __init__(self, coords, speed, color, shape, maze, height, width, target, merge, wall_size):
        super().__init__()
        self.penup()

        self.__position = coords
        self.goto(coords[1] * wall_size - merge[0], -coords[0] * wall_size + merge[1])

        self.speed(speed)
        self.shape(shape)
        self.color(color)
        self.w_merge, self.h_merge = merge
        self.wall_size = wall_size
        self.shapesize(wall_size / 20)

        self.path = self.Search_Astar(maze, height, width, self.__position, target)[::-1]
        self.step = 1

    def getPosition(self):
        return self.__position

    def move(self):
        self.goto(self.path[self.step][1] * self.wall_size - self.w_merge,
                  -self.path[self.step][0] * self.wall_size + self.h_merge)
        self.__position = self.path[self.step]
        self.step += 1

    def Search_Astar(self, maze, height, width, start, end):
        start_node = Node(None, start)  # Создаем стартовый узел
        end_node = Node(None, end)  # Создаем конечный узел

        start_node.g = 0
        start_node.h = (((start_node.pos[0] - end_node.pos[0]) ** 2) +
                        ((start_node.pos[1] - end_node.pos[1]) ** 2)) ** 0.5
        start_node.f = start_node.g + start_node.h

        not_visited = [start_node]  # Список непосещенных узлов
        visited = []  # Список посещенных узлов

        while len(not_visited) > 0:  # Пока список непосещенных узлов непустой
            cur_node = not_visited[0]  # Берем первый узел в списке непосещенных
            cur_ind = 0  # Его индекс

            # Перебираем индексы непосещенных узлов, чтобы найти узел с наименьшей стоимостью перемещения
            for ind in range(len(not_visited)):
                if not_visited[ind].f < cur_node.f:
                    cur_node = not_visited[ind]
                    cur_ind = ind

            not_visited.pop(cur_ind)  # Удаляем узел с наименьшей стоимостью перемещения из списка непосещенных
            visited.append(cur_node)  # Добавляем его в список посещенных

            if cur_node == end_node:  # Если узел, в котором мы сейчас находимся, является финальным узлом
                path = []

                cur = cur_node
                while cur is not None:  # Проходимся по ветке узлов
                    path.append(cur.pos)  # Генерируем путь
                    cur = cur.parent

                return path

            for new_pos in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Перебираем все возможные перемещения
                node_pos = (
                    cur_node.pos[0] + new_pos[0], cur_node.pos[1] + new_pos[1])  # Вычисляем позицию соседнего узла

                # Если координаты соседнего узла не за границами лабиринта и не является стеной
                if (0 <= node_pos[0] < height and
                        0 <= node_pos[1] < width and
                        maze[node_pos[0]][node_pos[1]]):
                    new_node = Node(cur_node, node_pos)  # Создаем новый узел

                    if new_node not in visited:
                        # Вычисляем веса
                        new_node.g = cur_node.g + 1
                        new_node.h = (((new_node.pos[0] - end_node.pos[0]) ** 2) +
                                      ((new_node.pos[1] - end_node.pos[1]) ** 2)) ** 0.5
                        new_node.f = new_node.g + new_node.h

                        eq_nodes = []

                        # Ищем этот узел в списке непосещенных и удаляем те,
                        # у которых узлы имеет стоимость перемещения больше
                        for i in range(len(not_visited)):
                            if new_node == not_visited[i]:
                                if new_node.f > not_visited[i].f:
                                    eq_nodes.append(not_visited[i])
                                else:
                                    not_visited.pop(i)

                        # Если есть нет узлов, которые соответствуют данному узлу, то добавляем его в список непосещенных
                        if len(eq_nodes) <= 0:
                            not_visited.append(new_node)

        return []
