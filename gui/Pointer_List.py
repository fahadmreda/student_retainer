
class pointer_list:
    def __init__(self):
        self.list = []
        self.current = 0
        self.size = 0

    def add(self, n):
        self.list.append(n)
        self.size += 1

    def increment(self):
        if self.current+1 == self.size:
            self.current = 0
        else:
            self.current += 1

    def decrement(self):
        if self.current-1 == -1:
            self.current = self.size-1
        else:
            self.current -= 1

    def raise_frame(self):
        self.list[self.current].tkraise()