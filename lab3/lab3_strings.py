import doctest

def get_text():
    return input("Введіть текст: ")


def reverse_string(s:str):
    '''
    Reverses the letters in each word of the input text.
    Non-letter characters remain in their original positions
    :param s: input text
    :return:  text with letters reversed in each word, keeping non-letters in place
    :raises: TypeError: if the input is not a string

    >>> reverse_string('abcd')
    'dcba'
    >>> reverse_string('abcd efgh')
    'dcba hgfe'
    >>> reverse_string('')
    ''
    >>> reverse_string('a3bc$d @efg8h!')
    'd3cb$a @hgf8e!'
    >>> 12345
    12345
    >>> reverse_string(123)
    Traceback (most recent call last):
    ...
    TypeError: Input must be a string.
    '''
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")

    words = s.split(" ")
    result = []

    for word in words:
        if word.isalpha():
            result.append(word[::-1])
        else:
            letters = list(word)
            start_pointer = 0
            end_pointer = len(letters) - 1

            while start_pointer < end_pointer:
                if not letters[start_pointer].isalpha():
                    start_pointer += 1
                elif not letters[end_pointer].isalpha():
                    end_pointer -= 1
                else:
                    letters[start_pointer], letters[end_pointer] = (
                        letters[end_pointer], letters[start_pointer]
                    )
                    start_pointer += 1
                    end_pointer -= 1

            result.append("".join(letters))

    return " ".join(result)

def ask_to_continue():
    while True:
        answer = input("Продовжити? y/n: ").lower()

        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            print("Помилка! Введіть y або n.")

if __name__ == "__main__":
    doctest.testmod()
    while True:
        text = get_text()
        print(reverse_string(text))

        if not ask_to_continue():
            break