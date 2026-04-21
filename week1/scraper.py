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


# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By

# A class to represent a Webpage
# If you're not familiar with Classes, check out the "Intermediate Python" notebook

# Some websites need you to use proper headers when fetching them:
# headers = {
#  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
# }

# class Website:
#     def __init__(self, url):
#         self.url = url
#         self.title = None
#         self.text = None

#         # --- Try BeautifulSoup first ---
#         try:
#             response = requests.get(url, headers=headers, timeout=10)
#             soup = BeautifulSoup(response.content, 'html.parser')
#             self.title = soup.title.string if soup.title else "No title found"
#             for irrelevant in soup.body(["script", "style", "img", "input"]):
#                 irrelevant.decompose()
#             self.text = soup.body.get_text(separator="\n", strip=True)
#         except Exception:
#             self.text = None

#         # --- If BeautifulSoup fails or gets very little text, try Selenium ---
#         if not self.text or len(self.text) < 100:
#             try:
#                 options = Options()
#                 options.add_argument("--headless")
#                 options.add_argument("--no-sandbox")
#                 options.add_argument("--disable-dev-shm-usage")
#                 # No need to specify executable_path; Selenium Manager will handle the driver
#                 driver = webdriver.Chrome(options=options)
#                 driver.get(url)
#                 time.sleep(3)  # Wait for JS to load
#                 self.title = driver.title or self.title or "No title found"
#                 try:
#                     body = driver.find_element(By.TAG_NAME, "body")
#                     self.text = body.text
#                 except Exception:
#                     self.text = "No body text found"
#                 driver.quit()
#             except Exception as e:
#                 self.text = f"Selenium failed: {e}"
