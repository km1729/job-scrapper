from job import Job, Jobs
from bs4 import BeautifulSoup
import requests

class ParserInterface:
    def parse(self, term):
        raise NotImplementedError
    
class RemoteOk(ParserInterface):
    def parse_term(self, term):
        jobs_list = []
        url = f"https://remoteok.com/remote-{term}-jobs"
        request = requests.get(url, headers={"User-Agent": "Kimchi"})

        if request.status_code == 200:
            soup = BeautifulSoup(request.text, "html.parser")
            job_boards = soup.find(id='jobsboard').find_all('tr', class_='job', recursive=False)

            for job in job_boards:
                company = job.find("h3", itemprop="name").text.strip()
                title = job.find("td", class_="company").find("h2", itemprop="title").text.strip()
                print(title)
                location_salary = job.find("td", class_="company").find_all("div", class_="location")
                salary = location_salary[-1].text
                link= "/abc"
                if len(location_salary) > 2:
                    location_texts = [loc.text.strip() for loc in location_salary[:-1]] 
                    location = ', '.join(location_texts)
                else:
                    location = location_salary[0].text.strip()               
                new_job = Job(title=title, company=company, link=link,location=location,salary=salary,keyword=term)
                jobs_list.append(new_job)
        return jobs_list
                
    