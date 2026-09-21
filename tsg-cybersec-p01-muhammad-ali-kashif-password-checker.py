import getpass
import re
import string
from pathlib import Path


# ==========================================
# DATASET
# ==========================================

DATASET_FILE = Path(__file__).parent / "data" / "common_passwords.txt"


def load_common_passwords():
    """Load common passwords from the dataset."""

    if not DATASET_FILE.exists():
        print("Warning: common_passwords.txt not found.")
        return set()

    with open(DATASET_FILE, "r", encoding="utf-8") as file:
        return {
            line.strip().lower()
            for line in file
            if line.strip()
        }


COMMON_PASSWORDS = load_common_passwords()


# ==========================================
# PREDICTABILITY CHECK
# ==========================================

def check_predictability(password):

    problems = []
    lower_password = password.lower()

    # --------------------------------------
    # Sequential numbers
    # --------------------------------------

    number_sequences = [
        "0123",
        "1234",
        "2345",
        "3456",
        "4567",
        "5678",
        "6789"
    ]

    for sequence in number_sequences:
        if sequence in lower_password:
            problems.append(
                f"Sequential number pattern detected: {sequence}"
            )
            break

    # --------------------------------------
    # Sequential letters
    # --------------------------------------

    letter_sequences = [
        "abcd",
        "bcde",
        "cdef",
        "defg",
        "efgh",
        "fghi",
        "ghij",
        "wxyz"
    ]

    for sequence in letter_sequences:
        if sequence in lower_password:
            problems.append(
                f"Sequential letter pattern detected: {sequence}"
            )
            break

    # --------------------------------------
    # Repeated characters
    # --------------------------------------

    if re.search(r"(.)\1\1", password):
        problems.append(
            "Repeated character pattern detected."
        )

    # --------------------------------------
    # Keyboard patterns
    # --------------------------------------

    keyboard_patterns = [
        "qwerty",
        "asdf",
        "zxcv",
        "qaz",
        "wsx"
    ]

    for pattern in keyboard_patterns:
        if pattern in lower_password:
            problems.append(
                f"Keyboard pattern detected: {pattern}"
            )
            break

    # --------------------------------------
    # Common words
    # --------------------------------------

    common_words = [
        "password",
        "admin",
        "welcome",
        "login",
        "user",
        "letmein",
        "monkey",
        "dragon"
    ]

    for word in common_words:
        if word in lower_password:
            problems.append(
                f"Predictable word detected: {word}"
            )
            break

    return problems


# ==========================================
# PASSWORD CHECKER
# ==========================================

def check_password(password):

    feedback = []

    length = len(password)

    has_lowercase = any(
        char.islower() for char in password
    )

    has_uppercase = any(
        char.isupper() for char in password
    )

    has_number = any(
        char.isdigit() for char in password
    )

    has_special = any(
        char in string.punctuation
        for char in password
    )

    # ======================================
    # LENGTH SCORE — 40 POINTS
    # ======================================

    if length >= 16:
        length_score = 40

    elif length >= 12:
        length_score = 30
        feedback.append(
            "Use at least 16 characters for stronger protection."
        )

    elif length >= 8:
        length_score = 20
        feedback.append(
            "Use at least 12 characters; 16 or more is recommended."
        )

    else:
        length_score = 10
        feedback.append(
            "Password is too short. Use at least 12 characters."
        )

    # ======================================
    # CHARACTER VARIETY — 40 POINTS
    # ======================================

    variety_score = 0

    if has_lowercase:
        variety_score += 10
    else:
        feedback.append("Add lowercase letters.")

    if has_uppercase:
        variety_score += 10
    else:
        feedback.append("Add uppercase letters.")

    if has_number:
        variety_score += 10
    else:
        feedback.append("Add numbers.")

    if has_special:
        variety_score += 10
    else:
        feedback.append(
            "Add special characters such as !, @, #, or $."
        )

    # ======================================
    # COMMON PASSWORD CHECK — 10 POINTS
    # ======================================

    is_common = password.lower() in COMMON_PASSWORDS

    if is_common:

        common_score = 0

        feedback.append(
            "This password appears in the common-password "
            "dataset. Replace it with a unique password."
        )

    else:

        common_score = 10

    # ======================================
    # PREDICTABILITY
    # ======================================

    predictability_problems = check_predictability(
        password
    )

    # Start with maximum 10 points.
    predictability_score = 10

    if predictability_problems:

        # Each detected issue removes 5 points.
        penalty = len(predictability_problems) * 5

        predictability_score = max(
            0,
            predictability_score - penalty
        )

        for problem in predictability_problems:

            if "Sequential number" in problem:
                feedback.append(
                    "Avoid sequential numbers such as 1234."
                )

            elif "Sequential letter" in problem:
                feedback.append(
                    "Avoid sequential letters such as abcd."
                )

            elif "Repeated character" in problem:
                feedback.append(
                    "Avoid repeating the same character "
                    "three or more times."
                )

            elif "Keyboard pattern" in problem:
                feedback.append(
                    "Avoid predictable keyboard patterns."
                )

            elif "Predictable word" in problem:
                feedback.append(
                    "Avoid common or predictable words."
                )

    # ======================================
    # FINAL SCORE
    # ======================================

    score = (
        length_score
        + variety_score
        + common_score
        + predictability_score
    )

    score = max(0, min(score, 100))

    # ======================================
    # RISK LEVEL
    # ======================================

    if score >= 80:
        risk = "LOW"

    elif score >= 60:
        risk = "MEDIUM"

    else:
        risk = "HIGH"

    # A common password must always be HIGH risk.
    if is_common:
        risk = "HIGH"

    # Predictable structure can override an otherwise high numerical score.
    # One detected pattern is at least MEDIUM risk; two or more are HIGH.
    if len(predictability_problems) >= 2:
        risk = "HIGH"
    elif len(predictability_problems) == 1 and risk == "LOW":
        risk = "MEDIUM"

    return {
        "score": score,
        "risk": risk,
        "length": length,
        "lowercase": has_lowercase,
        "uppercase": has_uppercase,
        "number": has_number,
        "special": has_special,
        "common": is_common,
        "predictability": predictability_problems,
        "feedback": feedback
    }


# ==========================================
# DISPLAY RESULTS
# ==========================================

def main():

    print("=" * 50)
    print("       PERSONAL PASSWORD SECURITY CHECKER")
    print("=" * 50)

    password = getpass.getpass(
        "Enter a password to test: "
    )

    if not password:

        print("\nError: Password cannot be empty.")
        return

    result = check_password(password)

    print("\nPassword Security Assessment")
    print("-" * 35)

    print(
        f"Password length: {result['length']}"
    )

    print(
        f"Lowercase letters: "
        f"{'YES' if result['lowercase'] else 'NO'}"
    )

    print(
        f"Uppercase letters: "
        f"{'YES' if result['uppercase'] else 'NO'}"
    )

    print(
        f"Numbers: "
        f"{'YES' if result['number'] else 'NO'}"
    )

    print(
        f"Special characters: "
        f"{'YES' if result['special'] else 'NO'}"
    )

    print(
        f"Common password: "
        f"{'YES' if result['common'] else 'NO'}"
    )

    print(
        f"Predictability issues: "
        f"{len(result['predictability'])}"
    )

    print(
        f"\nSecurity Score: "
        f"{result['score']}/100"
    )

    print(
        f"Risk Level: {result['risk']}"
    )

    print("\nActionable Feedback")
    print("-" * 35)

    if result["feedback"]:

        for item in result["feedback"]:
            print(f"- {item}")

    else:

        print("- No major improvements detected.")

    print(
        "\nDo not share your real passwords with anyone."
    )


if __name__ == "__main__":
    main()
