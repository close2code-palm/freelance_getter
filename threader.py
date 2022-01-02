import multiprocessing
import threading

from flsite import Site


class Scanner:

    def __init__(self, *sites, max_threads=4):
        self.resources: [Site] = [sites]
        self.threads = max_threads

    def runner_h(self):
        tq = multiprocessing.Queue(self.threads)
        for site in self.resources:
            tq.put(threading.Thread(target=site.scrape, daemon=False))

    def runner_all(self):
        for site in
