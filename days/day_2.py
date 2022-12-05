ROCK = "R"
PAPER = "P"
SCISSORS = "S"

DRAW = 0
P1_WIN = 1
P1_LOSE = -1

GAME_MAP = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS,
    "X": ROCK,
    "Y": PAPER,
    "Z": SCISSORS,
}

OUTCOME_MAP = {
    "X": P1_WIN,
    "Y": DRAW,
    "Z": P1_LOSE,
}

MATCH_MAP = {
    ROCK+ROCK: 0,
    ROCK+PAPER: -1,
    ROCK+SCISSORS: 1,
    PAPER+ROCK: 1,
    PAPER+PAPER: 0,
    PAPER+SCISSORS: -1,
    SCISSORS+ROCK: -1,
    SCISSORS+PAPER: 1,
    SCISSORS+SCISSORS: 0,
}

SCORE_MAP = {
    ROCK: 1,
    PAPER: 2,
    SCISSORS: 3,
    DRAW: 3,
    P1_WIN: 0,
    P1_LOSE: 6,
}


def rps_match(p1_move, p2_move):
    p1_s_move = GAME_MAP[p1_move]
    p2_s_move = GAME_MAP[p2_move]

    result = MATCH_MAP[p1_s_move+p2_s_move]

    score = SCORE_MAP[result] + SCORE_MAP[p2_s_move]
    return score


def rps_outcome_plan(p1_move, p2_move):
    p1_s_move = GAME_MAP[p1_move]
    expected_result = OUTCOME_MAP[p2_move]

    for move in [ROCK, PAPER, SCISSORS]:
        result = MATCH_MAP[p1_s_move+move]
        if result == expected_result:
            score = SCORE_MAP[result] + SCORE_MAP[move]
            return score


def run_matches(data):
    total_score = 0
    for match in data:
        p1_move, p2_move = match.split(" ")
        total_score += rps_match(p1_move, p2_move)

    return total_score


def run_planned_matches(data):
    total_score = 0
    for match in data:
        p1_move, p2_move = match.split(" ")
        total_score += rps_outcome_plan(p1_move, p2_move)

    return total_score


###############################################################################
def run_a(input_data):
    total_score = run_matches(input_data)
    return total_score


def run_b(input_data):
    total_score = run_planned_matches(input_data)
    return total_score
