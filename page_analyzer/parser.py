from bs4 import BeautifulSoup


def get_dict_content(html_content):
    soup = BeautifulSoup(html_content, "lxml")
    h1 = soup.find('h1')
    title = soup.find('tittle')
    meta = soup.find('meta', {'name': 'description'})
    if meta:
        description = meta.get('content')
    else:
        description = None
    return {
        'h1': h1.text if title else None,
        'title': title.text if title else None,
        'description': description
    }
