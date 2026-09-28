def parse_line_bytes(line):
    try:
        val = line.split('"')[2].split()[1]
        return int(val) if val != "-" else 0
    except (IndexError, ValueError):
        return 0

def calculate_bytes():
    with open("logs/2017_05_07_nginx.txt") as file:
        sent_bytes = (parse_line_bytes(line) for line in file)
        return sum(sent_bytes)


if __name__ == "__main__":
    try:
        total_sent = calculate_bytes()
        print("Надіслано байтів:", total_sent)
    except FileNotFoundError:
        print("Помилка: файл не знайдено")