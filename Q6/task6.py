"""
Provides functions for parsing chess PGN files and performing statistical analysis
on chess games, including win/loss statistics by opening, ELO difference, and move
sequences. Uses pandas for efficient data handling and supports flexible queries
on chess datasets for research and reporting.

Author : Szeto Lok
"""

import re
import pandas as pd
import re


def read_pgn(file_name: str) -> list[dict]:
    """
    Reads a PGN file and returns a list of dictionaries representing games.
    Each dictionary contains 7 tags and up to 20 moves for white and black.

    Args:
        file_name (str): Path to the PGN file.

    Returns:
        list[dict]: List of game dictionaries with keys as specified in part1.txt.
    """

    games = []  # This will hold all parsed games as dictionaries.

    # These are the tags (metadata) we want to extract from each game.
    required_tags = ['event', 'white', 'black', 'result', 'whiteelo', 'blackelo', 'opening']

    # Open the PGN file for reading.
    with open(file_name, 'r', encoding='utf-8') as file:
        # Read all lines from the file into a list.
        lines = file.readlines()

    # Initialize a pointer to track which line we're on.
    current_line_index = 0

    # Store the total number of lines for easy bounds checking.
    total_lines = len(lines)

    # Loop through the file until we've processed all lines.
    while current_line_index < total_lines:

        # Skip any blank lines before the start of a game.
        while current_line_index < total_lines and lines[current_line_index].strip() == '':
            current_line_index += 1

        # If we've reached the end of the file, stop processing.
        if current_line_index >= total_lines:
            break

        # --- Parse the tag section for this game ---

        # This will store the tags for the current game.
        tags = {}  

        # Loop through lines that start with '[' (these are tag lines).
        while current_line_index < total_lines and lines[current_line_index].startswith('['):
            line = lines[current_line_index].strip()

            # Try to match the line to the pattern [TagName "Value"]
            match = re.match(r'\[([a-zA-Z]+)\s+"(.*)"\]', line)

            if match:

                # Extract the tag and its value.
                tag, value = match.groups() 
                
                # Store the tag in lowercase for consistency.
                tags[tag.lower()] = value    

            # Move to the next line.
            current_line_index += 1  

        # Skip any blank lines between the tags and the moves.
        while current_line_index < total_lines and lines[current_line_index].strip() == '':
            current_line_index += 1

        # --- Parse the moves section for this game ---

        # This will accumulate all the moves for the current game.
        moves_str = ''  

        # Keep reading lines until we hit a new tag section or a blank line.
        while current_line_index < total_lines and not lines[current_line_index].startswith('[') and lines[current_line_index].strip() != '':
            
            # Add this line's moves to our moves string, separated by a space.
            moves_str += ' ' + lines[current_line_index].strip()
            current_line_index += 1

        # Remove any leading/trailing whitespace from the moves string.
        moves_str = moves_str.strip()

        # Remove the game result (like "1-0", "0-1", "1/2-1/2") from the end if present.
        moves_str = re.sub(r'\s*(1-0|0-1|1/2-1/2)\s*$', '', moves_str)

        # Split the moves string into individual tokens (numbers and moves).
        move_tokens = moves_str.split()

        # --- Prepare the output dictionary for this game ---

        # This will store all info for this game.
        game_dict = {}  

        # Add all required tags to the game dictionary.
        # If a tag is missing, use '?' as a placeholder.
        for tag in required_tags:
            game_dict[tag] = tags.get(tag, '?')

        # Initialize all move slots for 20 rounds (w1, b1, ..., w20, b20) to '-'
        for round_number in range(1, 21):
            game_dict[f'w{round_number}'] = '-'
            game_dict[f'b{round_number}'] = '-'

        # --- Extract moves into w1, b1, ..., w20, b20 ---

        # This keeps track of which round we're on (1-based).
        current_round = 1  

        # This keeps track of our position in move_tokens.
        move_token_index = 0 

        # Process up to 20 rounds of moves (white and black).
        while move_token_index < len(move_tokens) and current_round <= 20:

            # Look for a move number token (like "1.")
            if re.match(r'^\d+\.$', move_tokens[move_token_index]):

                # Skip the move number token.
                move_token_index += 1 

                # If the next token is a move (not another number), assign to white.
                if move_token_index < len(move_tokens) and not re.match(r'^\d+\.$', move_tokens[move_token_index]):
                    game_dict[f'w{current_round}'] = move_tokens[move_token_index]
                    move_token_index += 1

                # If the next token is a move (not another number), assign to black.
                if move_token_index < len(move_tokens) and not re.match(r'^\d+\.$', move_tokens[move_token_index]):
                    game_dict[f'b{current_round}'] = move_tokens[move_token_index]
                    move_token_index += 1

                # Move to the next round.
                current_round += 1

            else:

                # If the token is not a move number, skip it (defensive programming).
                move_token_index += 1

        # Add the fully parsed game dictionary to the list of games.
        games.append(game_dict)

    # Once all games are processed, return the list of game dictionaries.
    return games


# Part 2
def win_loss_by_opening(games: list[dict]) -> dict:
    """
    Analyzes chess games to count white/black wins per opening using pandas.
    
    Args:
        games (list[dict]): List of game dictionaries from read_pgn()
        
    Returns:
        dict: {opening_name: (white_wins, black_wins)}
    """

    # Convert list of game dictionaries to pandas DataFrame
    df = pd.DataFrame(games)

    # Filter DataFrame to only games where white won ('1-0')
    # Then group by 'opening' and count occurrences for each opening
    white_wins = df[df['result'] == '1-0'].groupby('opening').size()
    
    # Filter DataFrame to only games where black won ('0-1')
    # Then group by 'opening' and count occurrences for each opening
    black_wins = df[df['result'] == '0-1'].groupby('opening').size()

    # Get all unique opening names from the dataset
    # Using a set ensures we don't miss openings with only draws/losses
    all_openings = set(df['opening'])
    
    # Initialize empty dictionary to store results
    result = {}

    # Populate the result dictionary
    for opening in all_openings:

        # Get white win count (0 if opening not found in white_wins)
        white_count = white_wins.get(opening, 0)

        # Get black win count (0 if opening not found in black_wins)
        black_count = black_wins.get(opening, 0)
        
        # Convert numpy.int64 to native Python int for cleaner output
        result[opening] = (int(white_count), int(black_count))

    return result


#Part 3
def win_loss_by_elo(games: list[dict], lower: int, upper: int) -> tuple[int, int]:
    """
    Uses pandas to count wins by lower and higher ELO players in games where the
    absolute ELO difference is in (lower, upper).

    Args:
        games (list[dict]): List of game dicts from read_pgn.
        lower (int): Lower bound (exclusive) for ELO difference.
        upper (int): Upper bound (exclusive) for ELO difference.

    Returns:
        tuple: (lower_elo_wins, higher_elo_wins)
    """

    # Convert list of game dictionaries to pandas DataFrame for efficient processing
    df = pd.DataFrame(games)

    # Convert ELO strings to numeric values, invalid values become NaN
    # This handles cases where ELO might be '?' or other non-numeric values
    df['whiteelo'] = pd.to_numeric(df['whiteelo'], errors='coerce')
    df['blackelo'] = pd.to_numeric(df['blackelo'], errors='coerce')

    # Remove games with missing ELO values (NaN) from either player
    # These games can't be used for ELO comparison analysis
    df = df.dropna(subset=['whiteelo', 'blackelo'])

    # Calculate absolute ELO difference between players
    # This represents the skill gap regardless of which player is higher rated
    df['elo_diff'] = (df['whiteelo'] - df['blackelo']).abs()

    # Filter to only games where ELO difference falls within specified range
    df = df[(df['elo_diff'] > lower) & (df['elo_diff'] < upper)]

    # Create boolean flag indicating if white player is the lower-rated player
    df['lower_is_white'] = df['whiteelo'] < df['blackelo']

    # Calculate lower ELO wins:
    # - Either white is lower rated and won (1-0)
    # - Or black is lower rated and won (0-1)
    lower_elo_wins = (
        (df['lower_is_white'] & (df['result'] == '1-0')) |  # White underdog win
        (~df['lower_is_white'] & (df['result'] == '0-1'))   # Black underdog win
    ).sum()

    # Calculate higher ELO wins:
    # - Either white is higher rated and won (1-0)
    # - Or black is higher rated and won (0-1)
    higher_elo_wins = (
        (~df['lower_is_white'] & (df['result'] == '1-0')) |  # White favorite win
        (df['lower_is_white'] & (df['result'] == '0-1'))     # Black favorite win
    ).sum()

    # Convert numpy ints to Python native ints for clean return
    return int(lower_elo_wins), int(higher_elo_wins)


#Part 4
def win_loss_by_moves(games: list[dict], moves: list[str]) -> tuple[int, int]:
    """
    Counts the number of games won by white and black for games that start with the given sequence of moves.

    Args:
        games (list[dict]): List of game dictionaries as produced by read_pgn.
        moves (list[str]): List of moves (alternating white/black) to match at the start of each game.

    Returns:
        tuple[int, int]: (white_win_count, black_win_count)
            - white_win_count: Number of games won by white.
            - black_win_count: Number of games won by black.
    """

    # Convert the list of game dictionaries to a pandas DataFrame
    # This allows efficient column-wise operations and filtering
    df = pd.DataFrame(games)

    # Determine how many moves we need to check in the sequence
    number_of_moves_to_check = len(moves)

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
    move_column_pairs = zip(move_columns, moves)

    # Refine the mask by checking each move in sequence
    for column_name, expected_move in move_column_pairs:

        # For each move-column pair:
        # 1. Check if the game's move in this column matches the expected move
        # 2. Combine with previous checks using logical AND (&)
        # This progressively filters out non-matching games
        mask = mask & (df[column_name] == expected_move)

    # Apply the final mask to get only games matching ALL moves
    filtered_games = df[mask]

    # Count white wins (result == '1-0') in the filtered games
    # .sum() works because True = 1, False = 0 in numeric context
    white_wins = (filtered_games['result'] == '1-0').sum()

    # Count black wins (result == '0-1') in the filtered games
    black_wins = (filtered_games['result'] == '0-1').sum()

    # Convert numpy.int64 to native Python int and return
    return int(white_wins), int(black_wins)

# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    # your test code goes here
    game = read_pgn('Q6/own_example.pgn')

    # print(game)
    # game2 = read_pgn('Q6/example.pgn')
    # result = win_loss_by_opening(game2)

    game = read_pgn('Q6/lichess_small.pgn')

    result = win_loss_by_elo(game, 0, 600)
    print(result)

    result = win_loss_by_elo(game, 0, 400)
    print(result)
    
    result = win_loss_by_elo(game, 0, 200)
    print(result)

    result = win_loss_by_elo(game, 0, 100)
    print(result)

    result = win_loss_by_elo(game, 400, 600)
    print(result)

    game = read_pgn('Q6/example.pgn')
    # print(game)
    print(win_loss_by_moves(game, ['e4', 'e5', 'Nf3', 'Nc6']))
    print(win_loss_by_moves(game, ['e4', 'e5', 'Nf3']))