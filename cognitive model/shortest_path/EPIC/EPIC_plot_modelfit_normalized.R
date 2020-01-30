# Define data (x: videos, y: fit of model, edit distance with Damerau-Levenshtein)
xdata <- c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)
model_ck <- c(0.33,0.6,0.25,0.5,0,0,0,0.43,0.25,0.29,0.33,0.78,0.8,0,0.4,0.4)
k_set <- c(0.33,0.6,0.25,0.5,0,0.33,0,0.71,0.25,0.29,0.33,0.78,0.8,0,0.4,0.4)
c_set <- c(0.67,0.6,0.25,0.5,0,0,0,0.57,0.5,0.43,0.67,0.78,0.8,0.5,0.4,0.6)
no_params <- c(0.67,0.6,0.75,1,0,0.33,0.2,0.86,0.5,0.43,0.67,1,0.8,0.5,0.4,0.6)
avg <- c(0.44,0.668,0.605,0.605,0.44,0.44,0.668,0.756,0.605,0.756,0.725,0.80,0.668,0.25,0.668,0.668)

# Plot model, c+k set
plot(xdata, model_ck, type='o', col='blue', pch=15, lty=2, ylim=c(0,1.5), lwd=2, 
     ylab='Normalized Damerau-Levenshtein distance',
     xlab='Video sequence', las=1, xaxt='n', cex.lab=1.4)
axis(side=1, at=1:16, labels=xdata, cex.axis=1)

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

# Plot model
points(xdata, model_ck, col='blue', pch=15)
lines(xdata, model_ck, col='blue', lty=2, lwd=2)

legend(11.8,1.53,legend=c('c+k set', 'k set', 'c set', 'no parameters set','mean edit distance'), 
       col=c('blue', 'red', 'dark green', 'dark magenta','black'), 
       pch=c(15,16,17,18,20), lty=c(1,1,1,1,2), ncol=1, cex=1.2)

