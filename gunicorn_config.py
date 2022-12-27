import os

def num_cpus():
    try:
        return len(os.sched_getaffinity(0))
    except AttributeError:
        return os.cpu_count()

def max_workers():
    return (num_cpus() * 2) + 1

logfile = "gunicorn.log"
bind = "194.233.173.32:5000"
workers = max_workers()
timeout = 300