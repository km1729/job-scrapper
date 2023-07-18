from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import re

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
browser = webdriver.Chrome(options=options)


def get_page_count(keywords):
  """
  https://www.workforceaustralia.gov.au/ 
  입력한 키워드를 검색하고 키워드로 출력된 page 갯수 구하기
  """
  browser.get(
    f"https://www.workforceaustralia.gov.au/individuals/jobs/search?searchText={keywords}"
  )
  soup = BeautifulSoup(browser.page_source, "html.parser")
  pagination = soup.find('nav', class_="mint-pagination")
  pages = pagination.select('ul li', recursive=False)

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


def extract_workforceaustralia_jobs(keywords):
  """
  키워드에 맞는 포지션 workforceaustralia 웹사이트에서 검색하고,  
  검색결과를 json 파일로 (포지션, 회사이름, 회사위치, 잡링크) 저장
  """
  # get number of pages
  pages = get_page_count(keywords)
  print("Found", pages, "pages")

  # extract jobs depneds on the # of pages
  results = []

  for page in range(pages):
    #   # update url to match to the page #
    #   # page # 0 = 0, page #1 = 10, #2 = 20, #3=30, #4=40, #5=50
    # browser.get(f"https://www.workforceaustralia.gov.au/individuals/jobs/search?searchText={keywords}?&pageNumber={page}")
    browser.get(
      f"https://www.workforceaustralia.gov.au/individuals/jobs/search?searchText={keywords}&pageNumber={page+1}"
    )
    final_url = f"https://www.workforceaustralia.gov.au/individuals/jobs/search?searchText={keywords}&pageNumber={page+1}"
    print("Requesting", final_url)
    soup = BeautifulSoup(browser.page_source, "html.parser")

    jobs = soup.find('div', class_='results-list')

    job_posts = jobs.select('section', recursive=False)
    for job_post in job_posts:

      position = job_post.find('h5', class_="title").a.text
      job_link = job_post.find('h5', class_="title").a['href']
      link = f"https://www.workforceaustralia.gov.au{job_link}"

      # move to next page to get company name and location
      browser.get(link)
      soup2 = BeautifulSoup(browser.page_source, "html.parser")
      job_description = soup2.find('div', class_="mint-card")
      company = re.search("<b> company:</b> ([^<]+)", str(job_description))
      if company == None:
        company_name = "Not provided"
      else:
        company_name = company.group(1)

      location = re.search("<b> Location:</b> ([^<]+)", str(job_description))
      if location == None:
        company_location = "Not provided"
      else:
        company_location = location.group(1)


      job_data = {
        'company': company_name,
        'location': company_location,
        'position': position.replace(',', ''),
        'link': link
      }

      results.append(job_data)

  return results
