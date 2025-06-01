import re
import pandas as pd

import re
from itertools import groupby
from typing import List, Dict

# def read_pgn(file_name: str) -> list[dict]:
#     """
#     Reads a PGN file and returns a list of game dictionaries.
#     Uses itertools.groupby to separate games by blank lines.
#     """
#     required_tags = ['event', 'white', 'black', 'result', 'whiteelo', 'blackelo', 'opening']
#     games = []
    
#     # with open(file_name, 'r', encoding='utf-8') as f:
#     #     # Group lines into game blocks separated by blank lines
#     #     grouped = groupby(f, key=lambda line: line.strip() == '')
        
#     #     for is_blank, group in grouped:
#     #         if not is_blank:
#     with open(file_name, 'r', encoding='utf-8') as f:
#             file_content = f.read()

#     # Split the file into blocks, each representing a game
#     game_blocks = [block.strip() for block in file_content.split('\n\n') if block.strip()]

#     games = []
#     for game_block in game_blocks:
#         lines = game_block.split('\n')
#         # game_lines = [line.strip() for line in group]
#         game_dict = parse_game(lines, required_tags)
#         games.append(game_dict)
    
#     return games

# def parse_game(lines: List[str], required_tags: List[str]) -> Dict:
#     """Parses a single game's lines into a dictionary."""
#     tags = parse_tags(lines)
#     moves_str = extract_moves(lines)
#     return build_game_dict(tags, moves_str, required_tags)

# def parse_tags(lines: List[str]) -> Dict:
#     """Extracts tags from game lines."""
#     tags = {}
#     for line in lines:
#         if not line.startswith('['):
#             break
#         match = re.match(r'\[(\w+)\s+"(.*)"\]', line)
#         if match:
#             tag, value = match.groups()
#             tags[tag.lower()] = value
#     return tags

# def extract_moves(lines: List[str]) -> str:
#     """Extracts and concatenates move lines."""
#     moves = []
#     in_moves = False
    
#     for line in lines:
#         if not line.startswith('['):
#             in_moves = True
#         if in_moves:
#             moves.append(line)
    
#     return ' '.join(moves).strip()

# def build_game_dict(tags: Dict, moves_str: str, required_tags: List[str]) -> Dict:
#     """Builds the final game dictionary with moves."""
#     game_dict = {tag: tags.get(tag, '?') for tag in required_tags}
    
#     # Initialize all move fields to '-'
#     for i in range(1, 21):
#         game_dict[f'w{i}'] = '-'
#         game_dict[f'b{i}'] = '-'
    
#     # Process move tokens
#     move_tokens = re.sub(r'\s*(1-0|0-1|1/2-1/2)\s*$', '', moves_str).split()
#     current_round = 1
#     token_idx = 0
    
#     while token_idx < len(move_tokens) and current_round <= 20:
#         if re.match(r'^\d+\.$', move_tokens[token_idx]):
#             token_idx += 1  # Skip move number
            
#             # White's move
#             if token_idx < len(move_tokens) and not re.match(r'^\d+\.', move_tokens[token_idx]):
#                 game_dict[f'w{current_round}'] = move_tokens[token_idx]
#                 token_idx += 1
                
#             # Black's move
#             if token_idx < len(move_tokens) and not re.match(r'^\d+\.', move_tokens[token_idx]):
#                 game_dict[f'b{current_round}'] = move_tokens[token_idx]
#                 token_idx += 1
                
#             current_round += 1
#         else:
#             token_idx += 1
    
#     return game_dict


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