def get_positive_float(prompt: str) -> float:
    while True:
        raw_value = input(prompt).strip()
        try:
            value = float(raw_value)
        except ValueError:
            print("  ⚠ That doesn't look like a number. Please enter digits only (e.g. 68.5).")
            continue

        if value <= 0:
            print("  ⚠ Value must be greater than zero. Please try again.")
            continue

        return value


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    return weight_kg / (height_m ** 2)


def classify_bmi(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def main() -> None:
    print("=== BMI Calculator ===\n")

    weight = get_positive_float("Enter your weight in kg: ")
    height = get_positive_float("Enter your height in m (e.g. 1.75): ")

    bmi = calculate_bmi(weight, height)
    category = classify_bmi(bmi)

    print("\n--- Result ---")
    print(f"Your BMI is: {bmi:.2f}")
    print(f"Category:    {category}")


if __name__ == "__main__":
    main()
