def compute_code(board):
    """Computes the ternary code-number for a given Terni Lapilli board.

    The board is represented as a list of 9 integers where:
    - 0 indicates an empty cell,
    - 1 indicates a piece of player 1,
    - 2 indicates a piece of player 2.

    The board must contain exactly three of each value (0, 1, and 2), otherwise the function returns None.

    The code-number is calculated using the formula:
        code = sum(p_i * (3 ** i)) for i in range(9)

    Args:
        board (List[int]): A list of 9 integers representing the board state.

    Returns:
        Optional[int]: The computed code-number, or None if the input is invalid.
    """
    return None if len(board) != 9 or board.count(0) != 3 or board.count(1) != 3 or board.count(2) != 3 \
        else sum(p * (3 ** i) for i, p in enumerate(board))