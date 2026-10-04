def get_error_markers(text: str, errors: list) -> str:
    markers = [" "] * len(text)

    for position in errors:
        markers[position] = "^"

    return "".join(markers)


def validate_brackets(text: str):
    brackets = {
        ")": "(",
        "}": "{",
        ">": "<",
        "]": "["
    }

    stack = []
    errors = []

    for position, char in enumerate(text):

        if char in brackets.values():
            stack.append((char, position))

        elif char in brackets:

            if not stack:
                errors.append(position)

            elif stack[-1][0] == brackets[char]:
                stack.pop()

            else:
                errors.append(position)

    for _, position in stack:
        errors.append(position)

    if errors:
        errors.sort()

        markers = get_error_markers(text, errors)

        raise ValueError(
            f"Дужки незбалансовані на позиціях {errors}\n"
            f"{text}\n"
            f"{markers}"
        )

def get_text() -> str:
    return input("Введіть строку: ")


def want_to_proceed() -> bool:
    while True:
        answer = input("Want to proceed? y/n: ").lower()

        if answer == "y":
            return True

        if answer == "n":
            return False

        print("Please enter y or n.")


def main():
    while True:
        text = get_text()

        validate_brackets(text)

        print("Строка валідна")

        if not want_to_proceed():
            break


if __name__ == "__main__":
    main()