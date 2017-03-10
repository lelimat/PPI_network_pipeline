# net_cytoscape.py
# C: Jun 22, 2012
# M: Mar 10, 2017
# A: Leandro Lima <leandro.lima@gladstone.ucsf.edu>

import sys
import networkx as nx

# Run it after running "get_network_info.R"

def strType(var):
    try:
        if int(var) == float(var):
            return 'int'
    except:
        try:
            float(var)
            return 'float'
        except:
            return 'str'


def write_node(node, FILE, attributes):
    '''
    Function to write the attributes of a node in a FILE
    '''
    FILE.write('    <node label="%s" id="%s">\n' % (node, node))
    for attribute in attributes:
        try:
            exec('dic = dic_' + attribute)
            att_type = strType(str(dic[node]))
            if att_type == 'str' or attribute == 'geneID':
                FILE.write('        <att type="string" name="%s" value="%s"/>\n' % (attribute, dic[node]))
            elif att_type == 'float':
                FILE.write('        <att type="real" name="%s" value="%f"/>\n' % (attribute, dic[node]))
            elif att_type == 'int':
                FILE.write('        <att type="integer" name="%s" value="%d"/>\n' % (attribute, dic[node]))
            # Modifying special nodes attributes
            if attribute == 'node_type':
                # BROKERS
                if dic[node] == 'broker':
                    FILE.write('        <att type="string" name="node.fillColor" value="255,204,204"/>\n')
                    FILE.write('        <att type="string" name="node.size" value="70"/>\n')
                    FILE.write('        <att type="string" name="node.shape" value="ellipse"/>\n')
                    FILE.write('        <graphics type="ELLIPSE" fill="#ffcccc" h="70.0" w="70.0"/>\n')
                # BRIDGES
                elif dic[node] == 'bridge':
                    FILE.write('        <att type="string" name="node.fillColor" value="102,204,255"/>\n')
                    FILE.write('        <att type="string" name="node.size" value="60"/>\n')
                    FILE.write('        <att type="string" name="node.shape" value="diamond"/>\n')
                    FILE.write('        <graphics type="DIAMOND" fill="#66ccff" h="60.0" w="60.0"/>\n')
                # OTHERS
                else:
                    FILE.write('        <att type="string" name="node.fillColor" value="#dddddd"/>\n')
                    FILE.write('        <att type="string" name="node.shape" value="ellipse"/>\n')
                    FILE.write('        <graphics type="ELLIPSE" fill="#dddddd"/>\n')
        except:
            pass
    FILE.write('    </node>\n')

def write_edge(edge, FILE, attributes):
    '''
    Function to write the attributes of a edge in a FILE
    '''
    FILE.write('    <edge label="%s" source="%s" target="%s">\n' % (':'.join(edge), edge[0], edge[1]))
    FILE.write('        <att type="string" name="edge.color" value="153,153,153"/>\n')
    FILE.write('        <graphics width="3" fill="#999999"/>\n')
    FILE.write('    </edge>\n')


filename = 'nodes_attributes.txt' #sys.argv[1]

lines = open(filename).read().split('\n')
while lines[-1] == '':
    lines.pop()

attributes = lines[0].split('\t')
attributes.append('node_type')
for attribute in attributes:
    exec('global dic_' + attribute)
    exec('dic_' + attribute + ' = {}')

for line in lines[1:]:
    atts = line.split('\t')
    node_id = atts[0]
    for i in range(len(atts)):
        att_type = strType(atts[i])
        if att_type == 'str':
            exec('dic_' + attributes[i] + '[node_id] = "' + atts[i] + '"')
        else:
            exec('dic_' + attributes[i] + '[node_id] = ' + atts[i])


def main():

    G = nx.read_edgelist('edges_attributes.txt', delimiter='\t')
    G.remove_node('node_1')
    G.remove_node('node_2')

    brokers = []
    for pair in open('brokers.txt').read().split('\n')[1:]:
        if pair != '':
            node = pair.split('\t')[0]
            brokers.append(node)

    bridges = []
    for pair in open('bridges.txt').read().split('\n')[1:]:
        if pair != '':
            node = pair.split('\t')[0]
            bridges.append(node)

    for node in G.nodes():
        if node in brokers:
            if node in bridges:
                dic_node_type[node] = 'broker_bridge'
            else:
                dic_node_type[node] = 'broker'
        elif node in bridges:
            dic_node_type[node] = 'bridge'
        else:
            dic_node_type[node] = 'common'

    FILE = open('network.xgmml', 'w')
    FILE.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    FILE.write('<graph label="InteractomeView network" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:cy="http://www.cytoscape.org" xmlns="http://www.cs.rpi.edu/XGMML" directed="1"  Layout="points">\n')
    FILE.write('    <att name="documentVersion" value="1.1"/>\n')
    FILE.write('    <att type="string" name="backgroundColor" value="#ffffff"/>\n')

    for node in G.nodes():
        write_node(node, FILE, attributes)

    for edge in G.edges():
        write_edge(edge, FILE, None)

    FILE.write('</graph>\n')
    FILE.close()


if __name__ == '__main__':
    main()
