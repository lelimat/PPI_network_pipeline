# get_PPI_data_iRefIndex.R
# C: Apr 30, 2014
# M: Mar 10, 2017
# A: Leandro Lima <leandro.lima@gladstone.ucsf.edu> / <lelimaufc@gmail.com>

# install.packages('iRefR')

# Usage: R --slave --file=get_PPI_data_iRefIndex.R --args [min_evidence] [database_dir]

min_evidence <- commandArgs(TRUE)[1]
database_dir <- commandArgs(TRUE)[2]
if (!substr(database_dir, 1, 1) == '/') {
	database_dir <- paste('.', database_dir, sep='/')
}


# Installing libraries from bioconductor
source("http://bioconductor.org/biocLite.R")
for (package in c('graph', 'RBGL')){
	if(!require(package, character.only = TRUE)){
		cat('Installing package', package, 'from bioconductor.\n')
		biocLite(package)
	}
	cat('Loading package', package, 'from bioconductor.\n')
	require(package, character.only = TRUE)
}

# Installing libraries from CRAN
for (package in c('devtools', 'stringr')){
	if(!require(package, character.only = TRUE)){
		cat('Installing package', package, 'from CRAN.\n')
		install.packages(package)
	}
	cat('Loading package', package, 'from CRAN.\n')
	require(package, character.only = TRUE)
}
 # Installing iRefR from developer's GitHub
install_github("antonio-mora/iRefR")
library("iRefR")

# to see last version: http://irefindex.org/download/irefindex/data/archive/
if(!dir.exists(database_dir)) {
	dir.create(database_dir)
}

iref = get_irefindex(tax_id="9606", iref_version="current", data_folder=database_dir)

human_human_list = data.frame(iref$taxa,iref$taxb)
tmp = do.call(`paste`, c(unname(human_human_list), list(sep=".")))
iref_human = iref[tmp == "taxid:9606(Homo sapiens).taxid:9606(Homo sapiens)" | tmp == "-.taxid:9606(Homo sapiens)",]

mA = str_locate(iref_human$aliasA, perl("hgnc:.*?\\|"))
hugoA = str_sub(iref_human$aliasA,mA[,1]+5,mA[,2]-1)
mB = str_locate(iref_human$aliasB, perl("hgnc:.*?\\|"))
hugoB = str_sub(iref_human$aliasB,mB[,1]+5,mB[,2]-1)

x = data.frame(iref_human$X.uidA, iref_human$uidB, hugoA, hugoB, iref_human$irigid)
colnames(x) = c("uidA","uidB","hugoA","hugoB","irigid")
x = data.frame(x, 1)

net_counts = aggregate(x$X1, list('hugoA'=x$hugoA, 'hugoB'=x$hugoB), FUN=sum)

write.table(net_counts[which(net_counts$x >= min_evidence), 1:2], 'iRefIndex_human.txt', sep='\t', row.names=FALSE, quote=FALSE)


