from bs4 import BeautifulSoup
from urllib.parse import urljoin

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
