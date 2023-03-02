import time

class Timer:
    def __init__(self, max_time):
        self.start_time = 0
        self.atual_time = 0
        self.max_time = max_time
        self.run = False

    def active(self):
        self.start_time = time.time()
        self.run = True

    def update(self):
        self.atual_time = time.time()
        if self.atual_time - self.start_time >= self.max_time:
            self.run = False