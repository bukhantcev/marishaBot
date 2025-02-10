import os
from collections import Counter

# Таблица частот русских букв (заглавных)
frequency_table = [
    (' ', 0.175), ('О', 0.090), ('Е', 0.072), ('А', 0.062), ('И', 0.062),
    ('Н', 0.053), ('Т', 0.053), ('Р', 0.040), ('С', 0.045), ('В', 0.038),
    ('Л', 0.035), ('Д', 0.025), ('М', 0.026), ('П', 0.023), ('У', 0.021),
    ('Ы', 0.016), ('Б', 0.014), ('Ч', 0.012), ('Г', 0.013), ('З', 0.016),
    ('Ж', 0.077), ('Ф', 0.002), ('К', 0.028), ('Х', 0.009), ('Ц', 0.004),
    ('Ш', 0.006), ('Э', 0.003), ('Ю', 0.006), ('Я', 0.018), ('Ъ', 0.014),
    ('Ь', 0.014), ('Щ', 0.003)
]


# Считывание текстов из файлов
def read_files(directory):
    texts = ""
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                texts += file.read() + "\n"
    return texts


# Подсчет частоты символов
def count_characters(text):
    return Counter(text)


# Замена символов на основе частоты
def replace_characters(text, char_freq, frequency_table):
    sorted_freq = sorted(char_freq.items(), key=lambda x: x[1], reverse=True)

    # Создаем словарь для замены
    replace_dict = {}
    for i in range(min(len(sorted_freq), len(frequency_table))):
        replace_dict[sorted_freq[i][0]] = frequency_table[i][0]

    # Заменяем символы
    replaced_text = ''.join(replace_dict.get(char, char) for char in text)

    return replaced_text


# Основной процесс
def main():
    directory = "CODE"  # Путь к папке с текстовыми файлами
    texts = read_files(directory)

    # Подсчитаем частоту символов в тексте
    char_freq = count_characters(texts)

    # Заменим символы по частоте
    replaced_text = replace_characters(texts, char_freq, frequency_table)

    # Запишем отредактированный текст в новый файл
    with open("decoded_text.txt", "w", encoding="utf-8") as file:
        file.write(replaced_text)

    print("Текст отредактирован и сохранен в 'decoded_text.txt'.")


