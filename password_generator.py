import random
import string

MIN_LENGTH = 8


def get_length() -> int:
    while True:
        raw_value = input(f"Enter desired password length (minimum {MIN_LENGTH}): ").strip()
        try:
            length = int(raw_value)
        except ValueError:
            print("  ⚠ Please enter a whole number.")
            continue

        if length < MIN_LENGTH:
            print(f"  ⚠ Length must be at least {MIN_LENGTH} characters.")
            continue

        return length


def get_character_types() -> str:
    print("\nWhich character types should be included?")
    while True:
        use_upper = input("  Include uppercase letters? (y/n): ").strip().lower() == "y"
        use_lower = input("  Include lowercase letters? (y/n): ").strip().lower() == "y"
        use_digits = input("  Include numbers? (y/n): ").strip().lower() == "y"
        use_symbols = input("  Include symbols? (y/n): ").strip().lower() == "y"

        if sum([use_upper, use_lower, use_digits, use_symbols]) < 2:
            print("  ⚠ Please select at least 2 character types.\n")
            continue

        pool = ""
        if use_upper:
            pool += string.ascii_uppercase
        if use_lower:
            pool += string.ascii_lowercase
        if use_digits:
            pool += string.digits
        if use_symbols:
            pool += string.punctuation

        return pool


def generate_password(length: int, pool: str) -> str:
    return "".join(random.choice(pool) for _ in range(length))


def main() -> None:
    print("=== Random Password Generator ===\n")

    while True:
        length = get_length()
        pool = get_character_types()

        password = generate_password(length, pool)
        print(f"\nGenerated password: {password}\n")

        again = input("Generate another password? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break
        print()


if __name__ == "__main__":
    main()
