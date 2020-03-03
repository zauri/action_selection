library(RColorBrewer)

# Define data (x: videos, y: fit of model, edit distance with Damerau-Levenshtein)
xdata <- c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)
model_ck <- c(0.33,0.8,0.25,0.5,0,0,0.6,0.67,0.25,0.71,0.33,0.44,0.8,0,0.6,0.8)
k_set <- c(0.33,0.8,0.25,0.5,0,0.33,0.6,0.67,0.25,0.86,0.50,0.44,0.8,0,0.4,0.8)
c_set <- c(0.67,0.8,0.25,0.5,0,0,0.6,0.83,0.5,0.71,0.33,0.78,0.8,0.5,0.6,0.8)
no_params <- c(0.67,0.8,0.5,0.75,0,0.67,0.6,0.83,0.5,0.71,0.33,0.56,0.8,0.5,0.4,0.8)
avg <- c(0.44,0.666,0.605,0.605,0.44,0.44,0.666,0.723,0.605,0.756,0.723,0.806,0.666,0.25,0.666,0.666)

col = brewer.pal(n=6,name='Set1')

# Plot model, c+k set
plot(xdata, model_ck, type='o', col=col[1], pch=15, lty=3, ylim=c(0,1.0), lwd=2, 
     ylab='Normalized Damerau-Levenshtein distance', main="EPIC, 3D model",
     xlab='Video sequence', las=1, xaxt='n', cex.lab=1.4)
axis(side=1, at=1:16, labels=xdata, cex.axis=1)

# Plot model without c
points(xdata, k_set, col=col[2], pch=16)
lines(xdata, k_set, col=col[2], lty=1, lwd=2)

# Plot model without k
points(xdata, c_set, col=col[3], pch=17)
lines(xdata, c_set, col=col[3], lty=1, lwd=2)

# Plot greedy without params
points(xdata, no_params, col=col[4], pch=18)
lines(xdata, no_params, col=col[4], lty=3, lwd=2)

# Plot avg/baseline
points(xdata, avg, col='black', pch=20)
lines(xdata, avg, col='black', lty=2, lwd=2)

# Plot model
points(xdata, model_ck, col=col[1], pch=15)
lines(xdata, model_ck, col=col[1], lty=3, lwd=2)


# Plot legend in 3 columns
legend_order <- matrix(1:6, ncol=3, byrow=TRUE)

legend(2,1.03, c('c+k set', 'k set', 'c set', 'no parameters set','mean edit distance')[legend_order], 
       col=c(col[1],col[2],col[3],col[4],'black')[legend_order], 
       pch=c(15,16,17,18,20)[legend_order], lty=c(3,1,1,3,2)[legend_order], ncol=3, cex=1.2)

