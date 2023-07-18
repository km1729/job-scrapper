from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import re

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
browser = webdriver.Chrome(options=options)


def get_page_count(keywords):
  # print(f"https://kr.indeed.com/jobs?q={keywords}")
  browser.get(f"https://kr.indeed.com/jobs?q={keywords}")
  soup = BeautifulSoup(browser.page_source, "html.parser")

  # nav tag안애 div 태그로 페이지네이션을 보여주고 있다.
  # pagenation = None으로 했을 경우 에러가 나서
  # div 갯수 유무로 처리 했다.
  # div 갯수가 0, 즉 [] empty인 리스트라면 1을 리턴한다.
  pagination = soup.find('nav', class_='css-jbuxu0')
  pages = pagination.find_all('div', recursive=False)

  if pages == []:
    print(f"{keywords}: {len(pages)}")
    return 1
  else:
    if len(pages) >= 5:
      print(f"{keywords}: {len(pages)}, it returns 5")
      return 5
    else:
      print(f"{keywords}: {len(pages)}")
      return len(pages)


def extract_indeed_jobs(keywords):
  """
  키워드에 맞는 잡을 indeed 웹사이트에서 검색하고, 
  검색결과를 json 파일로 (포지션, 회사이름, 회사위치, 잡링크) 저장
  """
  # get number of pages
  pages = get_page_count(keywords)
  print("Found", pages, "pages")

  # extract jobs depneds on the # of pages
  results = []

  for page in range(pages):
    # update url to match to the page #
    # page # 0 = 0, page #1 = 10, #2 = 20, #3=30, #4=40, #5=50
    browser.get(f"https://kr.indeed.com/jobs?q={keywords}&start={page*10}")
    final_url = f"https://kr.indeed.com/jobs?q={keywords}&start={page*10}"
    print("Requesting", final_url)
    soup = BeautifulSoup(browser.page_source, "html.parser")

    jobs = soup.find('div', class_='mosaic mosaic-provider-jobcards')
    # !!!!! this parts often results in error. re-run will solve the problem
    job_posts = jobs.select('ul li', recursive=False)

    for job_post in job_posts:
      zone = job_post.find('table', class_='jobCard_mainContent')
      if zone != None:
        # Job title
        job_title = zone.find(
          'span', id=lambda value: value and value.startswith('jobTitle'))

        # Job company and location
        company = zone.find('span', class_='companyName')
        location = zone.find('div', class_='companyLocation')

        # Job link
        anchor = zone.select_one('h2 a')
        link = re.search(r"jk=([a-zA-Z0-9]+)&fccid", anchor['href'])
        if link == None:
          job_link = "none"
        else:
          job_link = f"https://kr.indeed.com/jobs?q=python&vjk={link.group(1)}"

        job_data = {
          'company': company.string.replace(',', ''),
          'location': location.string.replace(',', ''),
          'position': job_title['title'].replace(',', ''),
          'link': job_link
        }
        results.append(job_data)

  return results
