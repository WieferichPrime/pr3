import numpy as np
import csv
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def neighbors(a, row, col):
    return [a[i][j]['color'] for j in range(col-1, col+2)
                               for i in range(row-1, row+2)
                               if (-1 < j < len(a[0]) and
                                   -1 < i < len(a) and
                                   (col != j or row != i) and
                                   (0 <= j < len(a[0])) and
                                   (0 <= i < len(a)))]


def happy_define(b):
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
    m = int(input('Iterations count:'))
    b = np.random.choice(['B', 'W', '_'], n ** 2, p=[0.45, 0.45, 0.1])
    b = [[{'color': b[(i + j * n)], 'status': None} for i in range(n)] for j in range(n)]

    happy_define(b)

    data = []
    for i in range(n):
        for j in range(n):
            data.append((i, j, b[i][j]['color']))

    with open("snapshot_before.csv", "wt") as fp:
        writer = csv.writer(fp, delimiter=",")
        writer.writerow(["x", "y", "type"])  # write header

        writer.writerows(data)

    snapshot = pd.read_csv('snapshot_before.csv')
    sns.scatterplot(snapshot, x=snapshot['x'], y=snapshot['y'], hue='type')
    plt.savefig('before.jpeg')
    plt.show()


    for _ in range(m):
        rows_with_human = [i for i, _ in enumerate(b) if len(list(filter(lambda x: x['color'] != '_' and x['status'] == 'unhappy', b[i]))) != 0]
        if len(rows_with_human) == 0:
            print('Everybody happy')
            break
        random_row = np.random.choice(rows_with_human)
        not_empty_cells = [j for j, value in enumerate(b[random_row]) if value['color'] != '_' and value['status'] == 'unhappy']
        random_col = np.random.choice(not_empty_cells)
        not_empty_cell = random_row, random_col

        rows_with_empty = [i for i, _ in enumerate(b) if len(list(filter(lambda x: x['color'] == '_', b[i]))) != 0]
        random_row = np.random.choice(rows_with_empty)
        empty_cells = [j for j, value in enumerate(b[random_row]) if value['color'] == '_']
        random_col = np.random.choice(empty_cells)
        empty_cell = random_row, random_col

        b[not_empty_cell[0]][not_empty_cell[1]], b[empty_cell[0]][empty_cell[1]] = b[empty_cell[0]][empty_cell[1]], b[not_empty_cell[0]][not_empty_cell[1]]
        happy_define(b)

    data = []
    for i in range(n):
        for j in range(n):
            data.append((i, j, b[i][j]['color']))

    with open("snapshot_after.csv", "wt") as fp:
        writer = csv.writer(fp, delimiter=",")
        writer.writerow(["x", "y", "type"])  # write header

        writer.writerows(data)

    snapshot = pd.read_csv('snapshot_after.csv')
    sns.scatterplot(snapshot, x=snapshot['x'], y=snapshot['y'], hue='type')
    plt.savefig('after.jpeg')
    plt.show()


if __name__ == '__main__':
    main()
