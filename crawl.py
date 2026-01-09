import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def normalize_url(input_url: str) -> str:
    if 'https://' in input_url: input_url = input_url[8:]
    elif 'http://' in input_url: input_url = input_url[7:]
    
    if input_url[-1] == '/': input_url = input_url[:-1]

    return input_url.lower()

def get_h1_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    h1 = soup.find('h1')

    return h1.get_text(strip=True) if h1 else ''

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    
    main = soup.find('main')
    if main is None:
        p = soup.find('p')
        return p.get_text() if p else ''

    p = main.find('p') 
    return p.get_text() if p else ''

def get_urls_from_html(html, base_url: str) -> list:
    collected_links = []
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')

    for link in links:
        try:
            link = link.get('href')
            collected_links.append(urljoin(base_url, link))
        except Exception as e:
            print(f'{str(e)}: {link}')
 
    return collected_links

def get_images_from_html(html, base_url: str) -> list:
    collected_links = []
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('img')
    
    for link in links:
        try:
            link = link.get('src')
            collected_links.append(urljoin(base_url, link))
        except Exception as e:
            print(f'{str(e)}: {link}')
        
    return collected_links

def extract_page_data(html, page_url: str) -> dict:
    title = get_h1_from_html(html)
    paragraph = get_first_paragraph_from_html(html)
    out_links = get_urls_from_html(html, page_url)
    img_links = get_images_from_html(html, page_url)

    return {
        'url': page_url,
        'h1': title,
        'first_paragraph': paragraph,
        'outgoing_links': out_links,
        'image_urls': img_links
    }

def get_html(url: str):
    accept_var = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    headers = {'User-Agent': 'MiniCrawler/1.0', 'Accept': accept_var}
    try: response = requests.get(url, headers=headers)
    except Exception as e: print(f'error: {e}')

    if response.status_code >= 400:
        raise Exception(f'error: {response.status_code}, {response.reason}') 
    if  'text/html' not in response.headers.get('Content-Type', ''):
        actual_content_type = response.headers['Content-Type']
        raise Exception(f'error: content type is not text/html but {actual_content_type}') 

    return response.text

def crawl_page(base_url, current_url=None, page_data=None):
    if current_url is None: current_url = base_url
    if page_data is None: page_data = {}

    current_url_parsed = urlparse(current_url)
    base_url_parsed = urlparse(base_url)
    if current_url_parsed.netloc != base_url_parsed.netloc: return page_data

    normalized_url =  normalize_url(current_url)
    if normalized_url in page_data: return page_data

    webpage = get_html(current_url)
    page_data[normalized_url] = extract_page_data(webpage, current_url)
    print(f'crawled: {current_url}')

    all_links = get_urls_from_html(webpage, current_url) 
    for link in all_links:
        try: crawl_page(base_url, link, page_data)
        except: continue

    return page_data
