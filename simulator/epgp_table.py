class Epgp_table():

    def __init__(self):
        self.table = {}
        

    def add_worker(self, name):
        self.table[name] = {"ep": 400, "gp": 400}

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

        self.table[name]["ep"] = self.table[name]["ep"] + amount

    def add_gp(self, name, amount):

        if name not in self.table:
            self.add_worker(name)

        self.table[name]["gp"] += amount
