class IdentifiersStack():
    def __init__(self):
        self._stack = []

    def search(self, token_name):
        for token in self._stack[::-1]:
            if not token['token'] == "$" and token['token'] == token_name:
                    return True
        return False

    def push(self, identifier):
        self._stack.append(identifier)
        self._print_stack()

    def pop(self):
        if len(self._stack) > 0:
            self._stack.pop();

    def _print_stack(self):
        s = "| "
        for item in self._stack:
            s += item['token'] + " | "
        print('STACK: ', s)

    def close_scope(self):
        for token in self._stack[::-1]:
            if token['token'] != '$':
                self.pop()
            else:
                self.pop()
                break
        self._print_stack()