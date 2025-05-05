class StateEncoder:
    """
    State Encoder class for the snake game.
    Converts the complex state representation into a simplified format
    that can be used as a key in the Q-table.
    """
    def __init__(self, max_vision_length=3):
        """
        Initialize the StateEncoder with given parameters.
        This limits how far the snake can see for Q-table simplification.
        Args:
            max_vision_length: Maximum length of the vision for the snake
        """
        self.max_vision_length = max_vision_length

    def encode(self, state):
        """
        Encode the state dictionary into a string key for the Q-table.
        Simplifies the vision to reduce the state space.

        Format: "up_vision|right_vision|down_vision|left_vision"
        Where each vision is encoded as a string of cell types,
        limited to max_vision_length.
        """

        up_vision = self._encode_direction(state["up"])
        right_vision = self._encode_direction(state["right"])
        down_vision = self._encode_direction(state["down"])
        left_vision = self._encode_direction(state["left"])

        state_key = f"{up_vision}|{right_vision}|{down_vision}|{left_vision}"
        return state_key

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
        return {
            "up": [int(x) for x in parts[0]],
            "right": [int(x) for x in parts[1]],
            "down": [int(x) for x in parts[2]],
            "left": [int(x) for x in parts[3]],
        }
