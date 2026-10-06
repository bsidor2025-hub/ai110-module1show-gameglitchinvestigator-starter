# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Game purpose:** Glitchy Guesser is a Streamlit number-guessing game. The player picks a difficulty (Easy 1-20, Normal 1-100, Hard 1-50), guesses the secret number within a limited number of attempts, and gets a higher/lower hint after each guess. A score rewards winning quickly.
- [x] **Bugs found:**
  1. **Wrong hints:** the "Go HIGHER" / "Go LOWER" messages were swapped, and on alternating attempts the secret was converted to a string, so guesses were compared as text (`"9" > "10"`).
  2. **Attempts mismatch:** the UI said the player was out of attempts while the header still showed 1 attempt left. Attempts started at 1, and the "Attempts left" banner was drawn before the guess was processed, so it was stale.
  3. **New Game button broken after a loss:** it reset only the attempts and the secret, so the game stayed in the "lost" state and never restarted.
- [x] **Fixes applied:**
  1. Swapped the hint messages back and always compare ints, with no string fallback.
  2. Attempts now start at 0, and the banner is drawn after the guess is processed.
  3. New Game builds a whole fresh game (status, score and history too) and the game also resets when the difficulty changes.
  4. Refactored the code into layers: rules and turn logic in `logic_utils.py` (no Streamlit), and only the UI in `app.py`.
  5. Added 11 pytest tests, including a regression test for each bug.

## 📸 Demo Walkthrough

A sample game on **Normal** difficulty (range 1-100, 8 attempts), where the secret number is 57. The score starts at 0.

1. The player opens the game. The banner reads "Guess a number between 1 and 100. Attempts left: 8".
2. The player enters **40** and clicks Submit. The game shows "📈 Go HIGHER!" (the guess is too low), the score drops to **-5**, and the banner updates to "Attempts left: 7".
3. The player enters **50**. The game shows "📈 Go HIGHER!" again, the score drops to **-10**, and attempts left is **6**.
4. The player enters **70**. The game shows "📉 Go LOWER!" (the guess is too high), the score drops to **-15**, and attempts left is **5**.
5. The player enters **57**. The game shows the balloons and "You won! The secret was 57. Final score: 35", and the score rises by 50 for winning on attempt 4.
6. Submitting again shows "You already won. Start a new game to play again."
7. The player clicks **New Game**. The attempts, score and history reset, and a new secret is chosen. The banner is back to "Attempts left: 8".

**Losing instead:** if the player uses all 8 attempts without guessing the secret, the game shows "Out of attempts! The secret was …" with "Attempts left: 0" in the banner. The New Game button then starts a fresh game as in step 7.

## 🧪 Test Results

```
$ python -m pytest -v
============================= test session starts =============================
platform win32 -- Python 3.14.5, pytest-9.1.1, pluggy-1.6.0
collecting ... collected 11 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  9%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 18%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 27%]
tests/test_game_logic.py::test_numeric_comparison_not_string_comparison PASSED [ 36%]
tests/test_game_logic.py::test_hints_are_consistent_across_attempts PASSED [ 45%]
tests/test_game_logic.py::test_difficulty_settings PASSED                [ 54%]
tests/test_game_logic.py::test_attempts_left_hits_zero_when_lost PASSED  [ 63%]
tests/test_game_logic.py::test_new_game_after_loss_resets_everything PASSED [ 72%]
tests/test_game_logic.py::test_win_ends_the_game PASSED                  [ 81%]
tests/test_game_logic.py::test_invalid_input_is_reported PASSED          [ 90%]
tests/test_game_logic.py::test_apply_guess_does_not_mutate_input_state PASSED [100%]

============================= 11 passed in 0.04s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
