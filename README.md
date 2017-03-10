# PPI network pipeline

These commands will create a network based on a set of genes you should provide as "seeds.txt".

## Download PPI database (iRefIndex)

Usage: **R --slave --file=get\_PPI\_data\_iRefIndex.R [min\_evidence] [database\_dir]**.

* [min\_evidence] is the minimum number times the interaction is being reported. I usually choose 2.
* [database\_dir] is the directory where the iRefIndex file will be saved.

		R --slave --file=get_PPI_data_iRefIndex.R 2 databases

## Download gene information

	wget ftp://ftp.ncbi.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz
	gunzip Homo_sapiens.gene_info.gz
	
## Create network from seed genes (initial set of interest)

	python create_net_irefindex.py --database=iRefIndex_human.txt --seeds=seeds.txt --output=. --distance=1

The **distance** is the number of levels of neighbors added to the network starting from the seeds. If you only need to see how the seeds connect. Choose distance=0. For seeds + first neighbors, choose distance=1, and so on.

## Calculate network topology

	echo -e "node_1\tnode_2" > edges_attributes.txt
	cat edges.txt >> edges_attributes.txt
	python network_topology.py edges_attributes.txt Homo_sapiens.gene_info
	rm edges.txt

## Create plots for brokers, bridges and bottlenecks
	R --slave --file=get_network_info.R --args nodes_attributes.txt

## Getting nodes in the initial list
	grep Yes nodes_attributes.txt | cut -f1 > in_list_Yes.txt

## Separating the gene symbols in the network
	cut -f1 nodes_attributes.txt | grep -v node > all_genes.txt

## Creating Cytoscape file
	python net_cytoscape.py

The command above will generate a file "network.xgmml" to be open with Cytoscape.