import pickle
import random

with open("DRKG_mapped.txt", "rb") as fp:
    DRKG = pickle.load(fp)

DRKG_new = DRKG

from collections import defaultdict
node_rel = defaultdict(list)
for (s,r,_) in DRKG_new:
    node_rel[s].append(r)

# save node and relation data in the dictionary
for node in node_rel:
    node_rel[node] = list(set(node_rel[node]))

    
# pre process 1p
from collections import defaultdict

train_triples = []
train_ans = defaultdict(set)

for (s, r, e) in DRKG_new:
    train_ans[((s, (r,)),)].add(e)
    
for key in train_ans:
    train_triples.append(((key[0][0], key[0][1] ,0), '1-chain'))

with open('train_triples_1c_n.pkl', 'wb') as f:
    pickle.dump(train_triples, f)
with open('train_ans_1c_n.pkl', 'wb') as f:
    pickle.dump(train_ans, f)

# Read 1c data
with open('train_triples_1c_n.pkl', 'rb') as f:
    train_triples_1c = pickle.load(f)
with open('train_ans_1c_n.pkl', 'rb') as f:
    train_ans_1c = pickle.load(f)

# pre process 2p
from collections import defaultdict
train_ans = defaultdict(set)
train_triples = []

for fn_rel in train_ans_1c: # first node and relation
    for sn in train_ans_1c[fn_rel]: # second node
        if sn in node_rel:
            for rel in node_rel[sn]: # relation from second node
                train_ans[((fn_rel[0][0], (fn_rel[0][1][0], rel)),)] = train_ans_1c[((sn, (rel,)),)]

# randomly select 284925 due to the memory issue  
keys = random.sample(list(train_ans), 284925)
train_ans_mod = {k: train_ans[k] for k in keys}

train_triples = []
for key in train_ans_mod:
    train_triples.append(((key[0][0], (key[0][1][0], key[0][1][1]), 0), '2-chain'))

with open('train_triples_2c_n.pkl', 'wb') as f:
    pickle.dump(train_triples, f)
with open('train_ans_2c_n.pkl', 'wb') as f:
    pickle.dump(train_ans_mod, f)    
# Read 2c data
with open('train_triples_2c_n.pkl', 'rb') as f:
    train_triples_2c = pickle.load(f)
with open('train_ans_2c_n.pkl', 'rb') as f:
    train_ans_2c = pickle.load(f)

    
    
train_ans = defaultdict(set)
train_triples = []    
for fn_rel in train_ans_2c: # first node and relation
    for tn in train_ans_2c[fn_rel]: # third node
        if tn in node_rel:
            for rel in node_rel[tn]: # relation from third node
                train_ans[((fn_rel[0][0], (fn_rel[0][1][0], fn_rel[0][1][1], rel)),)] = train_ans_1c[((tn, (rel,)),)]

# randomly select 284925 due to the memory issue                  
keys = random.sample(list(train_ans), 284925)
train_ans_mod = {k: train_ans[k] for k in keys}                

for key in train_ans_mod:
    train_triples.append(((key[0][0], (key[0][1][0], key[0][1][1], key[0][1][2]), 0), '3-chain'))

import pickle
with open('train_triples_3c_n.pkl', 'wb') as f:
    pickle.dump(train_triples, f)
with open('train_ans_3c_n.pkl', 'wb') as f:
    pickle.dump(train_ans_mod, f)
    

