library(RColorBrewer)

# Define data (x: videos, y: fit of model, edit distance with Damerau-Levenshtein)
xdata <- c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19)
model_ck <- c(0.1,0.1,0,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0,0.1,0.5,0.5,0.1,0.1,0.1,0.1)
k_set <- c(0.2,0.2,0,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0,0.2,0.34,0.34,0.2,0.2,0.33,0.33)
c_set <- c(0.4,0.4,0,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0,0.4,0.5,0.5,0.4,0.4,0.2,0.2)
no_params <- c(0.59,0.59,0.33,0.59,0.59,0.59,0.59,0.59,0.59,0.59,0.59,0.33,0.59,0.57,0.57,0.59,0.59,0.37,0.37)
avg <- c(0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666)

col = brewer.pal(n=6,name='Set1')

# Plot model, c+k set
plot(xdata, model_ck, type='o', col=col[1], pch=15, lty=1, ylim=c(0,0.8), lwd=2, 
     ylab='Normalized Damerau-Levenshtein distance', main="TUM data, parameters",
     xlab='Video sequence', las=1, xaxt='n', cex.lab=1.4)
axis(side=1, at=1:19, labels=xdata, cex.axis=1)

# Plot model without c
points(xdata, k_set, col=col[2], pch=16)
lines(xdata, k_set, col=col[2], lty=1, lwd=2)

# Plot model without k
points(xdata, c_set, col=col[3], pch=17)
lines(xdata, c_set, col=col[3], lty=1, lwd=2)
  
# Plot greedy without params
points(xdata, no_params, col=col[4], pch=18)
lines(xdata, no_params, col=col[4], lty=1, lwd=2)

# Plot avg/baseline
points(xdata, avg, col='black', pch=20)
lines(xdata, avg, col='black', lty=2, lwd=2)



# Plot legend in 3 columns
legend_order <- matrix(1:6, ncol=3, byrow=TRUE)

legend(2,0.83, c('c+k set','k set','c set','no parameters set','mean edit distance')[legend_order], 
       col=c(col[1],col[2],col[3],col[4],'black')[legend_order], 
       pch=c(15,16,17,18,20)[legend_order], lty=c(1,1,1,1,2)[legend_order], ncol=3, cex=1.2)
