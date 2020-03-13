library(RColorBrewer)

# Define data (x: videos, y: fit of model, edit distance with Damerau-Levenshtein)
xdata <- c(1,2,3,4,5,6,7,8,9,10,11,12)
regions <- c(0,0,0,0.25,0,0,0.67,0.25,0,0,0,0)
avg <- c(0.44,0.44,0.44,0.605,0.44,0.44,0.44,0.605,0.44,0.44,0.44,0.44)
  
col = brewer.pal(n=7,name='Set1')

# Plot regions
plot(xdata, regions, type='o', col=col[1], pch=15, lty=1, ylim=c(0,0.8), lwd=2, 
     ylab='Normalized Damerau-Levenshtein distance', main="VR data, regions",
     xlab='Unique sequence (continuously numbered)', las=1, xaxt='n', cex.lab=1.4)
axis(side=1, at=1:12, labels=xdata, cex.axis=1)

# Plot avg/baseline
points(xdata, avg, col='black', pch=19)
lines(xdata, avg, col='black', lty=2, lwd=2)

# Plot legend 
legend_order <- matrix(1:2, ncol=2, byrow=TRUE)

legend(1,0.82, c('no parameters set','mean edit distance')[legend_order], 
       col=c(col[1],'black')[legend_order], 
       pch=c(15,19)[legend_order], lty=c(1,2)[legend_order], ncol=2, cex=1.2)