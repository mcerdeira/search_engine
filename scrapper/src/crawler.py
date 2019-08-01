import sys
import os
import traceback
from urllib.request import urlopen
from urllib import robotparser
from bs4 import BeautifulSoup
import sqlite3
from multiprocessing import Process
import extractor, db_actions

COMMIT_EVERY = 100
conn = sqlite3.connect('crawled_web.db')
_cursor = conn.cursor()

count = 0
urls = [("https://www.infobae.com", "https://www.infobae.com" )] #0: base_url, 1: url
found_urls = ["/?noredirect"]
already_fetched = []
LOG_FILE = None


def start_crawl():
    global urls
    last_url = ""
    intial_url_load()
    i = 0
    while(True):
        url = urls[i]
        print(str(len(urls)))
        if(not url[1].startswith("/") and url[0] != last_url):
            last_url = url[0]
            robots = get_robots(url[1])
        crawl(robots, url)
        urls = list(set(urls))
        i += 1
        if i - 1 >= len(urls):
            break

def intial_url_load():
    global urls
    sql = "SELECT url FROM result"
    rows = _cursor.execute(sql)
    for r in rows.fetchall():
        found = [u for u in urls if u[1] == r[0]]
        if(len(found) == 0):
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
    global urls
    base_url = url[0]
    global count
    count += 1
    try:
        # Is same domain or relative URL
        if base_url in url[1] or url[1].startswith("/"):
            valid = False
            if(url[1].startswith("/")):                
                tmpurl = url[1]
                url = (base_url, base_url + tmpurl)
                valid = True
            else:
                url1 = base_url
                url2 = base_url.replace("https", "http")
                if(url[1].startswith(url1) or url[1].startswith(url2)):
                    valid = True
                else:
                    valid = False

            if(valid and not url[1] in found_urls and (robots.can_fetch("*", url[1]) or robots is None)):
                html = urlopen(url[1])
                print(url[1])
                found_urls.append(url[1])
                dump(robots, url, html)
            else:
                print("Skiped: " + url[1])

    except Exception as e:
        found_urls.append(url[1])
        LOG_FILE.write(url[1] + ": " + str(e) + " " + repr(e) +
                       " " + traceback.format_exc() + "\n\n")
        LOG_FILE.write("---------------------------------------------")

        print("ERROR: " + str(e))
        print(repr(e))
        traceback.print_exc()


def dump(robots, url, content):
    global urls
    try:
        base_url = url[0]
        # 0001 TODO: This part must be a separate process, using extractor class
        soup = BeautifulSoup(content, 'html.parser')
        if(soup.title):
            title = soup.title.text
        else:
            title = ""
        # 0001

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
    except Exception as e:
        LOG_FILE.write(url[1] + ": " + str(e) + " " + repr(e) +
                       " " + traceback.format_exc() + "\n\n")
        LOG_FILE.write("---------------------------------------------")

        print("ERROR: " + str(e))
        print(repr(e))
        traceback.print_exc()

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
