# network_topology.py - script to calculate the bridging centrality [http://gbe.oxfordjournals.org/content/2/815.long]
# C: Jan 31, 2012
# M: Mar 10, 2017
# A: Leandro Lima <leandro.lima@gladstone.ucsf.edu>

import sys
import networkx as nx
import operator
from symbol_geneid import convert

network_file = sys.argv[1]
gene_info_file = sys.argv[2]

G = nx.Graph()

seeds = open('seeds.txt').read().replace('\r', '').split('\n')
while seeds[-1] == '':
    seeds.pop()

lines = open(network_file).read().replace('\r', '').split('\n')

# Creating network
for line in lines[1:]:
    if line != '':
        g1,g2 = line.split('\t')
        G.add_edge(g1,g2)

## ## ##
# Bridging centrality (C_Bdg) measures the extent to which a node or an edge is located between well-connected regions
# C_Bdg(i) = C_Btw(i) x BC(i)
#
# where BC(i) is the bridging coefficient that assesses the local
# bridging characteristics in the neighborhood of node i, which is defined as
#
# BC(i) = degree(i)^-1 / SUM_{v in ngbd(i)} [1 / degree(v)]
## ## ##

print 'Betweenness...'
betweenness_dic = nx.betweenness_centrality(G)

print 'Clustering...'
clustering_dic = nx.clustering(G)

# Getting maximum degree
print 'Degree...'
degree_dic = G.degree()
max_degree = int(max(degree_dic.iteritems(), key=operator.itemgetter(1))[1])

def BC(G, i):
    SUM = 0
    for neighbor in G.neighbors(i):
        SUM += (1./G.degree(neighbor))
        #print neighbor, G.degree(neighbor), '- new sum:', SUM
    return 1 / (G.degree(i) * SUM)

def bridging(G, i):
    return betweenness_dic[i] * BC(G, i)

f_out = open('nodes_attributes.txt', 'w')
#lines = open('nodes_attributes.txt').read().split('\n')

f_out.write('node\tgeneID\tdegree\tbridging_centrality\tclustering\tbetweenness\tnorm_degree\tbrokering\tis_seed\n')
#for line in lines[1:]:
#    if line != '':
i = 0
number_of_nodes = G.number_of_nodes()
for node in G.nodes():
    i += 1
    print i, 'out of', number_of_nodes
    #node = line.split('\t')[0]
    geneID = convert(node, get='ID', gene_info=gene_info_file)
    norm_degree  = degree_dic[node]/float(max_degree)
    broker_index = (1 - clustering_dic[node]) * norm_degree
    if node in seeds:
        is_seed = 'Yes'
    else:
        is_seed = 'No'
    f_out.write('%s\t%s\t%d\t%.5f\t%.5f\t%.5f\t%.5f\t%.5f\t%s\n' % (node, geneID, degree_dic[node], bridging(G, node), clustering_dic[node], betweenness_dic[node], norm_degree, broker_index, is_seed))
    '''
    print 'node', node
    print 'degree', degree_dic[node]
    print 'norm_degree', norm_degree
    print 'bridging', bridging(G, node)
    print 'betweenness', betweenness_dic[node]
    print 'brokering', broker_index
    print
    '''

f_out.close()
