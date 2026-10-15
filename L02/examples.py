"""L02 quick review examples. Run: python examples.py"""

def demo_function_defaults():
    def greet(name, title="同学"):
        return f"{title}{name}"

    print(greet("Q"))
    print(greet("Q", title="学员"))


def demo_mutable_default_pitfall():
    def bad_append(x, box=None):
        if box is None:
            box = []
        box.append(x)
        return box

    print(bad_append(1))
    print(bad_append(2))  # 应为 [2]，不是 [1, 2]


def demo_fact_loop_and_recurse():
    def fact_loop(n):
        r = 1
        for i in range(2, n + 1):
            r *= i
        return r

    def fact_rec(n):
        if n <= 1:
            return 1
        return n * fact_rec(n - 1)

    print("5! loop", fact_loop(5), "rec", fact_rec(5))


def demo_try_except():
    for s in ["12", "x"]:
        try:
            print(int(s))
        except ValueError:
            print("not int:", s)


def demo_class_inherit():
    class Person:
        def __init__(self, name):
            self.name = name

        def label(self):
            return self.name

    class Student(Person):
        def __init__(self, name, sid):
            super().__init__(name)
            self.sid = sid

        def label(self):
            return f"{self.name}#{self.sid}"

    print(Student("Q", "2026").label())


if __name__ == "__main__":
    demo_function_defaults()
    demo_mutable_default_pitfall()
    demo_fact_loop_and_recurse()
    demo_try_except()
    demo_class_inherit()
