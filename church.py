from expression import Abstraction, Application


def church_numeral(n: int) -> Abstraction:
    inner = Abstraction("x", "x")

    for i in range(n):
        inner.body = Application("f", inner.body)

    return Abstraction("f", inner)



if __name__ == '__main__':
    print(church_numeral(2))
