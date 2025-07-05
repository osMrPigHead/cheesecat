"""
Let $S_n^{(k-1)} = \sum\limits_{ i=0 }^{ k-1 } f_{i}(k) \ n^{(k-i)} = \sum\limits_{ i=1 }^{ n } i^{k-1}.$

We have:
$$
k \ f_p(k) = \binom{k}{p} - \sum_{ i=1 }^{ p } \binom{k}{i+1} f_{p-i}(k-i)
$$
"""
import sympy as sp


def generate_func(expression, symbol_x):
    return lambda x: expression.subs({symbol_x: x})


if __name__ == "__main__":
    k = sp.symbols("k")
    f = []
    for p in range(11):
        fpk = sp.simplify(sp.expand_func(
            ( sp.binomial(k, p) - sum([
                sp.binomial(k, i+1) * f[p-i](k-i)
                for i in range(1, p+1)
            ]) ) / k
        ))
        print(fpk)
        f += [generate_func(fpk, k)]
    print("\n\n")
    for n in range(11):
        for p in range(n+1):
            fpn = f[p](n + 1)
            print(fpn, " "*(8-len(str(fpn))), sep="", end="")
        print()
