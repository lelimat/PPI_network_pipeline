# symbol_geneid.py - script to convert gene symbol to gene Id and vice versa
# C: Jul 28, 2011
# M: Mar 10, 2017
# A: Leandro Lima <leandro.lima@gladstone.ucsf.edu>


import sys#, cPickle

def convert(x, get, gene_info):
    '''
    Converts 'x'. What do you want to get? Symbol or Entrez Gene ID?
    Running only for 'Homo sapiens'
    '''
    gene_Id        = {}
    gene_Symbol    = {}
    gene_Name      = {}
    gene_EnsemblID = {}
    
    # File above obtained from 'ftp://ftp.ncbi.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz'
    geneIdf = file(gene_info)
    i = 0
    geneIdl = geneIdf.readlines()
    for gidl in geneIdl:
        if gidl.startswith('9606'): # if species is exactly 'Homo sapiens'
            #txid       = gidl.split('\t')[0]
            geneId     = gidl.split('\t')[1]
            geneSymbol = gidl.split('\t')[2]
            other_dbs  = gidl.split('\t')[5].split('|')
            for db in other_dbs:
                if db.startswith('Ensembl:'):
                    EnsemblID = db.split(':')[1]
            geneName   = gidl.split('\t')[8]
            #print txid,'|',geneId,'|',geneSymbol,'|',geneName
            gene_Id[geneId] = geneSymbol
            gene_Symbol[geneSymbol] = geneId
            gene_Symbol[geneSymbol.upper()] = geneId
            gene_Name[geneId] = geneName
            gene_Name[geneSymbol] = geneName
            gene_Name[geneSymbol.upper()] = geneName
            gene_EnsemblID[geneSymbol] = EnsemblID
            gene_EnsemblID[geneSymbol.upper()] = EnsemblID
            #while int(go_line[i].split('\t'))
    if get.lower().startswith('s'): # get the symbol
        dic = gene_Id
    elif get.lower().startswith('n'): # get the name
        dic = gene_Name
    elif get.lower().startswith('ens'): # get the Ensembl ID
        dic = gene_EnsemblID
    elif get.lower().startswith('e') or get.lower().startswith('i'): # get the Entrez ID
        dic = gene_Symbol
    
    #print 'type is', type(x).__name__, 'and x is', x
    if type(x).__name__ == 'list':
        result_list = []
        for i in x:
            try:
                result_list.append(dic[str(i)])
            except:
                result_list.append('Not found')
        return result_list
    elif type(x).__name__ == 'str':
        try:
            return dic[x]
        except:
            return 'Not found'


def main():
    if len(sys.argv) < 5:
        print '\n\n    Run: python ~/programming/python/symbol_geneid.py [Name|Symbol|Id|File] [\'Symbol\'|\'Id\'|\'Name\'|\'Ensembl\'] [to_file=False] [sort=False]'
        print '    Please try again. =)\n\n'
        sys.exit(0)
    gene  = sys.argv[1]
    get   = sys.argv[2]
    #parameters = ['program', 'symbol/id', 'what you want', 'to file?', 'sort?']

    # Write to file?
    try:
        to_file = sys.argv[3]
        if to_file.lower().startswith('t'):
            to_file = True
        else:
            to_file = False
    except:
        to_file = False
    
    sort = sys.argv[4]
    if sort.lower() in ['true', 'yes', '1']:
        sort = True
    else:
        sort = False
    
    try:
        if to_file:
            nameOutFile = '.'.join(gene.split('.')[:-1]) + '_' + get + '.' + gene.split('.')[-1]
            outFile = open(nameOutFile, 'w')
        lines = open(gene).read().replace('\r\n','\n').split('\n')
        list_to_convert = []
        for line in lines:
            if line != '':
                print line.split('\t')[0]
                list_to_convert.append(line.split('\t')[0])
        #print 'list_to_convert:', list_to_convert
        list_converted = convert(list_to_convert, get, gene_info)
        #print 'list_converted:', list_converted
        if to_file:
            if order:
                print 'ok'
                list_converted.sort()
                for i in range(len(list_converted)):
                    element = list_converted[i]
                    if not element == 'Not found' and list_converted.index(element) == i:
                        outFile.write(element + '\n')
            else:
                for element in list_converted:
                    outFile.write(element + '\n')
    except:
        try:
            print convert(gene, get, gene_info)
        except:
            pass


if __name__ == '__main__':
    main()
