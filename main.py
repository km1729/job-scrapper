from extractors.wwr import extract_wwr_jobs
from extractors.indeed import extract_indeed_jobs
from extractors.workforceaustralia import extract_workforceaustralia_jobs
from extractors.remoteok import extract_jobs

# keyword = input("what do you want to search for? ")
keyword = 'python'

wfaus = extract_workforceaustralia_jobs(keyword)
indeed = extract_indeed_jobs(keyword)
wwr = extract_wwr_jobs(keyword)
remoteok = extract_jobs(keyword)

jobs = wfaus + indeed + wwr + remoteok

file = open(f"{keyword}.csv", "w")

file.write("Position, Company,Location, URL\n")
for job in jobs:
  file.write(
    f"{job['position']},{job['company']},{job['location']},{job['link']}\n")
file.close()
