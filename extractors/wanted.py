from playwright.sync_api import sync_playwright
import time 
from bs4 import BeautifulSoup

p = sync_playwright().start()

# create a browser
browser = p.chromium.launch(headless=False)
page = browser.new_page()
# go to a webpage
page.goto("https://www.wanted.co.kr/")

time.sleep(5)

page.click("button.Aside_searchButton__Xhqq3")

time.sleep(5)
# page.locator('button.Aside_searchButton__Xhqq3').click()

page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")
time.sleep(5)

page.keyboard.down('Enter')

time.sleep(5)

page.click("a#search_tab_position")
time.sleep(5)

for x in range(5):
    page.keyboard.down("End")
    time.sleep(5)

content = page.content()
soup = BeautifulSoup(content, "html.parser")
jobs = soup.find_all('div', class_="JobCard_container__FqChn JobCard_container--variant-card__znjV9")
for job in jobs:
    link = f"https://www.wanted.co.kr{job.find('a')['href']}"
    title = job.find("strong", class_='JobCard_title__ddkwM').text
    company_name = job.find('span', class_='JobCard_companyName__vZMqJ').text
    reward = job.find('span', class_='JobCard_reward__sdyHn').text

    job = {
        "title": title,
        "company": company_name,
        "reward": reward,
        "link": link
    }

    print(job)

p.stop()
