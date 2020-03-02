# Define data (x: videos, y: fit of model, edit distance with Damerau-Levenshtein)
xdata <- c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19)
model_ck <- c(0,0,0,0,0,0,0,0,0,0,0,0,0,0.17,0.17,0,0,0.17,0.17)
k_set <- c(0.8,0.8,0,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0,0.8,0.8,0.8,0.8,0.8,0.8,0.8)
c_set <- c(0.4,0.4,0,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0,0.4,0.4,0.4,0.4,0.4,0.4,0.4)
no_params <- c(1,1,0.67,1,1,1,1,1,1,1,1,0.67,1,0.8,0.8,1,1,0.8,0.8)
globally_optimal <- c(0.4,0.4,0.67,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.67,0.4,0.33,0.33,0.4,0.4,0.33,0.33)
avg <- c(0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666,0.666)

# Plot model, c+k set
plot(xdata, model_ck, type='o', col='blue', pch=15, lty=1, ylim=c(0,1.2), lwd=2, 
     ylab='Normalized Damerau-Levenshtein distance',
     xlab='Video sequence', las=1, xaxt='n', cex.lab=1.4)
axis(side=1, at=1:19, labels=xdata, cex.axis=1)

# Plot model without c
points(xdata, k_set, col='red', pch=16)
lines(xdata, k_set, col='red', lty=1, lwd=2)

# Plot model without k
points(xdata, c_set, col='dark green', pch=17)
lines(xdata, c_set, col='dark green', lty=1, lwd=2)

# Plot greedy without params
points(xdata, no_params, col='dark magenta', pch=18)
lines(xdata, no_params, col='dark magenta', lty=1, lwd=2)

# Plot avg/baseline
points(xdata, avg, col='black', pch=20)
lines(xdata, avg, col='black', lty=2, lwd=2)

# Plot globally optimal/shortest path
points(xdata, globally_optimal, col='darkorange1', pch=21)
lines(xdata, globally_optimal, col='darkorange1', lty=2, lwd=2)

# Plot legend in 3 columns
legend_order <- matrix(1:6, ncol=3, byrow=TRUE)

legend(2,1.23, c('c+k set','k set','c set','no parameters set','mean edit distance','global shortest path')[legend_order], 
       col=c('blue','red','dark green','dark magenta','black','darkorange1')[legend_order], 
       pch=c(15,16,17,18,20,21)[legend_order], lty=c(1,1,1,1,2,2)[legend_order], ncol=3, cex=1.2)
