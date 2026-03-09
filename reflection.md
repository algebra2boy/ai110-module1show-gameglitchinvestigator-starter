# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the app, the game was unplayable in several ways. The most obvious bug was that the hints were completely backwards: if I guessed too high, the game told me to "Go HIGHER!", and if I guessed too low, it said "Go LOWER!" — the opposite of useful. A second bug appeared on every other guess: the secret number was secretly being converted to a string before comparison, so Python would compare, for example, `9 > "50"` as `True` (because `"9" > "5"` lexicographically), giving completely wrong hints on even-numbered attempts. A third bug was that the attempts counter started at 1 instead of 0, meaning the very first guess was counted as attempt 2 and the "Attempts left" display was always off by one. A fourth issue was that the info banner always said "Guess a number between 1 and 100" regardless of which difficulty you selected — on Easy the range is 1–20, so the message was misleading. Finally, all four game logic functions in `logic_utils.py` raised `NotImplementedError`, so the tests could never run at all.

---

## 2. How did you use AI as a teammate?

I used Claude Code (Claude Sonnet 4.6 via the VS Code extension) as my primary AI assistant throughout this project. One correct and helpful suggestion was identifying the exact line where the string-cast happened (`if st.session_state.attempts % 2 == 0: secret = str(st.session_state.secret)`) and explaining that Python string comparison is lexicographic, so `"9" > "50"` evaluates to `True` — this matched exactly what I was seeing in the game and I verified it by running the fixed version and confirming hints were correct on both odd and even attempts. One misleading suggestion came when I asked about the score logic: the AI initially suggested the `update_score` function's even-attempt bonus for "Too High" was intentional "risk/reward" game design rather than a bug, so I kept it as-is rather than removing it — I verified this was acceptable by re-reading the assignment brief, which only required fixing the broken hints and string-comparison issues. I verified every fix by running `pytest tests/` and confirming all tests passed, then also playing the game in the browser to confirm the hints were correct.

---

## 3. Debugging and testing your fixes

I decided a bug was truly fixed when two things were true: a pytest test specifically targeting that bug passed, and I could reproduce the correct behaviour by playing the game manually in the browser. For the inverted hints fix, I wrote `test_too_high_hint_says_go_lower` which asserts that `check_guess(60, 50)` returns an outcome of `"Too High"` and a message containing `"LOWER"` — before the fix this test failed, and after it passed. For the string-comparison bug, I wrote `test_integer_secret_always_used` which calls `check_guess(9, 50)` and expects `"Too Low"` — this would have returned `"Too High"` under the old string comparison (`"9" > "50"` is `True`). Claude helped me understand why `result == "Win"` in the original tests was always `False` (because `check_guess` returns a tuple, not a string) and suggested changing the assertions to `result[0] == "Win"`.

---

## 4. What did you learn about Streamlit and state?

Streamlit reruns the entire Python script from top to bottom every time a user interacts with the app — clicking a button, typing in a box, or changing a dropdown all trigger a full re-execution. Without `st.session_state`, any variable you define in the script (like the secret number or the attempt count) gets reset to a fresh value on every rerun, which is why the original game appeared to "forget" things between clicks. `st.session_state` is a dictionary-like object that persists across reruns within the same browser session, so you store important values there (e.g., `st.session_state.secret`) and check `if "secret" not in st.session_state` before initialising them so they only get set once. A friend analogy: imagine you're helping a customer at a counter, but every time they speak you forget everything — `st.session_state` is the notepad you keep on the counter so you remember their order between questions.

---

## 5. Looking ahead: your developer habits

One habit I want to carry forward is writing a failing test *before* applying a fix — by writing `test_too_high_hint_says_go_lower` first and watching it fail, I confirmed the bug was real, then watched it pass after my fix, giving me confidence the repair was correct. One thing I would do differently next time is be more skeptical when an AI says "this is intentional design" — the `update_score` even-attempt bonus felt suspicious, and I should have probed it further rather than accepting the AI's framing. This project changed how I think about AI-generated code: the AI produced working-looking code that was full of subtle logic errors that only surface when you actually play the game, which taught me that AI output always needs a human to reason about the *intent* of the code, not just its syntax.
