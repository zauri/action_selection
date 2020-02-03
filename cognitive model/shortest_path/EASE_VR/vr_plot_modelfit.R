library(RColorBrewer)

# Define data (x: videos, y: fit of model, edit distance with Damerau-Levenshtein)
xdata <- c(1,2,3,4,5,6,7,8,9,10,11,12)
#model_ck <- c(0,0,0,0,0,0,0,0,0,0,0,0,0,0.17,0.17,0,0,0.17,0.17)
#k_set <- c(0.8,0.8,0,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0,0.8,0.8,0.8,0.8,0.8,0.8,0.8)
c_set <- c(0.2,0.43,0.17,0.33,0.17,0.33,0.67,0.33,0.33,0.17,0.17,0.33)
no_params <- c(0.2,0.43,0.17,0.33,0.17,0.33,0.67,0.33,0.33,0.17,0.17,0.33)
avg <- c(0.666,0.756,0.723,0.723,0.723,0.723,0.723,0.723,0.723,0.723,0.723,0.723)

# Plot model, c set
plot(xdata, no_params, type='o', col='blue', pch=15, lty=1, ylim=c(0,1.0), lwd=2, 
     ylab='Normalized Damerau-Levenshtein distance',
     xlab='Unique sequence (continuous numbering)', las=1, xaxt='n', cex.lab=1.4)
axis(side=1, at=1:12, labels=xdata, cex.axis=1)

# Plot greedy without params
#points(xdata, no_params, col='blue', pch=18)
#lines(xdata, no_params, col='blue', lty=3, lwd=2)

# Plot avg/baseline
points(xdata, avg, col='black', pch=20)
lines(xdata, avg, col='black', lty=2, lwd=2)


# Plot legend in 3 columns
legend_order <- matrix(1:2, ncol=2, byrow=TRUE)

legend(2,1.03, c('no parameters set','mean edit distance')[legend_order], 
       col=c('blue','black')[legend_order], 
       pch=c(15,20)[legend_order], lty=c(1,2)[legend_order], ncol=2, cex=1.2)
