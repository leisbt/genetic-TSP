import numpy as np
import matplotlib.pyplot as plt
from time import time

timer = time()
coords = [[52.9, 13.0],
          [55.0, 14.4],
          [54.7, 15.8],
          [55.1, 15.4],
          [55.6, 15.7],
          [50.6, 16.3],
          [56.1, 18.2],
          [48.5, 18.6],
          [57.1, 24.3],
          [55.0, 30.2],
          [56.1, 30.5],
          [57.0, 30.0],
          [46.5, 80.3]]
c_len = len(coords)
census_default = 40
choice_weight = 40
mutate_chance = 5 / 100


class Population:
    def __init__(self, census):
        self.paths = [list(np.random.choice(c_len, c_len, replace=False)) for _ in range(census)]
        self.d_list = [np.sum(np.sum((a - np.roll(a, -1, axis=2)) ** 2, axis=1) ** 0.5, axis=1)
                       for a in [[np.transpose([coords[b] for b in self.paths[c]]) for c in range(census)]]][0]
        self.d_list_mod = self.d_list ** choice_weight
        self.p_list = [a/b for b in [sum(self.d_list_mod)] for a in self.d_list_mod]
        self.bestd = np.min(self.d_list)
        self.bestpath = [a for a in self.paths[list(self.d_list).index(self.bestd)]]

    def evolve(self):
        self.paths[0] = [a for a in self.bestpath]
        self.d_list[0] = self.bestd
        lchoices = np.random.choice(list(range(census_default)), 2, p=self.p_list, replace=False)
        hchoicescm2 = np.random.choice(list(range(census_default)), census_default - 2, p=self.p_list, replace=False)
        hchoices = [a for a in list(range(census_default))
                    if a not in hchoicescm2]
        a = self.paths[hchoices[0]]
        b = a[c_len // 3:c_len // 3 * 2]
        c = [list(self.paths[lchoices[0]]).index(z) for z in b]
        d = np.roll(np.delete(self.paths[lchoices[0]], c), -c_len // 3)
        e = np.insert(d, c_len // 3, b)
        f = self.paths[hchoices[1]]
        g = f[c_len // 3:c_len // 3 * 2]
        h = [list(self.paths[lchoices[1]]).index(z) for z in g]
        i = np.roll(np.delete(self.paths[lchoices[1]], h), -c_len // 3)
        j = np.insert(i, c_len // 3, g)
        for a in range(len(self.paths)):
            c = np.random.rand()
            if c < mutate_chance / 10:
                self.paths[a] = list(np.random.choice(c_len, c_len, replace=False))
            for b in range(len(self.paths[a])):
                if c < mutate_chance:
                    m = self.paths[a][b]
                    n = np.random.randint(0, c_len)
                    tmp = m
                    self.paths[a][b] = self.paths[a][n]
                    self.paths[a][n] = tmp
                    np.random.randint(0, c_len)
        self.paths[lchoices[0]], self.paths[lchoices[1]] = e, j
        self.d_list[lchoices[0]] = np.sum(np.sum([z - np.roll(z, -1, axis=1) for z in
                                                 [np.transpose([coords[z] for z in e])]][0] ** 2, axis=0) ** 0.5)
        self.d_list[lchoices[1]] = np.sum(np.sum([z - np.roll(z, -1, axis=1) for z in
                                                 [np.transpose([coords[z] for z in j])]][0] ** 2, axis=0) ** 0.5)
        self.d_list_mod = self.d_list ** choice_weight
        self.p_list = [a/b for b in [sum(self.d_list_mod)] for a in self.d_list_mod]
        self.d_list_mod = self.d_list ** choice_weight
        self.p_list = [a/b for b in [sum(self.d_list_mod)] for a in self.d_list_mod]
        if np.min(self.d_list) < self.bestd:
            self.bestd = np.min(self.d_list)
            self.bestpath = [a for a in self.paths[list(self.d_list).index(self.bestd)]]

    @classmethod
    def generate(cls, census=census_default):
        return cls(census)


pop = Population.generate()
loops = 100000
totald = [None] * loops
bestd = [None] * loops

for loop in range(loops):
    pop.evolve()
    totald[loop] = sum(pop.d_list)
    bestd[loop] = pop.bestd
    print(round(loop/loops, 3), pop.bestd)
fig = plt.figure()
fig.add_subplot(311)
plt.plot(list(range(loops)), totald)
fig.add_subplot(312)
plt.plot(list(range(loops)), bestd)
fig.add_subplot(313)
plt.plot(np.append(np.transpose([coords[i] for i in pop.bestpath])[0],
                   np.transpose([coords[i] for i in pop.bestpath])[0][0]),
         np.append(np.transpose([coords[i] for i in pop.bestpath])[1],
                   np.transpose([coords[i] for i in pop.bestpath])[1][0]), 'go-')
print(time() - timer)
plt.show()
