import json
import sys
import string


def open_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def write_file(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def remove_chars_from_text(text, chars):
    "Удаление определенной буквы из текста"
    return "".join([ch for ch in text if ch not in chars])


def calc_frequency_letters(text):
    "Подсчет встречаемости букв в тексте"
    decrypt_letters = {}
    for ch in text:
        if ch in decrypt_letters:
            decrypt_letters[ch] += 1
        else:
            decrypt_letters[ch] = 1
    # Сортировка по частоте встречаемости букв
    decrypt_letters = dict(
        sorted(decrypt_letters.items(), key=lambda item: item[1], reverse=True)
    )
    return decrypt_letters


def text_process(text: str):
    """Предварительная обработка текста,
    очистка от лишних символов"""
    text = text.lower()
    spec_chars = string.punctuation + "\n\xa0«»\t—…–°−′"
    text = remove_chars_from_text(text, spec_chars)
    text = remove_chars_from_text(text, string.digits)
    return text


def main():
    args = sys.argv
    name_in_file = args[1]
    name_out_file = args[2]
    text = open_file(name_in_file)
    text = text_process(text)
    decrypt_letters = calc_frequency_letters(text)
    write_file(name_out_file, decrypt_letters)


if __name__ == "__main__":
    main()
