from typing_extensions import LiteralString
from frequency.frequency import *
import copy
import string
import re
from collections import deque


class Decrypter:
    def __init__(self):
        self.__comparisons = None

    def __remove_chars_from_text(self, text: str, chars: LiteralString):
        "Удаление определенной буквы из текста"
        return "".join([ch for ch in text if ch not in chars])

    def __text_processing_before_calc(self, text: str, space_consider: bool):
        "Обработка текст перед подсчетом частот встречаемости символов"
        spec_chars = string.punctuation + "\n\xa0«»\t—…–"
        if not space_consider:
            spec_chars += " "
        text = self.__remove_chars_from_text(text, spec_chars)
        text = self.__remove_chars_from_text(text, string.digits)
        return text

    def __calc_frequency_encrypt_letters(self, text: str, space_consider: bool):
        "Подсчет частот встречаемости символов в исходном тексте"
        text = self.__text_processing_before_calc(text, space_consider)
        decrypt_letters = {}
        for ch in text:
            decrypt_letters = self.__add_word_in_dict(ch, decrypt_letters)
        return self.__sort_dict(decrypt_letters)

    def __add_word_in_dict(self, word: str, store: dict):
        "Добавление слов с их встречаемостью в словарь"
        if word in store:
            store[word] += 1
        else:
            store[word] = 1
        return store

    def __sort_dict(self, store: dict):
        "Сортировка словаря по значению"
        return dict(sorted(store.items(), key=lambda item: item[1], reverse=True))

    def __extracting_sorting_words(self, text: str):
        "Извлечение служебных слов из текста и добавление их в словарь с частотами встречаемости"
        words = re.split("\W+", text)
        MIN_LENGTH_WORD = 2
        MAX_LENGTH_WORD = 5
        service_parts = {}
        for word in words:
            if len(word) >= MIN_LENGTH_WORD and len(word) <= MAX_LENGTH_WORD:
                service_parts = self.__add_word_in_dict(word, service_parts)
        return self.__sort_dict(service_parts)

    def __discard_rare(self, service_parts: dict):
        "Отсеивание редких слов и группировка частых по их длине символов"
        service_parts_by_len = {}
        MIN_FREQUENCY_WORD = 25
        for part in service_parts.items():
            length = len(part[0])
            if part[1] > MIN_FREQUENCY_WORD:
                if length in service_parts_by_len:
                    service_parts_by_len[length].append(part[0])
                else:
                    service_parts_by_len[length] = [part[0]]
        return service_parts_by_len

    def __bruteforce_pairs(self, service_parts_by_len: dict):
        "Перебор пар служебных слов для поиска соответствий"
        comp = {}
        taken_words = {}
        # Проходим по группам различной длинны
        for key in service_parts_by_len.keys():
            # Зашифрованные части речи в очередь
            q = deque(service_parts_by_len[key])
            while len(q) > 0:
                enc_part = q.popleft()
                # Перебираем пары зашифрованных и незашифрованных служебных частей речи
                for dec_part in service_parts_enc[str(key)]:
                    cnt = self.__count_letters_comp(copy.copy(enc_part), dec_part)
                    self.__add_part_dict(comp, taken_words, dec_part, enc_part, cnt, q)
        return comp

    def __solve_colision(
        self,
        comp: dict,
        taken_words: dict,
        dec_part: str,
        enc_part: str,
        cnt: int,
        q: deque,
    ):
        "Определить кому достанется дешифрованное слово"
        last_enc = taken_words[dec_part]
        obj = comp[last_enc]
        if cnt > obj["cnt"]:
            comp[enc_part] = {"part": dec_part, "cnt": cnt}
            taken_words[dec_part] = enc_part
            del comp[last_enc]
            q.append(last_enc)

    def __add_part_dict(
        self,
        comp: dict,
        taken_words: dict,
        dec_part: str,
        enc_part: str,
        cnt: int,
        q: deque,
    ):
        "Добавление пары служебных слов зашифрованного текста и возможного дешифрованного"
        if cnt >= len(enc_part) / 2:
            # Зашифрованное слово уже занято
            if enc_part in comp:
                obj = comp[enc_part]
                # Количество совпавших букв больше
                if cnt > obj["cnt"]:
                    # Дешифрованное слово уже занято
                    if dec_part in taken_words:
                        self.__solve_colision(comp, taken_words, dec_part, enc_part, cnt, q)
                    # Дешифрованное слово свободно
                    else:
                        comp[enc_part] = {"part": dec_part, "cnt": cnt}
                        taken_words[dec_part] = enc_part
                    del taken_words[obj["part"]]
            # Зашифрованное слово свободно
            else:
                # Дешифрованное слово уже занято
                if dec_part in taken_words:
                    self.__solve_colision(comp, taken_words, dec_part, enc_part, cnt, q)
                # Дешифрованное слово свободно
                else:
                    comp[enc_part] = {"part": dec_part, "cnt": cnt}
                    taken_words[dec_part] = enc_part

    def __count_letters_comp(self, str1: str, str2: str):
        "Подсчет количества совпавших символов в двух строках"
        count = 0
        mark_str = {"comp": set(), "no_comp": set()}
        for i in range(len(str1)):
            if str1[i] == str2[i]:
                mark_str["comp"].add(str1[i])
                count += 1
            else:
                mark_str["no_comp"].add(str1[i])
           
        # Если символ и в совпавших и не в совпавших, значит слова непохожи
        union_set = mark_str["comp"] & mark_str["no_comp"]
        if len(union_set) > 0:
            return 0
        return count

    def __substitution_by_coincidence(self):
        """Подстановка в исходный текст
        соответствующих по частоте встречаемости символов"""
        text_for_decrypt = ""
        for ch in self.__src_text:
            enc_ch = self.__comparisons.get(ch)
            if enc_ch is not None:
                text_for_decrypt += enc_ch
            else:
                text_for_decrypt += ch
        return text_for_decrypt

    def __find_key_by_value(self, value: str, dict: dict):
        "Найти ключ в словаре по его значению"
        for item in dict.items():
            if item[1] == value:
                return item[0]

    def __swap(self, key: str, new_value: str):
        "Обмен букв в таблице подстановок"
        last_key = self.__find_key_by_value(new_value, self.__comparisons)
        last_value = self.__comparisons[key]
        self.__comparisons[key] = self.__comparisons[last_key]
        self.__comparisons[last_key] = last_value

    def Encrypt_text(self, frequency_arr: list, space_consider: bool) -> str:
        """Дешифровка текста

        Args:
            frequency_arr (list): Частота встречаемости букв
            space_consider (bool): Флаг, зашифрован ли пробел

        Returns:
            str: Дешифрованный текст
        """
        if not space_consider:
            frequency_arr.pop(0)
        decrypt_letters = self.__calc_frequency_encrypt_letters(
            copy.copy(self.__src_text), space_consider)
        "Сопоставление частот и дешифровка текста"
        self.__comparisons = dict(zip(decrypt_letters, frequency_arr))
        text = self.__substitution_by_coincidence()
        self.__last_dec_text = text
        return self.__last_dec_text

    def Set_text(self, text: str):
        self.__src_text = text.lower()

    def Analyze_prepositions(self):
        "Поиск служебных частей речи"
        service_parts = self.__extracting_sorting_words(self.__last_dec_text)
        service_parts_by_len = self.__discard_rare(service_parts)
        return self.__bruteforce_pairs(service_parts_by_len)

    def Manual_editing(self, text: str):
        "Ручная додешифровка текста"
        for i in range(len(text) - 1):
            "Поиск расхождения текстов"
            if text[i] != self.__last_dec_text[i]:
                self.__swap(self.__src_text[i], text[i])
        "Новая подстановка для дешифровки"
        text = self.__substitution_by_coincidence()
        self.__last_dec_text = text
        return text
