# Define data (x: videos, y: fit of model, edit distance with Damerau-Levenshtein)
xdata <- c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)
model_ck <- c(0.33,0.6,0.25,0.5,0,0,0,0.43,0.25,0.29,0.33,0.78,0.8,0,0.4,0.4)
k_set <- c(0.33,0.6,0.25,0.5,0,0.33,0,0.71,0.25,0.29,0.33,0.78,0.8,0,0.4,0.4)
c_set <- c(0.67,0.6,0.25,0.5,0,0,0,0.57,0.5,0.43,0.67,0.78,0.8,0.5,0.4,0.6)
no_params <- c(0.67,0.6,0.75,1,0,0.33,0.2,0.86,0.5,0.43,0.67,1,0.8,0.5,0.4,0.6)

# Plot model, c+k set
plot(xdata, model_ck, type='o', col='blue', pch=15, lty=1, ylim=c(0,1.4), lwd=2, 
     ylab='Normalized Damerau-Levenshtein distance',
     xlab='Video sequence', las=1, xaxt='n', cex.lab=1.4)
axis(side=1, at=1:16, labels=xdata, cex.axis=1)

# Plot model without c
points(xdata, k_set, col='red', pch=16)
lines(xdata, k_set, col='red', lty=2, lwd=2)

# Plot model without k
points(xdata, c_set, col='dark green', pch=17)
lines(xdata, c_set, col='dark green', lty=3, lwd=2)

# Plot greedy without params
points(xdata, no_params, col='dark magenta', pch=18)
lines(xdata, no_params, col='dark magenta', lty=4, lwd=2)

legend(0.6,1.42,legend=c('c+k set', 'c not set', 'k not set', 'no parameters set'), 
       col=c('blue', 'red', 'dark green', 'dark magenta'), 
       pch=c(15,16,17,18), lty=c(1,2,3,4), ncol=1, cex=1.2)

