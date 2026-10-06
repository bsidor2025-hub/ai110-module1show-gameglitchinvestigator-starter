import streamlit as st

from logic_utils import (
    apply_guess,
    attempts_left,
    get_attempt_limit,
    get_range_for_difficulty,
    new_game,
    parse_guess,
)

# --- Layer 3: presentation. All Streamlit code lives here. ---

# FIX (bug 1): the messages were swapped (a too-high guess said "Go HIGHER").
HINT_MESSAGES = {
    "too_high": "📉 Go LOWER!",
    "too_low": "📈 Go HIGHER!",
}

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {get_attempt_limit(difficulty)}")

# One game state, rebuilt whenever the difficulty changes.
if "game" not in st.session_state or st.session_state.game["difficulty"] != difficulty:
    st.session_state.game = new_game(difficulty)

game = st.session_state.game

st.subheader("Make a guess")

attempts_info = st.empty()


def show_attempts_info():
    attempts_info.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempts_left(st.session_state.game)}"
    )


debug_info = st.expander("Developer Debug Info")

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game_clicked = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game_clicked:
    # FIX (bug 3): swapping in a whole fresh game also clears the "lost" status.
    st.session_state.game = new_game(difficulty)
    st.rerun()

if submit and game["status"] == "playing":
    game, result = apply_guess(game, raw_guess)
    st.session_state.game = game

    if result == "invalid":
        st.error(parse_guess(raw_guess)[2])
    elif result in HINT_MESSAGES and show_hint:
        st.warning(HINT_MESSAGES[result])
    elif result == "won":
        st.balloons()
        st.success(
            f"You won! The secret was {game['secret']}. "
            f"Final score: {game['score']}"
        )
    elif result == "lost":
        st.error(
            f"Out of attempts! "
            f"The secret was {game['secret']}. "
            f"Score: {game['score']}"
        )
elif game["status"] == "won":
    st.success("You already won. Start a new game to play again.")
elif game["status"] == "lost":
    st.error("Game over. Start a new game to try again.")

# FIX (bug 2): the banner used to be drawn before the guess was processed, so it
# showed a stale count (1 left) next to the out-of-attempts message. Drawing it
# here, after the turn, keeps it in sync.
show_attempts_info()

with debug_info:
    st.write("Secret:", game["secret"])
    st.write("Attempts:", game["attempts"])
    st.write("Score:", game["score"])
    st.write("Difficulty:", difficulty)
    st.write("History:", game["history"])

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
