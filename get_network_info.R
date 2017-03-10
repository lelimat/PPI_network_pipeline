# get_network_info.R
# C: Dec 19, 2011
# M: Mar 10, 2017
# A: Leandro Lima <leandrolima>

# Usage: R --slave --file=/home/users/llima/programming/R/get_network_info.R --args [nodes_attributes_files]

file_name <- commandArgs(TRUE)[1]
cat ("Opening file:", file_name, "\n")
nodes_file <- read.delim(file_name, stringsAsFactors=FALSE)
class <- 'common'
nodes_file <- data.frame(nodes_file, class, stringsAsFactors=FALSE)

# Threshold of quantile for best genes in each category.
# If threshold = 0.95, then the best 5% will be shown.
threshold <- 0.95


#############################################################################################
#############################################################################################
### Degree distribution
#############################################################################################
#############################################################################################

pdf('degree_distribution.pdf')
plot(nodes_file$degree[order(nodes_file$degree)], pch=16,
     main=paste('Degree distribution', sep=''),
     xlab='Nodes', ylab='Degrees', col=c('gray23', 'cornflowerblue')[as.factor(nodes_file$is_seed)])
legend('topleft', c('seeds','other genes'), col=c('cornflowerblue','gray23'), pch=16)
dev.off()


#############################################################################################
#############################################################################################
### Betweenness centrality 
#############################################################################################
#############################################################################################

bottleneck_th <- threshold # 'Betweenness centrality threshold' - getting the nodes with betweenness above the threshold
bottleneck_cut <- quantile(nodes_file$betweenness, probs=bottleneck_th)
bottleneck_names <- nodes_file[nodes_file$betweenness >= bottleneck_cut, c('node')]
for (i in 1:nrow(nodes_file)) {
    if (nodes_file$node[i] %in% bottleneck_names) {
        nodes_file$class[i] <- 'bottleneck'
    }
}

pdf('betweenness_distribution.pdf')
plot(nodes_file$betweenness[order(nodes_file$betweenness)], pch=16,
     main=paste('The best ',100*round(1-bottleneck_th, 2),'% bottleneck genes (betweenness above ',round(bottleneck_cut, 5),')', sep=''),
     xlab='Nodes', ylab='Nodes betweenness centrality', col=c('gray23', 'cornflowerblue')[as.factor(nodes_file$is_seed)])
legend('topleft', c('seeds','other genes'), col=c('cornflowerblue','gray23'), pch=16)
abline(h=bottleneck_cut,col='red')

n_names_to_plot <- 3 # Define it by hand

# Plotting bottlenecks names
if (n_names_to_plot > 0) {
    cols <- colnames(nodes_file) %in% c('node','betweenness')
    bottlenecks <- nodes_file[order(nodes_file$betweenness, decreasing = TRUE), cols]
    bottlenecks <- bottlenecks[1:n_names_to_plot,]
    x <- (nrow(nodes_file)-n_names_to_plot+1):nrow(nodes_file)
    y <- bottlenecks$betweenness
    text(x, y, bottlenecks$node, cex = 1, adj = c(1.2, 1.2))
}

dev.off()


# Writing bridges to a file
write.table(bottleneck_names, 'bottlenecks.txt', sep='\t', quote=FALSE, row.names=FALSE, col.names=FALSE)


#############################################################################################
#############################################################################################
### Bridgeness distribution
#############################################################################################
#############################################################################################

bridge_th <- threshold # 'Bridgeness threshold' - getting the nodes with bridgeness above the threshold
bridge_cut <- quantile(nodes_file$bridging_centrality, probs=bridge_th)
bridge_names <- nodes_file[nodes_file$bridging_centrality >= bridge_cut, c('node')]
for (i in 1:nrow(nodes_file)) {
    if (nodes_file$node[i] %in% bridge_names) {
        if (nodes_file$class[i] == 'common') {
            nodes_file$class[i] <- 'bridge'
        } else {
            nodes_file$class[i] <- paste(nodes_file$class[i], 'bridge', sep='_')
        }
    }
}

pdf('bridging_distribution.pdf')
plot(nodes_file$bridging_centrality[order(nodes_file$bridging_centrality)], pch=16,
     main=paste('The best ',100*round(1-bridge_th, 2),'% bridge genes (bridging centrality above ',round(bridge_cut, 5),')', sep=''),
     xlab='Nodes', ylab='Nodes bridging centrality', col=c('gray23', 'cornflowerblue')[as.factor(nodes_file$is_seed)])
legend('topleft', c('seeds','other genes'), col=c('cornflowerblue','gray23'), pch=16)
abline(h=bridge_cut,col='red')

# Writing bridges to a file
write.table(bridge_names, 'bridges.txt', sep='\t', quote=FALSE, row.names=FALSE, col.names=FALSE)

n_names_to_plot <- 3 # Define it by hand

# Plotting bridges names
if (n_names_to_plot > 0) {
    cols <- colnames(nodes_file) %in% c('node','bridging_centrality')
    bridges <- nodes_file[order(nodes_file$bridging_centrality, decreasing = TRUE), cols]
    bridges <- bridges[1:n_names_to_plot,]
    x <- (nrow(nodes_file)-n_names_to_plot+1):nrow(nodes_file)
    y <- bridges$bridging_centrality
    text(x, y, bridges$node, cex = 1, adj = c(1.2, 1.2))
}

dev.off()

#############################################################################################
#############################################################################################
### Brokering
#############################################################################################
#############################################################################################
broker_th <- threshold # 'Bridgeness threshold' - getting the nodes with bridgeness above the threshold
broker_cut <- quantile(nodes_file$brokering, probs=broker_th)
broker_names <- nodes_file[nodes_file$brokering >= broker_cut, c('node')]
for (i in 1:nrow(nodes_file)) {
    if (nodes_file$node[i] %in% broker_names) {
        if (nodes_file$class[i] == 'common') {
            nodes_file$class[i] <- 'broker'
        } else {
            nodes_file$class[i] <- paste(nodes_file$class[i], 'broker', sep='_')
        }
    }
}
pdf('brokering_distribution.pdf')
plot(nodes_file$brokering[order(nodes_file$brokering)], pch=16,
     main=paste('The best ',100*round(1-broker_th, 2),'% broker genes (brokering above ',round(broker_cut, 5),')', sep=''),
     xlab='Nodes', ylab='Nodes brokering', col=c('gray23', 'cornflowerblue')[as.factor(nodes_file$is_seed)])
legend('topleft', c('seeds','other genes'), col=c('cornflowerblue','gray23'), pch=16)
abline(h=broker_cut,col='red')

# Writing brokers to a file
write.table(broker_names, 'brokers.txt', sep='\t', quote=FALSE, row.names=FALSE, col.names=FALSE)

n_names_to_plot <- 3 # Define it by hand

# Plotting broker names
if (n_names_to_plot > 0) {
    cols <- colnames(nodes_file) %in% c('brokering','node')
    brokers <- nodes_file[order(nodes_file$brokering, decreasing = TRUE), cols]
    brokers <- brokers[1:n_names_to_plot,]
    x <- (nrow(nodes_file)-n_names_to_plot+1):nrow(nodes_file)
    y <- brokers$brokering
    text(x, y, brokers$node, cex = 1, adj = c(1.2, 1.2))
}

dev.off()

