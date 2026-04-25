class Player:
    def __init__(self, color, time_limit=None):
        self.color = color
        self.piece_count = 0
        self.time_remaining = time_limit

    def add_pieces(self, count):
        self.piece_count += count

    def remove_pieces(self, count):
        self.piece_count = max(0, self.piece_count - count)

    def tick(self, dt):
        if self.time_remaining is not None:
            self.time_remaining = max(0.0, self.time_remaining - dt)

    def is_out_of_time(self):
        return self.time_remaining is not None and self.time_remaining <= 0
