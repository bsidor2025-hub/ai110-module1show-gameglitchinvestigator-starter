# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
A: At first the game looked like it was working. The problem showed up when I guessed past the secret number: the game kept telling me to go higher. Either the hint logic is wrong or the function that decides "Go higher" or "Go lower" is returning the wrong result.
- List at least two concrete bugs you noticed at the start  
  1. The hints were wrong: after guessing above the secret number, the game still said "Go higher."
  2. The UI and the backend information conflicted: the UI said I was out of attempts even though the header still showed one attempt left.
  3. The new game button did not work after I ran out of attempts.
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess a number higher than the secret number | The hint says "Go lower" | The hint keeps saying "Go higher" | No error shown |
| Play until the last attempt | The header's attempts count and the out-of-attempts message agree | The UI says I'm out of attempts while the header still shows 1 attempt left | No error shown |
| Use up all attempts, then click the new game button | The game resets and I can play again | The new game button does not restart the game | No error shown |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
A: Claude Code in VS code
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
A: that bug #1 was a logical bug where the function responsible said Go Higher or Go Lower on inverted cases; I then cheked the actual code and it matched what the AI described.
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
A: when I talked to Claude about the functions mixes it clearly outlined them and suggested to put the UI concerning ones in a new file; I expanded its idea to separate all the functions into the clearly distinct layers.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
A: I repeated the exact steps from my Bug Reproduction Log and checked that the expected behavior now happened: the hints matched the guess, the attempts counter agreed with the game-over message, and New Game started a fresh game after a loss. I also wrote a pytest regression test for each bug, so a fix only counted if its test passed.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
A: I ran `python -m pytest` and all 11 tests passed. One of them, `test_attempts_left_hits_zero_when_lost`, plays every attempt and checks that the game is lost and attempts left is 0. It showed me the attempts bug came from game logic (the counter started at 1) as well as from the display. The original tests had passed even though the game was broken, because they only checked the outcome strings and never the hint messages.
- Did AI help you design or understand any tests? How?
A: Yes. Claude pointed out why the original tests missed the bugs and wrote regression tests for each fixed bug, including a check that the hints stay correct across many attempts. It also ran the app through Streamlit's AppTest to simulate a full game. I read the tests to confirm each one matched the bug it was meant to catch.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
