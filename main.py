import json
from pathlib import Path
from time import sleep

import requests
from requests.exceptions import RequestException
from lxml import html, etree

from config import *


class NoSuchPage(RequestException):
    pass


def get_html(url):
    response = requests.get(url)

    if response.status_code == 200:
        return html.fromstring(requests.get(url).content)
    elif response.status_code == 404:
        raise NoSuchPage
    else:
        print(response.status_code)
        sleep(5)
        get_html(url)


def get_links_page_url(page, current_target):
    return f'{domain}/jobs-{current_target.replace(" ", "+")}/?page={page}'


def scrape_links(current_target, current_progress):
    if current_progress.get('is_links_done', False):
        return

    try:
        page = current_progress['links_done'] + 1
    except KeyError:
        current_progress['links_done'] = 0
        update_progress()
        page = 1

    while True:
        links = get_html(get_links_page_url(page, current_target))\
            .xpath('//div[@id="pjax-job-list"]/div[@class]//h2/a/@href')
        if not links:
            current_progress['is_links_done'] = True
            update_progress()
            return

        parent_dir = Path(f'data/{current_target}/links')
        parent_dir.mkdir(parents=True, exist_ok=True)
        (parent_dir / f'{page}.json').write_text(json.dumps(links))

        current_progress['links_done'] = page
        update_progress()
        page += 1
        print(progress_dict)


def scrape_jobs(current_target, current_progress):
    if current_progress.get('is_done', False):
        return

    for f in Path(f'data/{current_target}/links/').glob('*.json'):
        for link in json.loads(f.read_text(encoding='utf-8')):
            try:
                if link in current_progress['done']:
                    continue
            except KeyError:
                current_progress['done'] = []

            page = get_html(f'{domain}{link}')
            value = {
                'url': f'{domain}{link}',
                'job': current_target,
                'header': page.xpath('//h1[1]')[0].text_content().strip(),
                'content': page.xpath('//div[@id="job-description"]')[0].text_content().strip()
            }

            job_id = link.split('/')[2]

            parent_dir = Path(f'data/{current_target}/jobs/')
            parent_dir.mkdir(parents=True, exist_ok=True)
            (parent_dir / f'{job_id}.json').write_text(json.dumps(value, indent=2, ensure_ascii=False),
                                                       encoding='utf-8')

            current_progress['done'].append(link)
            update_progress()

    current_progress['is_done'] = True
    update_progress()


def main():
    for target in config_dict['targets']:
        try:
            current_progress = progress_dict[target]
        except KeyError:
            current_progress = dict()
            progress_dict[target] = current_progress
            update_progress()

        scrape_links(target, current_progress)
        scrape_jobs(target, current_progress)


if __name__ == '__main__':
    main()
