from collections import deque


def check_relation(net, first, second):
    graph = {}
    for name_pairs in net:
        if name_pairs[0] not in graph:
            graph[name_pairs[0]] = []
        if name_pairs[1] not in graph:
            graph[name_pairs[1]] = []
        graph[name_pairs[0]].append(name_pairs[1])
        graph[name_pairs[1]].append(name_pairs[0])
    # для хранения пользователей которых проверяли для данного юзера
    visited_points = set()
    # создаём объект класса deque для более быстрого доступа к объектам очереди по сравнению с классическим списком
    names_queue = deque([first])
    while names_queue:
        name_from_queue = names_queue.popleft()
        if name_from_queue == second:
            return True
        visited_points.add(name_from_queue)
        for friend in graph[name_from_queue]:
            if friend not in visited_points:
                names_queue.append(friend)
    return False


if __name__ == '__main__':
    net = (
        ("Ваня", "Лёша"), ("Лёша", "Катя"),
        ("Ваня", "Катя"), ("Вова", "Катя"),
        ("Лёша", "Лена"), ("Оля", "Петя"),
        ("Стёпа", "Оля"), ("Оля", "Настя"),
        ("Настя", "Дима"), ("Дима", "Маша")
    )

    # print(check_relation(net, "Петя", "Стёпа"))
    # print(check_relation(net, "Маша", "Петя"))
    # print(check_relation(net, "Ваня", "Дима"))
    # print(check_relation(net, "Лёша", "Настя"))
    # print(check_relation(net, "Стёпа", "Маша"))
    # print(check_relation(net, "Лена", "Маша"))
    # print(check_relation(net, "Вова", "Лена"))
    assert check_relation(net, "Петя", "Стёпа") is True
    assert check_relation(net, "Маша", "Петя") is True
    assert check_relation(net, "Ваня", "Дима") is False
    assert check_relation(net, "Лёша", "Настя") is False
    assert check_relation(net, "Стёпа", "Маша") is True
    assert check_relation(net, "Лена", "Маша") is False
    assert check_relation(net, "Вова", "Лена") is True
