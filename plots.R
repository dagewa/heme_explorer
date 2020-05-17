#!/usr/bin/env Rscript --vanilla
args = commandArgs(trailingOnly=TRUE)
if (length(args)!=1) {
  stop("Must provide a filename of three column data", call.=FALSE)
}
d<-read.table(args[1],header=T)
num_datasets<-nrow(d)
km<-kmeans(data.frame(d$CBC.CMC, d$CBB.CMB), 4, nstart=100)

pdf("heme_classes1.pdf")
smoothScatter(d$CBC.CMC, d$CBB.CMB, xlab="||CBC - CMC|| (Å)", ylab="||CBB - CMB|| (Å)")
points(d$CBC.CMC, d$CBB.CMB, pch=".")
title(paste("Vinyl-methyl distances for", num_datasets, "heme structures"))
dev.off()

pdf("heme_classes2.pdf")
smoothScatter(d$CBC.CMC, d$CBB.CMB, xlab="||CBC - CMC|| (Å)", ylab="||CBB - CMB|| (Å)")
points(d$CBC.CMC, d$CBB.CMB, pch=".", col=km$cluster)
title(paste("Vinyl-methyl distances for", num_datasets, "heme structures"))
dev.off()

pdf("heme_classes3.pdf")
smoothScatter(d$CBC.CMC, d$CBB.CMB, xlab="||CBC - CMC|| (Å)", ylab="||CBB - CMB|| (Å)")
points(d$CBC.CMC, d$CBB.CMB, pch=".", col=km$cluster)
points(km$centers, pch=16)
title(paste("Vinyl-methyl distances for", num_datasets, "heme structures"))
dev.off()

tooltips <- paste(d$Filename,"<br />x: ", d$CBC.CMC, "<br />y: ", d$CBB.CMB)
urls <- paste("uglymol.html?id=",d$Filename)
library(scatterD3)
scatterD3(d$CBC.CMC, d$CBB.CMB,
    xlab="||CBC - CMC|| (Å)",
    ylab="||CBB - CMB|| (Å)",
    point_opacity = 0.3,
    tooltip_text=tooltips,
    url_var=urls)
