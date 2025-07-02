import json
from pathlib import Path
from collections import defaultdict


def merge_json_folder(input_dir, output_file):
    merged_data = defaultdict(int)
    processed_files = 0
    skipped_files = []

    # Проверяем существование директории
    input_path = Path(input_dir)
    if not input_path.is_dir():
        print(f"Ошибка: Директория '{input_dir}' не существует")
        return

    # Ищем все JSON-файлы в директории
    json_files = list(input_path.glob("*.json"))
    if not json_files:
        print("Нет JSON-файлов для обработки")
        return

    # Обрабатываем каждый файл
    for json_file in json_files:
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

                for key, value in data.items():
                    key = str(key).strip()

                    # Фильтрация ключей
                    if len(key) < 5:
                        continue

                    # Суммирование значений
                    try:
                        merged_data[key] = 1
                    except (ValueError, TypeError):
                        continue

                processed_files += 1

        except (json.JSONDecodeError, PermissionError) as e:
            skipped_files.append(json_file.name)
            continue

    # Сохраняем результат
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dict(merged_data), f, indent=4, ensure_ascii=False, sort_keys=True)

    # Выводим отчет
    print(f"Успешно обработано файлов: {processed_files}/{len(json_files)}")
    if skipped_files:
        print("\nСледующие файлы были пропущены:")
        for fn in skipped_files:
            print(f" - {fn}")


merge_json_folder("validated_channels", "new_words.json")
