class Job:
  def __init__(self, title, company, location, link, keyword, salary=None, position=None):
    self.title = title
    self.company = company
    self.location = location
    self.link = link
    self.keyword = keyword
    self.salary = salary if salary is not None else "Not stated"
    self.position = position if position is not None else "Not stated"

  def introduce(self):    
    print (f" {self.title}, {self.company}, '{self.position}', {self.location}, {self.link}")


class Jobs:
  def __init__(self, keyword, parser):
    self.keyword = keyword
    self.parser = parser
    self.job_results = []

  def add_jobs(self):
    self.job_results = self.parser.parse_term(self.keyword)

  def show_jobs(self):
    print("\n", "*" * 20, self.keyword, "*"*20)
    for job in self.job_results:
      job.introduce()
      
