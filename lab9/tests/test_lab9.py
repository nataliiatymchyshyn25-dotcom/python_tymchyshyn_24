import unittest
from lab9 import extract_datetime

class TestExtractDatetime(unittest.TestCase):
    def test_date_with_timezone(self):
        text = "On Sun, 13 Oct 2024 19:01:18 +0800, Test User <test@test.me> wrote:"
        self.assertEqual(extract_datetime(text), "2024-10-13T19:01:18Z")

    def test_date_with_at(self):
        text = "On Tue, Oct 1, 2024 at 19:23 Test User <test@test.me> wrote:"
        self.assertEqual(extract_datetime(text), "2024-10-01T19:23:00Z")

    def test_date_with_pm(self):
        text = "On Mon, Oct 14, 2024, 8:06 PM Test User <test@test.me> wrote:"
        self.assertEqual(extract_datetime(text), "2024-10-14T20:06:00Z")

    def test_date_with_am(self):
        text = "On Wed, 9 Oct 2024, 2:04 am Test User, <test@test.me> wrote:"
        self.assertEqual(extract_datetime(text), "2024-10-09T02:04:00Z")

    def test_date_with_hyphens(self):
        text = "On 25-Sep-2024 3:37 am, Test User <test@test.me> wrote:"
        self.assertEqual(extract_datetime(text), "2024-09-25T03:37:00Z")

    def test_date_without_seconds(self):
        text = "On Fri, 27 Sept 2024, 17:32 Test User, <test@test.me> wrote:"
        self.assertEqual(extract_datetime(text), "2024-09-27T17:32:00Z")


if __name__ == "__main__":
    unittest.main()