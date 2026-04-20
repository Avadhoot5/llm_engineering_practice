import requests
from bs4 import BeautifulSoup

# Standard headers to fetch a website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

def fetch_website_contents(url):
    '''
    Return the title and contents of the website at the given url
    '''
    # https://edwarddonner.com/ 
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else 'No Title Found'
    if soup.body:
        for irrelevant in soup.body(['img', 'script','style', 'input']):
            irrelevant.decompose()
        text = soup.body.get_text(separator='\n', strip=True)
    else:
        text = ''
    
    return (title + '\n\n' + text)[:2000]
