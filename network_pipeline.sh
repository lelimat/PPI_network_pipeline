# network_pipeline.sh
# C: Apr  1, 2012
# M: Mar 10, 2017
# A: Leandro Lima <leandro.lima@gladstone.ucsf.edu> / <lelimaufc@gmail.com>


R --slave --file=get_PPI_data_iRefIndex.R 2 databases
wget ftp://ftp.ncbi.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz
gunzip Homo_sapiens.gene_info.gz

d=1
python create_net_irefindex.py --database=iRefIndex_human.txt --seeds=seeds.txt --output=. --distance=$d #--subset=$HOME/Dropbox/doutorado/tdah/2014/genes_expressed_in_brain_UNION.txt
# python ~/Dropbox/programming/python/create_net_irefindex.py --database=/Users/limal/databases/iRef_human_counts_atleast2.txt --seeds=seeds.txt --output=. --distance=$d --subset=$HOME/Dropbox/doutorado/tdah/2014/genes_expressed_in_brain_UNION.txt
# Analyzing network created from iRefIndex
echo -e "node_1\tnode_2" > edges_attributes.txt
cat edges.txt >> edges_attributes.txt
python network_topology.py edges_attributes.txt Homo_sapiens.gene_info
rm edges.txt

# Getting bridges, brokers and bottlenecks
R --slave --file=get_network_info.R --args nodes_attributes.txt

# cat nodes_attributes_details.tsv | perl -pe 's/ //g; s/\t/,/g' > nodes_attributes_details.csv

# Getting nodes in the initial list
grep Yes nodes_attributes.txt | cut -f1 > in_list_Yes.txt

# Separating the gene symbols in the network
cut -f1 nodes_attributes.txt | grep -v node > all_genes.txt

# Creating Cytoscape file
python net_cytoscape.py

# DADA preparation
cut -f1 edges_attributes.txt | tail -n +2 > node_1.txt
cut -f2 edges_attributes.txt | tail -n +2 > node_2.txt
python $HOME/Dropbox/programming/python/symbol_geneid.py node_1.txt Id True Homo
python $HOME/Dropbox/programming/python/symbol_geneid.py node_2.txt Id True Homo
# length=`wc -l edges_attributes.txt | cut -f1 -d' '`
# length=`expr $length - 1`
# tail -n $length node_1_Id.txt > tmp.txt; mv tmp.txt node_1_Id.txt
# tail -n $length node_2_Id.txt > tmp.txt; mv tmp.txt node_2_Id.txt
paste node_1_Id.txt node_2_Id.txt > net_DADA.txt
echo -e "gene_name 1\tgene_name 2\tassociation_score" > tmp.txt
awk '{print $1"\t"$2"\t1"}' net_DADA.txt | grep -v 'Not found' >> tmp.txt
mv tmp.txt net_DADA.txt


# Getting from DADA
cut -f1 net.tsv | grep -v gene_name > nodes1.txt
cut -f2 net.tsv | grep -v gene_name > nodes2.txt
python ~/Dropbox/programming/python/symbol_geneid.py nodes1.txt symbol True Homo
python ~/Dropbox/programming/python/symbol_geneid.py nodes2.txt symbol True Homo
cat nodes1.txt nodes2.txt
paste nodes1_symbol.txt nodes2_symbol.txt > tmp.txt
echo -e "node_1\tnode_2" > titles.txt; cat titles.txt tmp.txt > edges_attributes.txt
python ~/Dropbox/programming/python/symbol_geneid.py seeds.txt symbol True Homo
python ~/Dropbox/programming/python/symbol_geneid.py candidates.txt symbol True Homo
python ~/Dropbox/programming/python/net_from_DADA.py seeds_symbol.txt
R --slave --file=$HOME/Dropbox/programming/R/get_network_info.R
python ~/programming/python/net_cytoscape.py

