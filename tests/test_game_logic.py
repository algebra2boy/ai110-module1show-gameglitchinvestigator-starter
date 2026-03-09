from logic_utils import check_guess, parse_guess, get_range_for_difficulty

# --- Existing tests (fixed: check_guess returns a tuple, so check index 0) ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result[0] == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, outcome should be "Too High"
    result = check_guess(60, 50)
    assert result[0] == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, outcome should be "Too Low"
    result = check_guess(40, 50)
    assert result[0] == "Too Low"

# --- New tests targeting fixed bugs ---

def test_too_high_hint_says_go_lower():
    # Bug fix: "Too High" used to say "Go HIGHER!" — now it must say "Go LOWER!"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_too_low_hint_says_go_higher():
    # Bug fix: "Too Low" used to say "Go LOWER!" — now it must say "Go HIGHER!"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_integer_secret_always_used():
    # Bug fix: secret was cast to str on even attempts, causing wrong comparisons.
    # e.g. str comparison "9" > "50" is True, giving wrong hint.
    # With integer secrets, 9 < 50 should correctly return "Too Low".
    outcome, _ = check_guess(9, 50)
    assert outcome == "Too Low"

def test_parse_guess_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_guess_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_guess_non_number():
    ok, value, err = parse_guess("abc")
    assert ok is False

def test_hard_range_harder_than_normal():
    # Bug fix: Hard used to return 1-50 (easier than Normal's 1-100).
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high
