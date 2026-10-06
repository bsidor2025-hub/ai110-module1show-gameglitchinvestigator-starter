import random

# --- Layer 1: rules (no Streamlit, no state) ---

DIFFICULTY_SETTINGS = {
    "Easy": {"range": (1, 20), "attempt_limit": 6},
    "Normal": {"range": (1, 100), "attempt_limit": 8},
    "Hard": {"range": (1, 50), "attempt_limit": 5},
}
DEFAULT_DIFFICULTY = "Normal"


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    return DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS[DEFAULT_DIFFICULTY])["range"]


def get_attempt_limit(difficulty: str):
    """Return how many attempts a given difficulty allows."""
    return DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS[DEFAULT_DIFFICULTY])["attempt_limit"]


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome.

    outcome: "Win", "Too High", "Too Low"
    """
    # FIX (bug 1): the secret used to be turned into a string on alternating
    # attempts, so this compared int to str and fell back to text ordering
    # ("9" > "10"). Both values are now always ints.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score


# --- Layer 2: game state and turn logic (no Streamlit) ---

def new_game(difficulty: str):
    """Return a fresh game state for the given difficulty."""
    low, high = get_range_for_difficulty(difficulty)
    # FIX (bug 2): attempts used to start at 1, so "attempts left" was off by one.
    # FIX (bug 3): New Game used to reset only attempts and secret, leaving status
    # as "lost"; building the whole state here resets everything at once.
    return {
        "difficulty": difficulty,
        "secret": random.randint(low, high),
        "attempts": 0,
        "score": 0,
        "status": "playing",
        "history": [],
    }


def attempts_left(state: dict):
    """Return how many attempts remain in the game."""
    return get_attempt_limit(state["difficulty"]) - state["attempts"]


def apply_guess(state: dict, raw: str):
    """
    Play one turn. Returns (new_state, result).

    result: "finished", "invalid", "too_high", "too_low", "won" or "lost".
    The input state is not modified.
    """
    if state["status"] != "playing":
        return state, "finished"

    state = {**state, "history": list(state["history"])}
    state["attempts"] += 1

    ok, guess, _ = parse_guess(raw)
    if not ok:
        state["history"].append(raw)
        result = "invalid"
    else:
        state["history"].append(guess)
        outcome = check_guess(guess, state["secret"])
        state["score"] = update_score(state["score"], outcome, state["attempts"])
        if outcome == "Win":
            result = "won"
        elif outcome == "Too High":
            result = "too_high"
        else:
            result = "too_low"

    if result == "won":
        state["status"] = "won"
    elif attempts_left(state) <= 0:
        state["status"] = "lost"
        result = "lost"

    return state, result
