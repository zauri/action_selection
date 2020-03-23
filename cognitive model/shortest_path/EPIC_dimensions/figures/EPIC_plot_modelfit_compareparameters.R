library(RColorBrewer)

# Define data (x: videos, y: fit of model, edit distance with Damerau-Levenshtein)
xdata <- c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)
ck <- c(0.33,0.8,0.5,1,0,0.33,0.6,0.694,0.3705,0.727,0.594,0.813,0.8,0.262,0.496,0.8)
c <- c(0.498,0.8,0.5,1,0,0.33,0.6,0.729,0.372,0.734,0.727,0.815,0.8,0.2605,0.5032,0.8)
k <- c(0.667,0.8,0.5,1,0,0.33,0.6,0.696,0.372,0.735,0.598,0.768,0.8,0.261,0.5,0.8)
none <- c(0.667,0.8,0.627,1,0,0.501,0.6,0,745,0.381,0.743,0.728,0.769,0.8,0.274,0.502,0.8)
avg <- c(0.44,0.666,0.605,0.605,0.44,0.44,0.666,0.723,0.605,0.756,0.723,0.806,0.666,0.25,0.666,0.666)

twoD <- c(0.504,0.653,0.5,1,0,0.33,0.6,0.698,0.372,0.730,0.593,0.838,0.848,0.256,0.867,0.596)
  
col = brewer.pal(n=7,name='Set1')

# Plot ck
plot(xdata, ck, type='o', col=col[1], pch=15, lty=1, ylim=c(0,1.1), lwd=2, 
     ylab='Normalized Damerau-Levenshtein distance', main="EPIC data, dimensions",
     xlab='Video sequence', las=1, xaxt='n', cex.lab=1.4)
axis(side=1, at=1:16, labels=xdata, cex.axis=1)

# Plot c
#points(xdata, c, col=col[2], pch=16)
#lines(xdata, c, col=col[2], lty=2, lwd=2)

# Plot k
#points(xdata, k, col=col[3], pch=17)
#lines(xdata, k, col=col[3], lty=2, lwd=2)

# Plot no params
#points(xdata, twoD, col=col[3], pch=18)  
#lines(xdata, twoD, col=col[3], lty=2, lwd=2)

# Plot avg/baseline
points(xdata, avg, col='black', pch=19)
lines(xdata, avg, col='black', lty=2, lwd=2)

legend(12,1.12,c('model','mean edit distance'),col=c(col[1],'black'),pch=c(15,19),lty=c(1,2))

# Plot legend in 3 columns
#legend_order <- matrix(1:6, ncol=3, byrow=TRUE)

#legend(1,1.33, c('c+k','c','k','no parameters','mean edit distance')[legend_order], 
#       col=c(col[1],col[2],col[3],col[4],'black')[legend_order], 
#       pch=c(15,16,17,18,19)[legend_order], lty=c(3,3,3,3,2)[legend_order], ncol=3, cex=1.2)
