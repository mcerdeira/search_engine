import sys
import os
import traceback
from urllib.request import urlopen
from urllib import robotparser
from bs4 import BeautifulSoup
import sqlite3

COMMIT_EVERY = 100
conn = sqlite3.connect('crawled_web.db')
_cursor = conn.cursor()

count = 0
urls = [("https://www.infobae.com", "https://www.infobae.com" )] #0: base_url, 1: url
found_urls = ["/?noredirect"]
already_fetched = []
LOG_FILE = None


def start_crawl():
    intial_url_load()
    for url in urls:
        robots = get_robots(url[1])
        crawl(robots, url)

def intial_url_load():
    sql = "SELECT url FROM result"
    rows = _cursor.execute(sql)
    for r in rows.fetchall():
        if r[0] not in urls:
            already_fetched.append(r[0])

def get_robots(url):
    try:
        url = url + "/robots.txt"
        rp = robotparser.RobotFileParser()
        rp.set_url(url)
        rp.read()
        return rp
    except Exception as e:
        print(str(e))
        return None


def crawl(robots, url):
    base_url = url[0]
    global count
    count += 1
    try:
        # Is same domain or relative URL
        if base_url in url[1] or url.startswith("/"):
            valid = False
            if(url.startswith("/")):
                url = base_url + url[1]
                valid = True
            else:
                url1 = base_url
                url2 = base_url.replace("https", "http")
                if(url.startswith(url1) or url.startswith(url2)):
                    valid = True
                else:
                    valid = False

            if(valid and not url[1] in found_urls and (robots.can_fetch("*", url) or robots is None)):
                html = urlopen(url[1])
                print(url[1])
                found_urls.append(url[1])
                dump(robots, url, html)
            else:
                print("Skiped: " + url)

    except Exception as e:
        found_urls.append(url[1])
        LOG_FILE.write(url[1] + ": " + str(e) + " " + repr(e) +
                       " " + traceback.format_exc() + "\n\n")
        LOG_FILE.write("---------------------------------------------")

        print("ERROR: " + str(e))
        print(repr(e))
        traceback.print_exc()


def dump(robots, url, content):
    base_url = url[0]
    soup = BeautifulSoup(content, 'html.parser')
    title = soup.title.text

    if not url[1] in already_fetched:
        already_fetched.append(url[1])
        sql = "INSERT INTO result VALUES (?, ?, ?)"
        _cursor.execute(sql, (url[1], title, soup.prettify(), ))

        if(count % COMMIT_EVERY == 0):
            conn.commit()

    for link in soup.find_all('a'):
        newlink = link.get('href')
        if(newlink and newlink not in found_urls):
            urls.append((base_url, newlink))
            #crawl(robots, base_url, newlink.strip())


if __name__ == '__main__':
    try:
        sys.setrecursionlimit(1000000000)
        LOG_FILE = open("log.txt", "w+")
        start_crawl()
        LOG_FILE.close()
        conn.commit()
        conn.close()
    except KeyboardInterrupt:
        print('Interrupted!!!!!!!!!!!')
        LOG_FILE.close()
        conn.commit()
        conn.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
