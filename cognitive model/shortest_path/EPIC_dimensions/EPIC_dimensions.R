library(RColorBrewer)

# Define data (x: videos, y: fit of model, edit distance with Damerau-Levenshtein)
xdata <- c(1,2,3,4,5,6,7)
avg <- c(0.446378670634921,0.447737202380952,0.471661656746032,0.420670386904762,0.46237683531746,0.441768204365079,
         0.424001041666667)
median <- c(0.7012,0.569283333333333,0.714483333333333,0.598,0.721833333333333,0.6447,0.707016666666667)

col = brewer.pal(n=6,name='Set1')

# Plot avg
plot(xdata, avg, type='o', col=col[1], pch=15, lty=3, ylim=c(0,1.0), lwd=2, 
     ylab='Normalized Damerau-Levenshtein distance', main="EPIC data",
     xlab='Dimensions', las=1, xaxt='n', cex.lab=1.4)
axis(side=1, at=1:7, labels=c('x','y','z','xy','xz','yz','xyz'), cex.axis=1)

# Plot median
points(xdata, median, col=col[2], pch=16)
lines(xdata, median, col=col[2], lty=1, lwd=2)

# Plot model without k
#points(xdata, c_set, col=col[3], pch=17)
#lines(xdata, c_set, col=col[3], lty=1, lwd=2)

# Plot greedy without params  
#points(xdata, no_params, col=col[4], pch=18)
#lines(xdata, no_params, col=col[4], lty=3, lwd=2)

# Plot avg/baseline
#points(xdata, avg, col='black', pch=20)
#lines(xdata, avg, col='black', lty=2, lwd=2)

# Plot model
#points(xdata, model_ck, col=col[1], pch=15)
#lines(xdata, model_ck, col=col[1], lty=3, lwd=2)


legend(1,1.03, c('avg', 'median'),col=c(col[1],col[2]),pch=c(15,16),lty=c(3,1))

# Plot legend in 3 columns
#legend_order <- matrix(1:6, ncol=3, byrow=TRUE)

#legend(1,1.03, c('avg', 'mean')[legend_order], 
#       col=c(col[1],col[2])[legend_order], 
#       pch=c(15,16)[legend_order], lty=c(3,1)[legend_order], ncol=3, cex=1.2)

