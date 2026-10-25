import re
import os
import shutil


def salty_language(text):
    pattern = r"[аеёиоуыэюяАЕЁИОУЫЭЮЯ]"
    replacement = lambda match: match.group() + "с" + match.group()
    return re.sub(pattern, replacement, text)


def extract_chords(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    pattern = r"\b[A-G][#b]?(?:m|maj|dim|aug|sus)?\d*\b"

    chords = re.findall(pattern, text)

    return set(chords)


def rename_files(dir, pattern, new_pattern=None, sample_names=None, to_replace=False):

    for filename in os.listdir(dir):
        if not os.path.isfile(os.path.join(dir, filename)):
            continue

        if not re.search(pattern, filename):
            continue

        new_name = filename

        if new_pattern is not None:
            new_name = re.sub(pattern, new_pattern, new_name)

        if sample_names is not None:
            for old, new in sample_names.items():
                new_name = new_name.replace(old, new)

        old_path = os.path.join(dir, filename)
        new_path = os.path.join(dir, new_name)

        if old_path == new_path:
            continue

        if os.path.exists(new_path):
            print(f"Файл уже существует: {new_name}")
            continue

        if to_replace:
            os.rename(old_path, new_path)
        else:
            shutil.copy2(old_path, new_path)

        print(f"{filename} -> {new_name}")
