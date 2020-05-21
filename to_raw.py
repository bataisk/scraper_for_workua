from pathlib import Path
import json
from langdetect import detect
from transliterate import translit


targets = [
    "юрист",
    "адвокат",
    "аудитор",
    "криминалист",
    "нотариус",
    "коллектор"
]

for target in targets:
    target_translated = translit(target, language_code='ru', reversed=True)

    profecion_folder = Path(f'data1/{target_translated}//')
    all_jobs_folder = Path(f'data1/all/')

    profecion_folder.mkdir(parents=True, exist_ok=True)
    all_jobs_folder.mkdir(parents=True, exist_ok=True)

    for file in Path(f'data/{target}/jobs/').glob('*.json'):
        data = json.loads(file.read_text(encoding='utf-8'), encoding='utf-8')
        file_language = detect(data['content'])

        data = f"{data['job']}\n{data['header']}\n{data['content']}"

        (profecion_folder / file_language).mkdir(parents=True, exist_ok=True)
        (all_jobs_folder / file_language).mkdir(parents=True, exist_ok=True)

        (profecion_folder / file_language / file.name.split('.')[0]).write_text(data, encoding='utf-8')
        (all_jobs_folder / file_language / file.name.split('.')[0]).write_text(data, encoding='utf-8')



