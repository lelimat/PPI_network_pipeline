# create_net_irefindex.py - program to read the human interactome from iRefIndex and put in a graph
# C: May  2, 2014
# M: Mar 10, 2017
# A: Leandro Lima <llima@ime.usp.br>

#from math import *
import os, sys, getopt
# import matplotlib.pyplot as plt
# from os import getenv
# HOME = getenv('HOME')

# Use this when you don't have networkx installed
#decorator_path = '../decorator-4.0.10/src'
#networkx_path  = '../networkx-1.11'
#sys.path.append(decorator_path)
#sys.path.append(networkx_path)

import networkx as nx


def create_interactome(database_path, seeds=[], distance=1, subset=[]):
    '''
    'List' contains a list with 'gene symbols' (must be as they are in the interactome).
    If restricted==True, an edge will be added only if both nodes are in the list.
    If restricted==False, an edge will be added if one of the nodes is in the list.
    '''

    # Reading interactome file
    lines = open(database_path).read().split('\n')
    while lines[-1] == '':
        lines.pop()

    whole_interactome = nx.Graph()
    if subset == []:
        for l in lines[1:]:
            g1, g2 = l.split('\t')
            if g1 != g2:
                whole_interactome.add_edge(g1,g2)
    else:
        for l in lines[1:]:
            g1, g2 = l.split('\t')
            if g1 != g2 and g1 in subset and g2 in subset:
                whole_interactome.add_edge(g1,g2)

    print 'WHOLE INTERACTOME'
    print 'number_of_nodes:', whole_interactome.number_of_nodes() 
    print 'number_of_edges:', whole_interactome.number_of_edges() 
    print

    current_seeds = []
    # Creating interactome
    interactome = nx.Graph()
    not_found_file = open('genes_not_found.txt', 'w')
    for seed in seeds:
        if seed in whole_interactome.nodes():
            current_seeds.append(seed)
            interactome.add_node(seed)
        else:
            not_found_file.write(seed + '\n')
    not_found_file.close()


    for seed1 in current_seeds:
        for seed2 in current_seeds:
            if seed1 < seed2 and whole_interactome.has_edge(seed1, seed2):
                interactome.add_edge(seed1, seed2)


    for time in range(1,distance+1):
        current_layer = []
        for seed in current_seeds:
            for neighbor in whole_interactome.neighbors(seed):
                if not interactome.has_edge(seed, neighbor):
                    interactome.add_edge(seed, neighbor)
                    if not neighbor in current_layer:
                        current_layer.append(neighbor)
        for node1 in current_layer:
            for node2 in current_layer:
                if whole_interactome.has_edge(node1, node2) and not interactome.has_edge(node1, node2):
                    interactome.add_edge(node1, node2)
        current_seeds = current_layer
    
    return interactome

def main():

    # Last use: python ~/Dropbox/programming/python/create_net_irefindex.py \
    #                  --database=/Users/limal/databases/iRef_human_counts_atleast2.txt \
    #                  --seeds=/Users/limal/Dropbox/doutorado/tdah/poster_e_relatorio_fapesp/rede_meta2/13536323485/seeds.txt \
    #                  --output=. \
    #                  --distance=1 \
    #                  --subset=genes_expressed_in_children_brains.txt

    optlist, dbs = getopt.getopt(sys.argv[1:], 'b', ['seeds=', 'output=', 'shortest_paths=', 'distance=', 'subset=', 'database='])
    subset = []
    #print 'optlist', optlist
    #print 'dbs', dbs
    for o, a in optlist:
        #print '['+o+'] ['+a+']'
        if o == "--seeds":
            in_file_name = a
        elif o == '--database':
            database_path = a
            #print 'in_file_name:', in_file_name
        elif o == "--output":
            output = a
        elif o == "--shortest_paths":
            if a == '1':
                put_shortest_paths = True
            else:
                put_shortest_paths = False
        elif o == '--distance':
            distance = int(a)
        elif o == "--subset":
            subset = open(a).read().replace('\r', '').split('\n')
            while subset[-1] == '':
                subset.pop()
        '''
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unhandled option"
        '''

    # Getting seeds of interest
    seeds = file(in_file_name).read().replace('\r','').split('\n')
    while seeds[-1] == '':
        seeds.pop()

    interactome = create_interactome(database_path, seeds, distance, subset)
    print 'THIS NETWORK'
    print 'number_of_nodes:', interactome.number_of_nodes() 
    print 'number_of_edges:', interactome.number_of_edges() 
    print

    nx.write_edgelist(interactome, output + '/edges.txt', comments='#', delimiter='\t', data=False, encoding='utf-8')
    
    sys.exit(0)


if __name__ == "__main__":
    main()
