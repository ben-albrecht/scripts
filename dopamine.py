#!/usr/bin/env python

"""
Questions

- Is it better to poll the TTY or have every shell command execute
      something under the hood?

Tasks

- [ ] Figure out how to get all active processes owned by a specific TTY
- [ ] Figure out how to sort processes by their start time
- [ ] Figure out best way to determine when a process ends
- [ ] Figure out how to get the exit code of a process that ended

"""

import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = '/Users/balbrecht/.exit-logs'
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



"""
import psutil
from pprint import pprint as pp
import getpass

## Iterate over all running process
#for proc in psutil.process_iter():
#    try:
#        # Get process name & pid from process object.
#        processName = proc.name()
#        processID = proc.pid
#        print(processName , ' ::: ', processID)
#    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#        pass

pp([(p.pid, p.info['name']) for p in psutil.process_iter(['name', 'username']) if p.info['username'] == getpass.getuser()])

#(16832, 'bash'),
#(19772, 'ssh'),
#(20492, 'python')]
"""
