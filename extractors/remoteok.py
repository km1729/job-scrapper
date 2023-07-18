from bs4 import BeautifulSoup
import requests


def extract_jobs(term):
  url = f"https://remoteok.com/remote-{term}-jobs"
  request = requests.get(url, headers={"User-Agent": "Kimchi"})
  if request.status_code == 200:
    soup = BeautifulSoup(request.text, "html.parser")
    job_boards = soup.find(id='jobsboard')
    job_posts = job_boards.find_all('tr', class_='job', recursive=False)

    for job_post in job_posts:
      job_link = job_post.find('a', class_="preventLink")

      job_data = {
        'company': job_post.find('span', class_="companyLink").h3.string.replace('\n',''),
        'position': job_post.find('td', class_="company position company_and_position").h2.string.replace('\n',''),
        'location': job_post.find('div', class_="location").string.replace(',',''),
        'link': f"https://remoteok.com/{job_link['href']}",
        'keyword':{term}
      }
      print(job_data)
      print("////// \n")

    print(len(job_posts))
  else:
    print("Can't get jobs.")