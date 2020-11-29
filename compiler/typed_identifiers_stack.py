class TypedIdentifiersStack():
    def __init__(self):
        self._stack = []

    def search(self, token_name):
        for token in self._stack[::-1]:
            if not token['token'] == "$" and token['token'] == token_name:
                    return token
        return False

    def push(self, identifier):
        self._stack.append(identifier)
        self.print()

    def pop(self):
        if len(self._stack) > 0:
            self._stack.pop();

    def print(self):
        s = "| "
        for item in self._stack:
            s += item['token'] + ": "+ item["type"] + " | "
        # print('TYPED_STACK: ', s)

    def close_scope(self):
        for token in self._stack[::-1]:
            if token['token'] != '$':
                self.pop()
            else:
                self.pop()
                break
        self.print()