def convert_temperature(fahrenheit):
    celsius = (fahrenheit - 32) * 5 / 9
    return round(celsius, 1)


def main():
    while True:
        try:
            user_temperature_input = float(input("Enter temperature in F: "))
        except ValueError:
            print("Error, enter a number")
            continue

        result = convert_temperature(user_temperature_input)
        print("Temperature in C:", result)

        while True:
            user_option = input("Want to proceed? y/n: ").lower()

            if user_option == "y":
                break
            elif user_option == "n":
                print("Exit..")
                return
            else:
                print("Error, try again")


if __name__ == "__main__":
    main()
