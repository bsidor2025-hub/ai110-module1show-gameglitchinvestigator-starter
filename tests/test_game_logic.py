from logic_utils import (
    apply_guess,
    attempts_left,
    check_guess,
    get_attempt_limit,
    get_range_for_difficulty,
    new_game,
)


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    assert check_guess(50, 50) == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    assert check_guess(60, 50) == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    assert check_guess(40, 50) == "Too Low"


def test_numeric_comparison_not_string_comparison():
    # Regression: "9" > "10" as strings, but 9 < 10 as numbers
    assert check_guess(9, 10) == "Too Low"


def test_hints_are_consistent_across_attempts():
    # Regression: hints used to break on alternating attempts
    state = new_game("Normal")
    state["secret"] = 50
    results = []
    for _ in range(4):
        state, result = apply_guess(state, "60")
        results.append(result)
    assert results == ["too_high"] * 4


def test_difficulty_settings():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_attempt_limit("Hard") == 5


def test_attempts_left_hits_zero_when_lost():
    # Regression: attempts left must agree with the game-over state
    state = new_game("Hard")
    state["secret"] = 50
    for _ in range(get_attempt_limit("Hard")):
        state, result = apply_guess(state, "1")
    assert result == "lost"
    assert state["status"] == "lost"
    assert attempts_left(state) == 0


def test_new_game_after_loss_resets_everything():
    # Regression: New Game used to leave the status as "lost"
    state = new_game("Hard")
    state["secret"] = 50
    for _ in range(get_attempt_limit("Hard")):
        state, _ = apply_guess(state, "1")
    fresh = new_game("Hard")
    assert fresh["status"] == "playing"
    assert fresh["attempts"] == 0
    assert fresh["score"] == 0
    assert fresh["history"] == []


def test_win_ends_the_game():
    state = new_game("Normal")
    state["secret"] = 42
    state, result = apply_guess(state, "42")
    assert result == "won"
    assert state["status"] == "won"


def test_invalid_input_is_reported():
    state = new_game("Normal")
    state, result = apply_guess(state, "abc")
    assert result == "invalid"


def test_apply_guess_does_not_mutate_input_state():
    state = new_game("Normal")
    apply_guess(state, "5")
    assert state["attempts"] == 0
    assert state["history"] == []
