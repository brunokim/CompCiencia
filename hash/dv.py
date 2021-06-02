
def rev_digits(n):
    while n >= 10:
        yield n % 10
        n //= 10
    yield n


def terms(num):
    for m, d in zip(range(2, 1000), rev_digits(num)):
        yield m*d


def dv(num, ds=None):
    if ds is None:
        ds = list(reversed(list(rev_digits(num))))
    ts = list(reversed(list(terms(num))))
    s = sum(ts)
    mod = s % 11
    if mod == 0:
        dv = 0
    else:
        dv = 11 - mod
    return locals()


def dist(ds1, ds2):
    d = abs(len(ds1) - len(ds2))
    for d1, d2 in zip(ds1, ds2):
        if d1 != d2:
            d += 1
    return d


def circ(ds1, r):
    num_digits = len(ds1)
    maxnum = 10**num_digits
    for i in range(maxnum):
        ds2 = list(reversed(list(rev_digits(i))))
        ds2 = ([0]*(num_digits-len(ds2))) + ds2
        d = dist(ds1, ds2)
        if d == r:
            yield i, ds2

def main():
    info = dv(33333)
    print(info)
    ds1 = info['ds']
    dv1 = info['dv']

    for r in [1, 2]:
        num_r, num_r_dv = 0, 0
        for i, ds2 in circ(ds1, r):
            info2 = dv(i, ds2)
            dv2 = info2["dv"]
            num_r += 1
            if dv1 == dv2:
                print(f'{i:05d}-{dv2}')
                num_r_dv += 1
        print(f'num[d={r}] = {num_r}, num[d={r}, dv={dv1}] = {num_r_dv}')


if __name__ == '__main__':
    main()
