import numpy as np

ns = set(range(1, 10))


def main():
    a = []
    for i in range(9):
        a += [[int(x) for x in input()]]
    a = np.array(a)
    assert a.shape == (9, 9)

    for i in range(3):
        for j in range(3):
            assert set(a[i*3+j].flat) == ns, i*3+j
            assert set(a[:, i*3+j].flat) == ns, i*3+j
            assert set(a[i*3:i*3+3,j*3:j*3+3].flat) == ns, f"{i},{j}"
    input()


if __name__ == "__main__":
    while True:
        main()
