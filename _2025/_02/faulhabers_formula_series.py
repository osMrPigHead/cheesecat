"""
Let $S_n^{(k-1)} = \sum\limits_{ i=1 }^{ k } a_i^{(k-1)} n^i = \sum\limits_{ i=1 }^{ n } i^{k-1}.$

We have:
$$
\begin{align}
a_1^{(0)} &= 1, \\
a_{p+1}^{(q+1)} &= \cfrac { q+1 }{ p+1 } a_p^{(q)}, \\
a_1^{(p)} &= 1 - \sum_{ i=1 }^{ p } a_{i+1}^{(p)}.
\end{align}
$$
"""
from fractions import Fraction


if __name__ == "__main__":
    a = [[Fraction(1)]]
    for q in range(1, 11):
        a += [[a[q-1][p-2]*q/p for p in range(2, q+2)]]
        a[q] = [1 - sum(a[q])] + a[q]
    for i in a:
        for j in reversed(i):
            print(j, " "*(8-len(str(j))), sep="", end="")
        print()
