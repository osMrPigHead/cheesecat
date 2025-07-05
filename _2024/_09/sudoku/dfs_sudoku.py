import numpy as np


def dfs(a):
    if True not in set((a == 0).flat):
        return [a]
    idx = tuple(x[0] for x in np.where(a == 0))
    n = set(range(1, 10))
    n -= set(a[idx[0]].flat)
    n -= set(a[:, idx[1]].flat)
    idz = tuple(i // 3 * 3 for i in idx)
    n -= set(a[idz[0]:idz[0]+3, idz[1]:idz[1]+3].flat)
    ans = []    
    for ni in n:
        d = np.zeros((9, 9), dtype=int)
        d[idx] = ni
        ans += dfs(a + d)
    return ans


def main():
    print("="*11)
    print()
    a = []
    for i in range(9):
        a += [[int(x) for x in input()]]
    a = np.array(a)
    assert a.shape == (9, 9)
    ans = dfs(a)
    print()
    print("SOLUTIONS==")
    print()
    for x in ans:
        for nx in x:
            for ny in nx:
                print(ny, end="")
            print()
        print()


if __name__ == "__main__":
    print()
    while True:
        main()
