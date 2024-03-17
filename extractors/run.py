from parser import RemoteOk
from job import Job, Jobs

terms=["machine-learning","front-end","react"]

#  RemoteOK
for term in terms:
    job = Jobs(term, RemoteOk())
    job.add_jobs()
    job.show_jobs()


# Other website