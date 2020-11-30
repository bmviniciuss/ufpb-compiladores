class PCT():
    def __init__(self):
        self._stack = []

    def push(self, type):
        self._stack.append(type)

    def pop(self):
        if len(self._stack) > 0:
            return self._stack.pop()

    def peekTop(self):
        if len(self._stack) > 0:
            return self._stack[-1]
        return ""

    def print(self):
        s = "| "
        for item in self._stack:
            s += item + " | "
        print('PCT: ', s)
