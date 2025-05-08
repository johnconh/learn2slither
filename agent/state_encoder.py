class StateEncoder:
    """
    State Encoder class for the snake game.
    Converts the complex state representation into a simplified format
    that can be used as a key in the Q-table.
    """
    def __init__(self, max_vision_length=5):
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

        danger_up = self._detect_danger(state["up"])
        danger_right = self._detect_danger(state["right"])
        danger_down = self._detect_danger(state["down"])
        danger_left = self._detect_danger(state["left"])

        food_up = self._detect_food(state["up"])
        food_right = self._detect_food(state["right"])
        food_down = self._detect_food(state["down"])
        food_left = self._detect_food(state["left"])

        red_food_up = self._detect_red_food(state["up"])
        red_food_right = self._detect_red_food(state["right"])
        red_food_down = self._detect_red_food(state["down"])
        red_food_left = self._detect_red_food(state["left"])

        state_key = (
            f"{danger_up}{danger_right}{danger_down}{danger_left}|"
            f"{food_up}{food_right}{food_down}{food_left}|"
            f"{red_food_up}{red_food_right}{red_food_down}{red_food_left}"
        )
        return state_key

    def _detect_danger(self, vision):
        """
        Detect danger in vision with distance awareness.
        Returns:
        - 2: Immediate danger (position 0)
        - 1: Near danger (positions 1-2)
        - 0: No danger in visible range
        """
        if 2 in vision[:1] or 5 in vision[:1]:
            return 2
        elif 2 in vision[1:3] or 5 in vision[1:3]:
            return 1
        return 0
    
    def _detect_food(self, vision):
        """
        Detect green apple in vision with distance awareness.
        Returns:
        - 3: Green apple at immediate position
        - 2: Green apple at position 1
        - 1: Green apple at positions 2-4
        - 0: No green apple in visible range
        """

        if 3 in vision[:1]:
            return 3
        elif 3 in vision[1:2]:
            return 2
        elif 3 in vision[2:4]:
            return 1
        return 0

    def _detect_red_food(self, vision):
        """
        Detect red apple in vision with distance awareness.
        Returns:
        - 1: Red apple visible
        - 0: No red apple in visible range
        """
        if 4 in vision[:5]:
            return 1
        return 0