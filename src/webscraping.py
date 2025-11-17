import requests 
import pandas as pd 
import numpy as np 
import time
import random

from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_headers():
    """Returns standard browser headers to mimic human requests."""
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }

def get_rss(url, headers=None, max_retries=5):
    """Fetches and parses an RSS feed from the given URL."""
    if headers is None:
        headers = get_headers()
    
    delay = 1
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Attempt {attempt} to fetch RSS feed from {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            link = [a.get('href') for a in soup.find_all('a', href=True) if ('feed' in a.get('href')) or ('rss' in a.get('href'))]

            if not link:
                link = [l.get('href') for l in soup.find_all('link', href=True) if 
                                                                    ('feed' in l.get('href')) or 
                                                                    ('rss' in l.get('href')) or 
                                                                    ('/api' in l.get('rel')[0])
                                                                    ]

            if not link: 
                time.sleep(random.uniform(1, 3))
                return None
            if 'https' not in link[0]:
                time.sleep(random.uniform(1, 3))
                rss = urljoin(url, link[0])
            else:
                rss = link[0]
            
            response2 = requests.get(rss, headers=headers, timeout=10)
            response2.raise_for_status()

            time.sleep(2)
            return response2.content
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            if attempt == max_retries:
                print("Max retries reached. Failed to fetch RSS feed.")
                raise
            sleep_time = delay + random.uniform(0, 0.5)
            print(f"Retrying in {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
            delay *= 2

def xml_to_df(xml_content):
    """Converts RSS XML content to a pandas DataFrame."""
    if xml_content is None:
        return pd.DataFrame()
    soup = BeautifulSoup(xml_content, 'xml')

    title = []
    category = []
    author = []
    pubdate = []
    guid = []
    link = []
    description = []
    content = []

    for i in soup.find_all('item'):
        title_tag = i.find('title')
        title.append(title_tag.get_text(strip=True) if title_tag else '')

        cat = [c.text for c in i.find_all('category')]
        category.append(', '.join(cat))

        author_tag = i.find('author')
        author.append(author_tag.get_text(strip=True) if author_tag else None)

        pub_tag = i.find('pubDate')
        pubdate.append(pub_tag.get_text(strip=True) if pub_tag else None)

        guid_tag = i.find('guid')
        guid.append(guid_tag.get_text(strip=True) if guid_tag else None)

        link_tag = i.find('link')
        link.append(link_tag.get_text(strip=True) if link_tag else None)

        desc_tag = i.find('description')
        if desc_tag:
            description_soup = BeautifulSoup(desc_tag.text, 'html.parser')
            description.append(description_soup.get_text(" ", strip=True))
        else:
            description.append('')

        content_tag = i.find('content:encoded')
        if content_tag is not None:
            content_soup = BeautifulSoup(content_tag.text, 'html.parser')
            content.append(content_soup.get_text(" ", strip=True))
        else:
            content.append('')

    table = pd.DataFrame(
        {
            "title": title,
            "category": category,
            "author": author,
            "pubdate": pubdate,
            "guid": guid,
            "link": link,
            "description": description,
            "content": content,
        }
    )

    return table