class Epgp_table():

    def __init__(self):
        self.table = {}
        self.decay_ratio = 0.1


    def add_worker(self, name, ep, gp):
        self.table[name] = {"ep": ep, "gp": gp}

    def remove_worker(self, name):
        del self.table[name]

    def get_entry(self, name):
        return self.table[name]

    def get_ep(self, name):
        return self.table[name]["ep"]

    def get_gp(self, name):
        return self.table[name]["gp"]

    def get_pr(self, name):
        return self.get_ep(name) / self.get_gp(name)

    def add_ep(self, name, amount):

        if name not in self.table:
            self.add_worker(name)

        self.table[name]["ep"] += amount

    def add_gp(self, name, amount):

        if name not in self.table:
            self.add_worker(name)

        self.table[name]["gp"] += amount

    def apply_decay(self):
        for name in  self.table:
            self.table[name]['ep'] *= (1-self.decay_ratio)
            self.table[name]['gp'] *= (1-self.decay_ratio)


