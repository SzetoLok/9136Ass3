from binh_chess import *
import pandas as pd
import re

# This function should be taken from task 6
def read_pgn(file_name: str) -> list[dict]:
    """
    Reads a PGN file and returns a list of dictionaries representing games.
    Each dictionary contains 7 tags and up to 20 moves for white and black.

    Args:
        file_name (str): Path to the PGN file.

    Returns:
        List[Dict]: List of game dictionaries with keys as specified in part1.txt.
    """
    games = []  # List to store all parsed games

    # Tags we care about (output keys are lower case)
    required_tags = ['event', 'white', 'black', 'result', 'whiteelo', 'blackelo', 'opening']

    # Read all lines from the file
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    current_line_index = 0
    total_lines = len(lines)

    while current_line_index < total_lines:
        # Skip any leading blank lines before a game
        while current_line_index < total_lines and lines[current_line_index].strip() == '':
            current_line_index += 1

        # If we reach the end of the file, break out of the loop
        if current_line_index >= total_lines:
            break

        # --- Parse the tag section for this game ---
        tags = {}  # Dictionary to hold the tags for this game
        while current_line_index < total_lines and lines[current_line_index].startswith('['):
            line = lines[current_line_index].strip()
            # Match lines like [TagName "Value"]
            match = re.match(r'\[([a-zA-Z]+)\s+"(.*)"\]', line)

            if match:
                tag, value = match.groups()
                tags[tag.lower()] = value  # Store tag in lower case
            current_line_index += 1

        # Skip blank line(s) between tags and moves
        while current_line_index < total_lines and lines[current_line_index].strip() == '':
            current_line_index += 1

        # --- Parse the moves section for this game ---
        moves_str = ''

        # Concatenate all lines containing moves until next tag or blank line
        while current_line_index < total_lines and not lines[current_line_index].startswith('[') and lines[current_line_index].strip() != '':
            moves_str += ' ' + lines[current_line_index].strip()
            current_line_index += 1
        moves_str = moves_str.strip()

        # Remove the result from the end of the move string if present
        moves_str = re.sub(r'\s*(1-0|0-1|1/2-1/2)\s*$', '', moves_str)

        # Split the moves string into tokens (move numbers and move notation)
        move_tokens = moves_str.split()

        # --- Prepare the output dictionary for this game ---
        game_dict = {}

        # Add all required tags, add '?' if player's rating is missing
        for tag in required_tags:
            game_dict[tag] = tags.get(tag, '?')

        # Initialize all w1-b20 keys to '-'
        for round_number in range(1, 21):
            game_dict[f'w{round_number}'] = '-'
            game_dict[f'b{round_number}'] = '-'

        # --- Extract moves into w1, b1, ..., w20, b20 ---
        current_round = 1  # Round number (1-based)
        move_token_index = 0  # Index in move_tokens list
        
        while move_token_index < len(move_tokens) and current_round <= 20:
            # Each round starts with a number and a period, e.g., "1."
            if re.match(r'^\d+\.$', move_tokens[move_token_index]):
                move_token_index += 1
                
                # Assign white's move if available and valid
                if move_token_index < len(move_tokens) and not re.match(r'^\d+\.$', move_tokens[move_token_index]):
                    game_dict[f'w{current_round}'] = move_tokens[move_token_index]
                    move_token_index += 1
                
                # Assign black's move if available and valid
                if move_token_index < len(move_tokens) and not re.match(r'^\d+\.$', move_tokens[move_token_index]):
                    game_dict[f'b{current_round}'] = move_tokens[move_token_index]
                    move_token_index += 1
                
                current_round += 1
            else:
                # If the token is not a move number, skip it (defensive)
                move_token_index += 1

        # Add the parsed game dictionary to the list of games
        games.append(game_dict)

    return games

#Part 1
def count_positions(moves: list[str], depth: int) -> int:
    """
    Recursively counts the number of legal move sequences of a given depth
    starting from the specified chess board state.

    Args:
        moves (list[str]): A list of moves in Standard Algebraic Notation (SAN)
            representing the current board state (empty list means starting position).
        depth (int): The number of additional moves (plies) to consider.

    Returns:
        int: The total number of valid move sequences of the specified depth.
    """

    # Base case: If depth is zero, there are no more moves to make.
    # There is exactly one sequence (the current position itself).
    if depth == 0:
        return 1

    # Initialize a counter to keep track of the total number of valid sequences.
    total_sequences = 0

    # Use binh_chess.possible_moves to get all legal next moves from the current position.
    # This returns a list of moves in SAN that are valid from the current board state.
    next_moves = possible_moves(moves)

    # For each legal next move, recursively count the number of valid sequences
    # that can be made from the new board state (after making this move),
    # with one fewer move to make (depth - 1).
    for move in next_moves:
        # Create a new move list by adding the current move to the history.
        new_move_history = moves + [move]

        # Recursively count all valid sequences from this new position with reduced depth.
        # Add the result to the running total.
        total_sequences += count_positions(new_move_history, depth - 1)

    # After considering all possible moves at this depth, return the total count.
    return total_sequences

#Part 2
def winning_statistics(file_name: str, depth: int, tolerance: int) -> tuple[float, list[str], int]:
    """
    Analyzes a PGN file to find the move sequence of specified depth with the highest white win probability,
    given a minimum number of games (tolerance) that follow the sequence.

    Args:
        file_name (str): Path to the PGN file containing chess games.
        depth (int): Number of moves (plies) in the sequence to analyze.
        tolerance (int): Minimum number of games required to consider a sequence valid.

    Returns:
        tuple[float, list[str], int]: A tuple containing:
            - Highest white win probability (0.0 if no valid sequence)
            - Move sequence achieving this probability (empty list if none)
            - Total games matching the sequence (0 if none)
    """

    # Read and parse the PGN file into a list of game dictionaries
    games = read_pgn(file_name)
    df = pd.DataFrame(games)

    def recursive_search(current_moves: list[str], current_depth: int) -> tuple[float, list[str], int]:
        """
        Recursively searches for the move sequence with the highest white win probability,
        given a minimum number of games (tolerance), starting from the current_moves sequence.

        Args:
            current_moves (list[str]): The current sequence of moves being considered.
            current_depth (int): The number of moves left to reach the target depth.

        Returns:
            tuple[float, list[str], int]: The best probability, the sequence, and the number of games.
        """

        # Build the list of column names corresponding to the moves in current_moves.
        # move_columns = []

        # for i in range(len(current_moves)):

        #     # If i is even, it's white's move in round (i//2)+1
        #     if i % 2 == 0:
        #         round_num = (i // 2) + 1
        #         move_columns.append(f'w{round_num}')

        #     # If i is odd, it's black's move in round (i//2)+1
        #     else:
        #         round_num = (i // 2) + 1
        #         move_columns.append(f'b{round_num}')

        # # Create a boolean mask to filter DataFrame rows matching the current move sequence
        # mask = pd.Series([True] * len(df))
        # for col, move in zip(move_columns, current_moves):
        #     mask &= (df[col] == move)
        # filtered_df = df[mask]

        # Determine how many moves we need to check in the sequence
        number_of_moves_to_check = len(current_moves)

        # Generate the corresponding column names for the moves list
        # Example: ['w1', 'b1', 'w2'] for moves ['e4', 'e5', 'Nf3']
        move_columns = []

        for move_index in range(number_of_moves_to_check):

            # Calculate which round (1-based) this move belongs to
            # First two moves (indices 0-1) are round 1, next two (2-3) are round 2, etc.
            round_number = (move_index // 2) + 1
            
            # Even indices (0, 2, 4...) are white moves (w1, w2, w3...)
            if move_index % 2 == 0:
                move_columns.append(f'w{round_number}')

            # Odd indices (1, 3, 5...) are black moves (b1, b2, b3...)
            else:
                move_columns.append(f'b{round_number}')

        # Initialize a boolean mask with all values True
        # This means all games are initially considered matches
        mask = pd.Series([True] * len(df))

        # Pair each move in the input list with its corresponding column name
        # Example: zip(['w1', 'b1', 'w2'], ['e4', 'e5', 'Nf3'])
        move_column_pairs = zip(move_columns, current_moves)

        # Refine the mask by checking each move in sequence
        for column_name, expected_move in move_column_pairs:

            # For each move-column pair:
            # 1. Check if the game's move in this column matches the expected move
            # 2. Combine with previous checks using logical AND (&)
            # This progressively filters out non-matching games
            mask = mask & (df[column_name] == expected_move)

        # Apply the final mask to get only games matching ALL moves
        filtered_games = df[mask]

        # =========================
        # BASE CASE: Target depth reached
        # =========================
        if current_depth == 0:
            # Count the number of games that match the current move sequence
            total_games = len(filtered_games)

            # Check if the number of games meets the minimum tolerance requirement
            if total_games >= tolerance:
                # Count how many of these games were won by white
                white_wins = filtered_games['result'].eq('1-0').sum()

                # Calculate the probability of white winning in these games
                probability = white_wins / total_games if total_games > 0 else 0.0

                # Return the probability, the move sequence, and the total number of games
                return (probability, current_moves.copy(), total_games)
            else:
                # If not enough games, return zero probability and an empty sequence
                return (0.0, [], 0)

        # =========================
        # RECURSION CASE: Explore next moves
        # =========================

        # Determine the next move index (how many moves have been played so far)
        next_move_index = len(current_moves)

        # Decide which column to use for the next move:
        # If the number of moves so far is even, it's white's turn
        # if next_move_index % 2 == 0:
        #     round_num = (next_move_index // 2) + 1
        #     next_col = f'w{round_num}'
        # # Otherwise, it's black's turn
        # else:
        #     round_num = (next_move_index // 2) + 1
        #     next_col = f'b{round_num}'

        # Calculate which round (1-based) next move belongs to
        round_number = (next_move_index // 2) + 1
        
        # Even indices (0, 2, 4...) are white moves (w1, w2, w3...)
        if move_index % 2 == 0:
            next_column = (f'w{round_number}')

        # Odd indices (1, 3, 5...) are black moves (b1, b2, b3...)
        else:
            next_column = (f'b{round_number}')

        # Get all unique possible next moves from the filtered games (excluding '-')
        possible_moves = []
        for move in filtered_games[next_column].unique():
            if move != '-':
                possible_moves.append(move)

        # Initialize variables to keep track of the best result found so far
        best_probability = 0.0
        best_sequence = []
        best_total = 0

        # Try each possible next move recursively
        for move in possible_moves:
            # Add the move to the current sequence
            current_moves.append(move)

            # Recursively search for the best sequence from this new position, reducing depth by 1
            probability, sequence, total = recursive_search(current_moves, current_depth - 1)

            # Remove the move after recursion to backtrack
            current_moves.pop()

            # Update the best result if this sequence is better
            if total >= tolerance:
                if probability > best_probability:
                    best_probability, best_sequence, best_total = probability, sequence, total

        # Return the best probability, sequence, and number of games found
        return (best_probability, best_sequence, best_total)


    # Initiate recursive search from empty starting sequence
    result = recursive_search([], depth)
    
    # Return formatted results if valid sequence found, otherwise return defaults
    if result[2] >= tolerance:
        return (round(result[0], 4), result[1], result[2])
    else:
        return (0.0, [], 0)


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    # your test code goes here
    # print(count_positions([], 1))
    # print(count_positions([], 2))

    # print(count_positions([], 3))

    # print(count_positions([], 4))
    # print(count_positions(['e4', 'e6', 'Nf3', 'd5', 'exd5', 'Qxd5', 'd4', 'Nc6', 'Nc3', 'Qd7', 'Be3', 'Nf6'], 3) == 55707)

    print(winning_statistics('lichess_small.pgn', 3, 5 ) == (1.0, ['d4', 'd6', 'c4'], 5))
# winning_statistics('lichess_small.pgn', 3, 6 ) == (0.8571428571428571, ['d4', 'd5', 'c4'], 21)
# winning_statistics('lichess_small.pgn', 3, 22) == (0.6585365853658537, ['e4', 'e5', 'Nf3'], 41)
# winning_statistics('lichess_small.pgn', 3, 42) == (0, [], 0)
    