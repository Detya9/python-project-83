from bs4 import BeautifulSoup


def get_seo_content(html_content):
    soup = BeautifulSoup(html_content, "lxml")
    h1 = soup.find('h1')
    title = soup.find('title')
    meta = soup.find('meta', {'name': 'description'})
    if meta:
        description = meta.get('content')
    else:
        description = ''
    return {
        'h1': h1.text if h1 else '',
        'title': title.text if title else '',
        'description': description
    }
