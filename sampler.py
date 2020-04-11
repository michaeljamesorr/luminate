#!/usr/bin/env python3


class Sampler:

    def __init__(self, function):

        self._function = function

    def sample(self, **kwargs):
        return self._function(**kwargs)


def test(x, y):
    return "X: {x}, Y: {y}".format(x=x, y=y)


def main():
    s = Sampler(test)
    print(s.sample(x=1, y=10))


if __name__ == '__main__':
    main()
