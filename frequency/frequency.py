# Расположение букв русского алфавита в порядке их встречаемости в среднем (с Википедии)
frequency_ordinary = [
    ' ', 'о', 'е', 'а', 'и', 'н', 'т', 'с', 
    'р', 'в', 'л', 'к', 'м', 'д', 'п', 'у',
    'я', 'ы', 'ь', 'г', 'з', 'б', 'ч', 'й', 
    'х', 'ж', 'ш', 'ю', 'ц', 'щ', 'э', 'ф', 
    'ъ', 'ё']

# Расположение букв русского алфавита в порядке их встречаемости в художественной литературе
frequency_art=[
  " ", "о", "е", "а", "и", "н", "т", "с",
  "л", "в", "р", "м", "к", "д", "п", "у",
  "ь", "я", "ы", "г", "б", "з", "ч", "й",
  "ж", "х", "ш", "ю", "ц", "щ", "э", "ф",
  "ъ", "ё"]

# Частицы, предлоги, союзы в русских текстах
service_parts_enc = {
  "1": ["с", "о", "и", "а", "у", "в", "к"],
  "2": [
    "не", "ни", "со", "да", "но", "ко", "на",
    "за", "бы", "же", "пo", "об", "то", "ли",
    "ну", "от", "из", "до", "во"
  ],
  "3": [
    "как", "под", "все", "ибо", "для", "при",
    "обо", "вон", "вот", "над", "раз", "где",
    "кто", "меж", "что", "вне", "изо", "ото",
    "или", "еще", "без", "уже", "это", "про",
    "так", "ещё"
  ],
  "4": [
    "либо", "лишь", "дабы", "даже", "того", "безо",
    "ради", "пока", "хотя", "близ", "зато", "вряд",
    "пред", "хоть", "ведь", "таки", "куда", "едва",
    "надо", "тоже", "подо", "если"
  ],
  "5": [
    "предо", "перед", "вроде", "между", "через",
    "среди", "прямо", "ровно", "зачем", "будто",
    "каков", "всего", "точно", "кроме", "когда",
    "чтобы", "также", "разве"
  ]
}



# {
#   " ": 54188,
#   "о": 34199,
#   "е": 27329,
#   "а": 24916,
#   "и": 22829,
#   "н": 22158,
#   "т": 19811,
#   "с": 16285,
#   "л": 14638,
#   "в": 13927,
#   "р": 13915,
#   "м": 10060,
#   "к": 9734,
#   "д": 9193,
#   "п": 8814,
#   "у": 8069,
#   "ь": 6209,
#   "я": 6191,
#   "ы": 5966,
#   "г": 5479,
#   "б": 5435,
#   "з": 5092,
#   "ч": 4838,
#   "й": 3540,
#   "ж": 3086,
#   "х": 2578,
#   "ш": 2431,
#   "ю": 2038,
#   "ц": 1656,
#   "щ": 1099,
#   "э": 1061,
#   "ф": 991,
#   "ъ": 79,
#   "ё": 6
# }