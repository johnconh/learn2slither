from collections import deque


class Snake:
    def _init_(self, start_pos, init_length=3):
        self.body = deque(maxlen=init_length)
        self.body.append(start_pos)
        self.length = 1

    def grow(self):
        """
        Increase the snake's length by 1.
        """
        self.length += 1
        self.body = deque(self.body, maxlen=self.length)

    def shrink(self):
        """
        Decrease the snake's length by 1.
        """
        if self.length > 1:
            self.length -= 1
            self.body = deque(list(self.body)[:-1], maxlen=self.length)
            return True
        else:
            return False

    def move(self, new_head_pos):
        """
        Move the snake to a new head position.
        Adds a new head position and removes the tail.
        """
        self.body.appendleft(new_head_pos)
        if len(self.body) > self.length:
            self.body.pop()

    def get_head(self):
        """
        Get the position of the snake's head.
        """
        return self.body[0]

    def get_body(self):
        """
        Get the positions of the snake's body (excluding the head).
        """
        return list(self.body)[1:]

    def is_collision(self, pos):
        """
        Check if the given position collides with the snake's body.
        """
        return pos in self.body[1:]