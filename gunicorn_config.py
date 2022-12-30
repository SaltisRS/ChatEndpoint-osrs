import os
import configparser

def num_cpus():
    try:
        return len(os.sched_getaffinity(0))
    except AttributeError:
        return os.cpu_count()

def max_workers():
    return (num_cpus() * 2) + 1

# Read configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Set bind variable from configuration file
ip = config['SETTINGS']['ip']
port = config['SETTINGS']['port']
bind = f"{ip}:{port}"

logfile = "gunicorn.log"
workers = max_workers()
timeout = 300
