import sys

LETTERS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def open_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def write_file(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)


def caesar_cipher(text: str, key: int):
    """Зашифровка текста шифром Цезаря"""
    cnt = len(LETTERS)
    text_for_encrypt = text.lower().replace(",", "")
    arr = []
    for ch in text_for_encrypt:
        ind = LETTERS.find(ch)
        if ind > -1:
            arr.append(LETTERS[(ind + key) % cnt])
        else:
            arr.append(ch)
    text_for_decrypt = "".join(arr)
    return text_for_decrypt


def main():
    key = sys.argv[1]
    in_file = sys.argv[2]
    out_file = sys.argv[3]
    text = open_file(in_file)
    text = caesar_cipher(text, int(key))
    write_file(out_file, text)


if __name__ == "__main__":
    main()
