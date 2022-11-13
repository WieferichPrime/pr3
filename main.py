import numpy as np


def neighbors(a, row, col):
    return [a[i][j]['color'] for j in range(col-1, col+2)
                               for i in range(row-1, row+2)
                               if (-1 < j < len(a[0]) and
                                   -1 < i < len(a) and
                                   (col != j or row != i) and
                                   (0 <= j < len(a[0])) and
                                   (0 <= i < len(a)))]


def unhappy_iter(b):
    for i in range(len(b)):
        for j in range(len(b[0])):
            boys_next_door = neighbors(b, i, j)
            blacks = len(list(filter(lambda x: x == 'B', boys_next_door)))
            whites = len(boys_next_door) - blacks
            if b[i][j]['color'] == 'B':
                b[i][j]['status'] = 'happy' if blacks >= 2 else 'unhappy'
            elif b[i][j]['color'] == 'W':
                b[i][j]['status'] = 'happy' if whites >= 2 else 'unhappy'
            else:
                b[i][j]['status'] = None

def main():
    n = int(input('Grid size:'))
    b = np.random.choice(['B', 'W', '_'], n ** 2, p=[0.45, 0.45, 0.1])
    b = [[{'color': b[(i + j * n)], 'status': None} for i in range(n)] for j in range(n)]

    print('before:')
    for i in range(n):
        for j in range(n):
            print(b[i][j]['color'], end=" ")
        print()

    unhappy_iter(b)

    unhappy = 0

    for i in range(n):
        for j in range(n):
            if b[i][j]['status'] == 'unhappy':
                unhappy += 1

    print('Unhappy:', unhappy)


    for _ in range(10000):
        rows_with_human = [i for i, _ in enumerate(b) if len(list(filter(lambda x: x['color'] != '_' and x['status'] == 'unhappy', b[i]))) != 0]
        random_row = np.random.choice(rows_with_human)
        not_empty_cells = [j for j, value in enumerate(b[random_row]) if value['color'] != '_' and value['status'] == 'unhappy']
        random_col = np.random.choice(not_empty_cells)
        not_empty_cell = random_row, random_col

        if len(rows_with_human) == 0:
            print('Everybody happy')
            break

        rows_with_empty = [i for i, _ in enumerate(b) if len(list(filter(lambda x: x['color'] == '_', b[i]))) != 0]
        random_row = np.random.choice(rows_with_empty)
        empty_cells = [j for j, value in enumerate(b[random_row]) if value['color'] == '_']
        random_col = np.random.choice(empty_cells)
        empty_cell = random_row, random_col

        b[not_empty_cell[0]][not_empty_cell[1]], b[empty_cell[0]][empty_cell[1]] = b[empty_cell[0]][empty_cell[1]], b[not_empty_cell[0]][not_empty_cell[1]]

    print('after:')
    for i in range(n):
        for j in range(n):
            print(b[i][j]['color'], end=" ")
        print()

    unhappy_iter(b)

    unhappy = 0
    for i in range(n):
        for j in range(n):
            if b[i][j]['status'] == 'unhappy':
                unhappy += 1
    print('Unhappy:', unhappy)

if __name__ == '__main__':
    main()
