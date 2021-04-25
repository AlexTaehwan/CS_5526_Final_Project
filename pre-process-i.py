# Pre-Process DRKG 

import pickle
with open("DRKG_mapped.txt", "rb") as fp:
    DRKG = pickle.load(fp)
    
DRKG_new = DRKG
print("START")
from collections import defaultdict
entity = defaultdict(int)
relations = defaultdict(int)

# Make a dictioanry that holds the DRKG entity and relation counts
for (s,r,e) in DRKG_new:
    entity[s] += 1
    entity[e] += 1
    relations[r] += 1
    
from collections import defaultdict
source_dict = defaultdict(list)
for (s,r,e) in DRKG_new:
    source_dict[e].append((s, (r,)))

note = defaultdict()

train_ans = defaultdict(set)

# Build train_ans_2i and train_triples_2i
for source_node in source_dict:
    shared_nodes = source_dict[source_node]
    if len(shared_nodes) >= 2:
        for i in range(len(shared_nodes)):
            for j in range(i+1,len(shared_nodes)):
                if (shared_nodes[j], shared_nodes[i]) in train_ans:
                    train_ans[shared_nodes[j], shared_nodes[i]].add(source_node)
                else:
                    train_ans[shared_nodes[i], shared_nodes[j]].add(source_node)

                
    else:
        pass

import random
keys = random.sample(list(train_ans), 284925)
train_ans_mod = {k: train_ans[k] for k in keys}

import pickle
with open('train_ans_2i_n.pkl', 'wb') as f:
    pickle.dump(train_ans_mod, f)
print("Done")
train_triples = []
for node in train_ans:
    train_triples.append((node[0], node[1], 0, '2-inter'))

with open('train_triples_2i_n.pkl', 'wb') as f:
    pickle.dump(train_triples, f)
    
train_ans_3i = defaultdict(set)

# Build train_ans_3i and train_triples_3i

for source_node in source_dict:
    shared_nodes = source_dict[source_node]
    if len(shared_nodes) >= 3:
        for i in range(len(shared_nodes)):
            for j in range(i+1,len(shared_nodes)):
                for k in range(j+1, len(shared_nodes)):
                    if (shared_nodes[i], shared_nodes[k], shared_nodes[j]) in train_ans_3i:
                        train_ans_3i[shared_nodes[i], shared_nodes[k], shared_nodes[j]].add(source_node)
                    elif (shared_nodes[k], shared_nodes[i], shared_nodes[j]) in train_ans_3i:
                        train_ans_3i[shared_nodes[k], shared_nodes[i], shared_nodes[j]].add(source_node)
                    elif (shared_nodes[k], shared_nodes[j], shared_nodes[i]) in train_ans_3i:
                        train_ans_3i[shared_nodes[k], shared_nodes[j], shared_nodes[i]].add(source_node)
                    elif (shared_nodes[j], shared_nodes[i], shared_nodes[k]) in train_ans_3i:
                        train_ans_3i[shared_nodes[j], shared_nodes[i], shared_nodes[k]].add(source_node) 
                    elif (shared_nodes[j], shared_nodes[k], shared_nodes[i]) in train_ans_3i:
                        train_ans_3i[shared_nodes[j], shared_nodes[k], shared_nodes[i]].add(source_node)
                    else:
                        train_ans_3i[shared_nodes[i], shared_nodes[j], shared_nodes[k]].add(source_node)


    else:
        pass
    
import random
keys = random.sample(list(train_ans_3i), 284925)
train_ans_3i_mod = {k: train_ans_3i[k] for k in keys}

with open('train_ans_3i_n.pkl', 'wb') as f:
    pickle.dump(train_ans_3i_mod, f)

train_triples_3i = []
for node in train_ans_3i:
    train_triples_3i.append((node[0], node[1], node[2], 0, '3-inter'))
with open('train_triples_3i_n.pkl', 'wb') as f:
    pickle.dump(train_triples_3i, f)
