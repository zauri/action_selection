library(RColorBrewer)

# Define data (x: videos, y: fit of model, edit distance with Damerau-Levenshtein)
xdata <- c(1,2,3,4)
x <- c(0.2,0,0.21,0.4)
y <- c(0.48,0,0.58,0.26)
z <- c(0.47,0.33,0.53,0.27)
xy <- c(0.3,0,0.1,0.1)
xz <- c(0.31,0,0.5,0.1)
yz <- c(0.47,0,0.53,0.28)
xyz <- c(0.1,0,0.5,0.1)
avg <- c(0.666,0.44,0.666,0.666)
  
col = brewer.pal(n=7,name='Set1')

# Plot x
plot(xdata, x, type='o', col=col[1], pch=15, lty=1, ylim=c(0,0.9), lwd=2, 
     ylab='Normalized Damerau-Levenshtein distance', main="TUM data, dimensions",
     xlab='Video sequence', las=1, xaxt='n', cex.lab=1.4)
axis(side=1, at=1:4, labels=c('tnpsc','tn,pc,s','tnpcs','tnspc'), cex.axis=1)

# Plot y
points(xdata, y, col=col[2], pch=16)
lines(xdata, y, col=col[2], lty=2, lwd=2)

# Plot z
points(xdata, z, col=col[3], pch=17)
lines(xdata, z, col=col[3], lty=1, lwd=2)

# Plot xy
points(xdata, xy, col=col[4], pch=18)
lines(xdata, xy, col=col[4], lty=2, lwd=2)

# Plot xz
points(xdata, xz, col=col[5], pch=17)
lines(xdata, xz, col=col[5], lty=1, lwd=2)

# Plot yz
points(xdata, yz, col=col[6], pch=20)
lines(xdata, yz, col=col[6], lty=1, lwd=2)

# Plot xyz
points(xdata, xyz, col=col[7], pch=15)
lines(xdata, xyz, col=col[7], lty=2, lwd=2)

# Plot avg/baseline
points(xdata, avg, col='black', pch=19)
lines(xdata, avg, col='black', lty=3, lwd=2)


# Plot legend in 3 columns
legend_order <- matrix(1:9, ncol=3, byrow=TRUE)

legend(1,0.93, c('x','y','z','xy','xz','yz','xyz','mean edit distance')[legend_order], 
       col=c(col[1],col[2],col[3],col[4],col[5],col[6],col[7],'black')[legend_order], 
       pch=c(15,16,17,18,17,20,15,19)[legend_order], lty=c(1,2,1,1,1,1,2,3)[legend_order], ncol=3, cex=1.2)
