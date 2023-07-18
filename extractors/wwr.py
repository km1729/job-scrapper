from requests import get
from bs4 import BeautifulSoup


def extract_wwr_jobs(keyword):
  base_url = 'https://weworkremotely.com/remote-jobs/search?term='
  response = get(f"{base_url}{keyword}")

  if response.status_code != 200:
    print("Can't request website")
  else:
    results = []
    # html doc = response.text
    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup.find_all('title'))
    jobs = soup.find_all('section', class_="jobs")
    print(len(jobs))
    for job_section in jobs:
      # list of li
      job_post = job_section.find_all('li')
      job_post.pop(-1)
      for post in job_post:
        anchors = post.find_all('a')
        anchor = anchors[1]
        # link만 가져올 수 있음
        link = anchor['href']
        company, kind, region = anchor.find_all('span', class_='company')
        title = anchor.find('span', class_='title')
        # print(company.string, kind.string, region.string, title.string)
        # print('///////////////////////////')
        # print('///////////////////////////')
        job_data = {
          'company': company.string.replace(',', ''),
          'location': region.string.replace(',', ''),
          'position': title.string.replace(',', ''),
          'link':'none'
        }
        results.append(job_data)

    return results