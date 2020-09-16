import pyxdameraulevenshtein as dl
import numpy as np
import itertools

items = ['a','b','c','d','e','f','g','h','i','j','k','l']

permutations = list(itertools.permutations(items,len(items)))
permutations = [''.join(x) for x in permutations]

dl_dist = []
x = 0

for x in range(0,len(permutations)):
    dist2 = dl.damerau_levenshtein_distance(permutations[0], permutations[x])
    dl_dist.append(dist2)
    x += 1

print(round(np.mean(dl_dist)/len(items),3))