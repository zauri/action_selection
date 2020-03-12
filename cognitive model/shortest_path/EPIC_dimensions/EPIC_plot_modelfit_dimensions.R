library(RColorBrewer)

# Define data (x: videos, y: fit of model, edit distance with Damerau-Levenshtein)
xdata <- c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19)
x <- c(0.1952,0.1952,0,0.1952,0.1952,0.1952,0.1952,0.1952,0.1952,0.1952,0.1952,0,0.1952,0.2072,0.2072,0.1952,0.1952,0.4008,0.4008)
y <- c(0.4778,0.4778,0,0.4778,0.4778,0.4778,0.4778,0.4778,0.4778,0.4778,0.4778,0,0.4778,
       0.5754,0.5754,0.4778,0.4778,0.2634,0.2634)
z <- c(0.4672,0.4672,0.33,0.4672,0.4672,0.4672,0.4672,0.4672,0.4672,0.4672,0.4672,0.33,0.4672,
       0.5278,0.5278,0.4672,0.4672,0.2672,0.2672)
xy <- c(0.3,0.3,0,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0,0.3,0.1024,0.1024,0.3,0.3,0.4971,0.4974)
xz <- c(0.306,0.306,0,0.306,0.306,0.306,0.306,0.306,0.306,0.306,0.306,0,0.306,0.5022,0.5022,0.306,0.306,0.0996,0.0996)
yz <- c(0.4728,0.4728,0,0.4728,0.4728,0.4728,0.4728,0.4728,0.4728,0.4728,0.4728,0,0.4728,0.5332,0.5332,0.4728,0.4728,
        0.2752,0.2752)
xyz <- c(0.1002,0.1002,0,0.1002,0.1002,0.1002,0.1002,0.1002,0.1002,0.1002,0.1002,0,0.1002,0.496,0.496,0.1002,0.1002,
         0.1018,0.1018)
avg <- c(0.44,0.666,0.605,0.605,0.44,0.44,0.666,0.723,0.605,0.756,0.723,0.806,0.666,0.25,0.666,0.666)
  
col = brewer.pal(n=7,name='Set1')

# Plot x
plot(xdata, x, type='o', col=col[1], pch=15, lty=1, ylim=c(0,0.7), lwd=2, 
     ylab='Normalized Damerau-Levenshtein distance', main="EPIC data, dimensions",
     xlab='Video sequence', las=1, xaxt='n', cex.lab=1.4)
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

legend(1,0.72, c('x','y','z','xy','xz','yz','xyz','mean edit distance')[legend_order], 
       col=c(col[1],col[2],col[3],col[4],col[5],col[6],col[7],'black')[legend_order], 
       pch=c(15,16,17,18,19,20,21,19)[legend_order], lty=c(1,1,1,1,1,1,1,3)[legend_order], ncol=3, cex=1.2)
