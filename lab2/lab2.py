from tabulate import tabulate

def validate_user_input(info, data_type, default_term=None):
        while True:
            try:
                user_value = input(info)

                if user_value == "" and default_term is not None:
                    return default_term

                converted_user_value = data_type(user_value)
                if converted_user_value <= 0:
                    print("Помилка! Значення має бути більше нуля.")
                    continue
                return converted_user_value
            except ValueError:
                if data_type == int:
                    print("Помилка! Введіть ціле число.")
                elif data_type == float:
                    print("Помилка! Введіть число.")


def user_input():
        initial_deposit = validate_user_input("Початкова сума депозиту (грн): ", float)
        year_interest = validate_user_input("Річна відсоткова ставка (%): ", float)
        deposit_term = validate_user_input("Термін депозиту (роки): ", int, default_term= 2)
        return initial_deposit, year_interest, deposit_term

def calculate_monthly_deposit(initial_deposit, year_interest, deposit_term):
    k = 1 + (year_interest/ 1200)
    month_amount = deposit_term * 12

    curr_deposit = initial_deposit
    data = []

    for month in range(1, month_amount+1):
        curr_deposit *= k
        data.append([month, round(curr_deposit, 2)])

    return data, curr_deposit

def print_results(data, final_deposit):
    headers = ["Місяць", "Сума депозиту"]

    print(tabulate(data, headers=headers, tablefmt='pipe', floatfmt=".2f"))
    print("===============================")
    print(f"Результуюча сума на рахунку по завершенню терміну депозиту: {final_deposit:.2f}")

def main():
    while True:
        initial_deposit, year_interest, deposit_term = user_input()
        data, final_deposit = calculate_monthly_deposit(
            initial_deposit,
            year_interest,
            deposit_term
        )

        print_results(data, final_deposit)

        while True:
            print("")
            proceed = input("Продовжити? y/n: ").lower()
            if proceed == "y":
                break
            elif proceed == "n":
                print("Вихід..")
                return
            else:
                print("Error! Enter y or n.")

if __name__ == "__main__":
    main()
