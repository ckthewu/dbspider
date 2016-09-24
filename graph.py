# -*- coding : utf-8 -*-
from cmath import log
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.mlab import PCA
import codecs,json,re


file = codecs.open('scraped_data_utf8.json','r',encoding='utf-8')
i = 0
tl = []
ndsize = {}
H = []
while i<40:
    l = json.loads(file.readline(),encoding='utf-8')
    ndsize[l['groupid']]=log(float(l['membersnum']))*10
    tl.append(l)
    i += 1

G = nx.Graph()
for l in tl:
    G.add_node(l['groupid'])
    H.append(l['groupid'])
    for bg in l['bdgroupsid']:
        G.add_edge(l['groupid'],bg)
        # print 'add edge from %s to %s' % (l['groupid'],bg)


nx.draw(G,pos=nx.spring_layout(G),node_size=[ndsize[v] for v in H])
plt.show()

file.close()