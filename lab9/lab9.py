import re
from dateutil.parser import parse


def extract_datetime(text):
    pattern = r"^On\s+(.+?\d{1,2}:\d{2}(?::\d{2})?\s*(?:am|pm)?)"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        date = parse(match.group(1))
        return date.strftime("%Y-%m-%dT%H:%M:%SZ")

    return None


def main():
    strings = [
        "On Sun, 13 Oct 2024 19:01:18 +0800, Test User <test@test.me> wrote:",
        "On Tue, Oct 1, 2024 at 19:23 Test User <test@test.me> wrote:",
        "On Mon, Oct 14, 2024, 8:06 PM Test User <test@test.me> wrote:",
        "On Wed, 9 Oct 2024, 2:04 am Test User, <test@test.me> wrote:",
        "On 25-Sep-2024 3:37 am, Test User <test@test.me> wrote:",
        "On Fri, 27 Sept 2024, 17:32 Test User, <test@test.me> wrote:"
    ]

    for text in strings:
        print(extract_datetime(text))


if __name__ == "__main__":
    main()
