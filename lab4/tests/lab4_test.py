from unittest import TestCase, main
from unittest.mock import patch, mock_open
from lab4 import calculate_bytes, parse_line_bytes


class CalculateBytesTest(TestCase):

    def test_calculate_bytes_two_lines(self):
        test_log = (
            '213.109.238.193 - - [07/May/2017:00:08:35 +0300] "GET /question/edit.php?cmid=1&cat=1%2C18&qpage=0&category=7%2C131&qbshowtext=0&recurse=0&recurse=1&showhidden=0&showhidden=1 HTTP/1.0" 303 500 "http://learn.topnode.if.ua/question/edit.php" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"\n'
            '213.109.238.193 - - [07/May/2017:00:08:35 +0300] "GET /login/index.php HTTP/1.0" 303 1000 "http://learn.topnode.if.ua/question/edit.php" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"\n'
        )

        with patch("builtins.open", mock_open(read_data=test_log)):
            result = calculate_bytes()

        self.assertEqual(result, 1500)

    def test_calculate_bytes_empty_file(self):
        with patch("builtins.open", mock_open(read_data="")):
            self.assertEqual(calculate_bytes(), 0)

    def test_parse_line_bytes_corrupted(self):
        result = parse_line_bytes("Corrupted log line without quotes\n")
        self.assertEqual(result, 0)

    def test_parse_line_bytes_invalid_number(self):
        line = '91.243.6.52 - - [07/May/2017:13:39:09 +0300] "GET / HTTP/1.0" 200 abc "-" "Mozilla/5.0 (X11; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0"\n'

        result = parse_line_bytes(line)

        self.assertEqual(result, 0)

    def test_calculate_bytes_with_dash(self):
        test_log = (
            '91.243.6.52 - - [07/May/2017:13:39:09 +0300] "GET / HTTP/1.0" 200 1000 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0"\n'
            '213.109.238.193 - - [07/May/2017:00:08:35 +0300] "GET /login/index.php HTTP/1.0" 303 - "http://learn.topnode.if.ua/question/edit.php" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"\n'
        )

        with patch("builtins.open", mock_open(read_data=test_log)):
            result = calculate_bytes()
        self.assertEqual(result, 1000)



if __name__ == "__main__":
    main()