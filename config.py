import json
from pathlib import Path


config = Path('config.json')
progress = Path('progress.json')
config_dict = json.load(config.open(mode='r', encoding='utf-8'))
domain = config_dict['domain']


def update_progress():
    progress.write_text(json.dumps(progress_dict, indent=2, ensure_ascii=False), encoding='utf-8')


try:
    progress_dict = json.load(progress.open(mode='r', encoding='utf-8'))
except FileNotFoundError:
    progress_dict = dict()
    update_progress()



