class StateEncoder:
    """
    State Encoder class for the snake game.
    Converts the complex state representation into a simplified format
    that can be used as a key in the Q-table.
    """
    def __init__(self, max_vision_length=8):
        """
        Initialize the StateEncoder with given parameters.
        This limits how far the snake can see for Q-table simplification.
        Args:
            max_vision_length: Maximum length of the vision for the snake
        """
        self.max_vision_length = max_vision_length

    def encode(self, state):
        """
        Encode a single direction vision list into a string.
        Limits the vision to max_vision_length elements
        """

        up_vision = self._encode_direction(state["up"])
        right_vision = self._encode_direction(state["right"])
        down_vision = self._encode_direction(state["down"])
        left_vision = self._encode_direction(state["left"])
        food_direction = self._find_food_direction(state)

        state_key = f"{up_vision}|{right_vision}|{down_vision}|{left_vision}|{food_direction}"
        return state_key
    
    def _find_food_direction(self, state):
        """
        Find the direction to the closest food (green apple).
        Returns a value 0-3 indicating the primary direction to food:
        0: up, 1: right, 2: down, 3: left, -1: no food visible
        """
        directions = ["up", "right", "down", "left"]
        food_distances = []

        for direction in directions:
            try:
                food_index = state[direction].index(3)
                food_distances.append((food_index, directions.index(direction)))
            except:
                pass
        
        if not food_distances:
            return -1

        clossest_food = min(food_distances, key=lambda x: x[0])
        return clossest_food[1]

    def _encode_direction(self, vision_list):
        """
        Encode a single direction vision list into a string.
        Limits the vision to max_vision_length elements.
        """

        limited_vision = vision_list[:min(len(vision_list),
                                          self.max_vision_length)]
        return "_".join(map(str, limited_vision))

    def decode(self, state_key):
        """
        Decode a state key back into a state dictionary.
        Useful for debugging and visualization.
        """

        parts = state_key.split("|")
        if len(parts) != 4:
            raise ValueError("Invalid state key format")
        decoded_sate = {
            "up": self._decode_direction(parts[0]),
            "right": self._decode_direction(parts[1]),
            "down": self._decode_direction(parts[2]),
            "left": self._decode_direction(parts[3])
        }

        if len(parts) > 4:
            decoded_sate["food_direction"] = int(parts[4])
        
        return decoded_sate

    def _decode_direction(self, encoded_string):
        """
        Helper to decode a direction string to a list of integers
        """
        if not encoded_string:
            return []
        return [int(x) for x in encoded_string.split("_")]
