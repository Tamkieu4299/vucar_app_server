from bs4 import BeautifulSoup
import requests
import re

url = 'https://www.vucar.vn/vi/loi-ich-cua-ban/danh-sach-chi-tiet'
response = requests.get(url)

# Check if the request was successful (status code 200)
def get_criterias():
    dict = {}
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        for criteria in soup.find_all('h3', class_="flex items-center gap-2"):
            dict[criteria.get_text()] = {"status": False , "note": "Not yet checked"}
        return dict
    else:
        print('Failed to fetch the web page')
