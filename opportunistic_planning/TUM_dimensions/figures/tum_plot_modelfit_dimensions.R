library(RColorBrewer)

# Define data (x: videos, y: fit of model, edit distance with Damerau-Levenshtein)
xdata <- c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19)
x <- c(0.2,0.2,0,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0,0.2,0.21,0.21,0.2,0.2,0.4,0.4)
y <- c(0.48,0.48,0,0.48,0.48,0.48,0.48,0.48,0.48,0.48,0.48,0,0.48,0.58,0.58,0.48,0.48,0.26,0.26)
z <- c(0.47,0.47,0.33,0.47,0.47,0.47,0.47,0.47,0.47,0.47,0.47,0.33,0.47,0.53,0.53,0.47,0.47,0.27,0.27)
xy <- c(0.3,0.3,0,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0,0.3,0.1,0.1,0.3,0.3,0.1,0.1)
xz <- c(0.31,0.31,0,0.31,0.31,0.31,0.31,0.31,0.31,0.31,0.31,0,0.31,0.5,0.5,0.31,0.31,0.1,0.1)
yz <- c(0.47,0.47,0,0.47,0.47,0.47,0.47,0.47,0.47,0.47,0.47,0,0.47,0.53,0.53,0.47,0.47,0.28,0.28)
xyz <- c(0.1,0.1,0,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0,0.1,0.5,0.5,0.1,0.1,0.1,0.1)
avg <- c(0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666)
  
col = brewer.pal(n=7,name='Set1')


#par(oma=c(1,1,1,1))
#par(mar=c(4,5,3,0))

# Plot x
plot(xdata, x, type='o', col=col[1], pch=15, lty=1, ylim=c(0,1.0), lwd=2, 
     ylab='Normalized Damerau-Levenshtein distance', main="TUM data, dimensions",
     xlab='Video sequence', las=1, xaxt='n', cex.lab=1.4, cex.main=1.4)
axis(side=1, at=1:19, labels=xdata, cex.axis=1)


# Plot y
points(xdata, y, col=col[2], pch=16)
lines(xdata, y, col=col[2], lty=1, lwd=2)

# Plot z
points(xdata, z, col=col[3], pch=17)
lines(xdata, z, col=col[3], lty=1, lwd=2)

# Plot xy
points(xdata, xy, col=col[4], pch=18)
lines(xdata, xy, col=col[4], lty=1, lwd=2)

# Plot xz
points(xdata, xz, col=col[5], pch=19)
lines(xdata, xz, col=col[5], lty=1, lwd=2)

# Plot yz
points(xdata, yz, col=col[6], pch=20)
lines(xdata, yz, col=col[6], lty=2, lwd=2)

# Plot xyz
points(xdata, xyz, col=col[7], pch=21)
lines(xdata, xyz, col=col[7], lty=1, lwd=2)

# Plot avg/baseline
points(xdata, avg, col='black', pch=19)
lines(xdata, avg, col='black', lty=3, lwd=2)


# Plot legend in 3 columns
legend_order <- matrix(1:9, ncol=3, byrow=TRUE)

legend(9.6,1.03, c('x','y','z','xy','xz','yz','xyz','mean edit distance')[legend_order], 
       col=c(col[1],col[2],col[3],col[4],col[5],col[6],col[7],'black')[legend_order], 
       pch=c(15,16,17,18,19,20,21,19)[legend_order], lty=c(1,1,1,1,1,1,1,3)[legend_order], ncol=3, cex=1.2,
       text.width=1.7)
