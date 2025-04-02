from selenium.webdriver.common.by import By
from selenium import webdriver
import selenium
import models.search as search
import re
import time
import logging
import asyncio

options = selenium.webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')

def get_driver():
    driver = selenium.webdriver.Chrome(options=options)
    return driver

parse_timeout = 60*5


def get_n_searches(n, location=276, offset=0) -> list:
    links = []
    driver = get_driver()
    try:
        for i in range(n):
            css_selector=f'#page-body > div.forumbg > div > ul.topiclist.topics > li:nth-child({offset+i+1}) > dl > dt > div > a'
            driver.get(f"https://lizaalert.org/forum/viewforum.php?f={location}")
            elem = driver.find_element(By.CSS_SELECTOR, css_selector)
            link = elem.get_attribute("href")
            if link.find('&sid') != -1:
                link = link[:link.rfind('&sid')]

            links.append(link)
    except Exception as e:
        raise e
    finally:
        driver.quit()
    
    return links


def get_searches_descriptions(links) -> list[search.SearchDescription]:
    searches = []

    driver = get_driver()
    for l in links:
        logging.info(f'parsing: {l}')
        driver.get(l)
        # находим 1ый пост
        post = driver.find_element(By.CSS_SELECTOR, "div[id^='post_content']").find_element(By.CSS_SELECTOR, "div.content")
        # находим заголовок
        description = post.text
        
        title = post.find_element(By.TAG_NAME, 'span').find_element(By.CLASS_NAME, 'text-strong').text
        
        coords = extract_coords(description)
        if len(coords) == 0:
            logging.info("coords not found in post above")
            logging.info("-" * 40)
            continue

        type = extract_type(description)
        time = extract_time(description)
        searches.append(search.SearchDescription(l, title, time, type, coords[0][0], coords[0][1], time))

        logging.info("-" * 40)

    driver.quit()
    return searches

def extract_coords(text):
    res = []
    for l in text.split('\n'):
        coords = re.findall('(-?\d+\.\d+)\s?\,\s*(-?\d+\.\d+)$', l)

        for c in coords:
            res.append([c[0].strip(), c[1].strip()])
    return res

def extract_type(text):
    # на выходе строчка вида 'город/лес' или 'лесные задач' и тд
    selectors = ['форма одежды', 'одежда', 'форма']
    lines = text.split('\n')
    for l in lines:
        l = l.lower()
        for selector in selectors:
            if l.find(selector) != -1:
                type = l[l.find(selector) + len(selector):].strip()
                exclude = {':', '/', '-', '+'}
                type = ''.join(ch if ch not in exclude else ' ' for ch in type).strip()
                return type

def extract_time(text):
    regexp = '(([0-1]?[0-9]|2[0-3])(:|.)[0-5][0-9]$)'
    res = []
    for l in text.split('\n'):
        times = re.findall(regexp, l)

        if len(times) > 0:
            res.append(times[0][0])
    return res


async def broadcast(bot, ids):
    processed = set()
    while True:

        # смотрим n последних постов.
        searches = get_n_searches(3)

        # проверяем что раньше не обрабатывали этот пост
        new_searches = []
        for s in searches:
            if s not in processed:
                new_searches.append(s)
            logging.info(f'mark link as processed: {s}')
            processed.add(s)

        try:
            descriptions = get_searches_descriptions(new_searches)
        except Exception as e:
            for chat_id in ids:
                try:
                    await bot.send_message(int(chat_id), f"Exception: {e}")
                except:
                    logging.info(f'failed to send to: {chat_id}')
                    pass
            continue

        for d in descriptions:
            for chat_id in ids:
                try:
                    await bot.send_message(int(chat_id), text="**Поиск!**\n\n"
                                                f"[{d.title}]({d.link})\n"
                                                f"Штаб: {d.hq_time}\n"
                                                f"Тип: {d.search_type}\n\n"
                                                f"`{d.latitude}, {d.longitude}`",
                               parse_mode='Markdown')
                    await bot.send_location(int(chat_id), d.latitude, d.longitude)
                except:
                    logging.info(f'failed to send to: {chat_id}')

        await asyncio.sleep(parse_timeout)

