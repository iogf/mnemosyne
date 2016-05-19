from random import randint
from datetime import datetime, timedelta
from os.path import expanduser, join, exists
from itertools import product
import pickle

class Mne(object):
    def __init__(self, show):
        self.pool = {}
        self.show = show

    def add(self, msg, years, months, days, hours, minutes):
        for ind in product(years, months, days, hours, minutes):
            time = datetime(*map(int, ind))
            if time > datetime.today():
                self.register(msg, time)

    def process(self):
        for indi, indj in self.pool.items():
            if datetime.today() > indi: 
                self.dispatch(indj, indi)

    def register(self, msg, time):
        if time < datetime.today(): return
        msgs = self.pool.setdefault(time, [])
        msgs.append(msg)

    def dispatch(self, msgs, time):        
        for ind in msgs[:]:
            self.show(ind, time)
        del self.pool[time]

    def load(self, filename):
        fd   = open(filename, 'r')
        pool = pickle.load(fd)
        fd.close()
        self.pool.update(pool)

    def save(self, filename):
        fd = open(filename, 'w')
        pickle.dump(self.pool, fd)
        fd.close()
