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
            dict[criteria.get_text()] = False
        print(dict)
        return dict
        # for a_tag in soup.find_all('h2', class_='mt-6 font-unbounded text-xl font-bold'):
        #     print('Title:', a_tag.get_text())
        #     match = re.search(r'\((\d+) điểm\)', a_tag.get_text())
        #     if match:
        #         for b_tag in a_tag.find_next_siblings('div'):
        #             for div in b_tag:
        #                 div_h2 = 
        #             print('Contents:', b_tag.get_text())
    else:
        print('Failed to fetch the web page')