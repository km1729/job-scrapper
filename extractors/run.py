from parser import RemoteOk
from job import Job, Jobs

term="machine-learning"


#  RemoteOK
ml_job = Jobs(term, RemoteOk())

ml_job.add_jobs()
ml_job.show_jobs()


# Other website