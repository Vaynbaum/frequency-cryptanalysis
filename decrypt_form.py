from tkinter import *
from tkinter import filedialog as fd
from frequency.frequency import *
from decrypt import *


def open_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def set_file_text(text):
    "Добавить текст в поле для текста"
    global entry_text
    text_entry.delete(1.0, END)
    text_entry.insert(1.0, text[:4000])
    entry_text = text


def select_file():
    "Открытие файла и отображение его текста на форме"
    filename = fd.askopenfilename(
        initialdir="/C:/",
        filetypes=(("text files", "*.txt"), ("All files", "*.*")),
    )
    if filename != "":
        text = open_file(filename)
        set_file_text(text)
        decrypter.Set_text(text)


def change_type(*args) -> None:
    "Выбор типа текста для расшифровки"
    global type
    global selected_semantic_type
    selected_semantic_type = type.get()


def encrypt_text():
    "Расшифровка и текста и отображение результата на форме"
    text = decrypter.Encrypt_text(
        semantic_type_frequencies[selected_semantic_type].copy(), space_consider.get()
    )
    set_file_text(text)


def update_part(service_parts: dict):
    "Добавление найденных служебных частей речи на форму"
    global services_part_listbox
    services_part_listbox.delete(0, END)
    for part in service_parts.items():
        left = part[0]
        right = part[1]["part"]
        services_part_listbox.insert(END, f"{left}-{right}")


def save_edit():
    "Сохранение ручного исправления текста"
    text = text_entry.get(1.0, END)
    set_file_text(decrypter.Manual_editing(text))


def write_file(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)


def save_dec():
    "Сохранение результата в файл"
    filename = fd.asksaveasfilename(
        initialfile="decrypted.txt",
        filetypes=(("text files", "*.txt"), ("All files", "*.*")),
    )
    if filename != "":
        write_file(filename, entry_text)


def analyze():
    "Поиск служебных частей речи"
    service_parts = decrypter.Analyze_prepositions()
    update_part(service_parts)


decrypter = Decrypter()
entry_text = ""
# root
root = Tk()
root.title("Расшифровка криптоанализом")
root.geometry("900x500")
root.resizable(False, False)
# buttons
Button(root, text="Открыть файл с зашифрованным текстом", command=select_file).place(x=5, y=0)
Button(root, text="Расшифровать текст", command=encrypt_text).place(x=5, y=360)
Button(root, text="Сохранить изменения", command=save_edit).place(x=150, y=360)
Button(root, text="Сохранить расшифрованный текст в файл", command=save_dec).place(x=5, y=400)
Button(root, text="Искать предлоги", command=analyze).place(x=440, y=390)
# сheckbuttons
space_consider = BooleanVar(root)
prepositions_consider = BooleanVar(root)
Checkbutton(root, text="Пробелы зашифрованы", variable=space_consider).place(x=440, y=360)
# listbox
Label(root, text="Найденные служебные части").place(x=620, y=0)
services_part_listbox = Listbox(root)
services_part_listbox.place(x=620, y=30)
# menu
semantic_type_frequencies = {
    "Обычный": frequency_ordinary,
    "Художественный": frequency_art,
}
selected_semantic_type = list(semantic_type_frequencies.keys())[0]
main_menu = Menu(root)
type_menu = Menu(root)
type = StringVar(root, value=selected_semantic_type)

type.trace("w", change_type)
for semantic_type in semantic_type_frequencies.keys():
    type_menu.add_radiobutton(label=semantic_type, value=semantic_type, variable=type)

main_menu.add_cascade(label="Тип текста", menu=type_menu)
# entry
text_entry = Text(root, width=75, height=20, bg="light yellow")
text_entry.place(x=5, y=30)
root.config(menu=main_menu)
root.mainloop()
