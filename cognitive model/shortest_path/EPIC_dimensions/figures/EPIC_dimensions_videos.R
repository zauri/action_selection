library(RColorBrewer)

# Define data (x: videos, y: fit of model, edit distance with Damerau-Levenshtein)
xdata <- c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)
x <- c(0,0.6458,0.769,1,0.16433,0.16833,0.7158,0.7245,0.6125,0.752714286,0.72833,0.7944,0.6734,0.2525,0.8686,0.6866)
y <- c(0.502,0.8,0.5,1,0.33533,0.50133,0.4648,0.700167,0.37,0.797428571,0.554167,0.84967,0.8526,0.2485,0.9054,0.5844)
z <- c(0.667,0.8,0.753,0.703,0.44633,0.167,0.7008,0.728167,0.57875,0.805714286,0.729833,0.76822,0.8356,0.2805,0.9044,0.6016)
xy <- c(0.50433,0.653,0.5,1,0,0.33,0.6,0.6975,0.37175,0.730142857,0.5933,0.83767,0.8478,0.256,0.8672,0.596)
xz <- c(0.33,0.4,0.7385,1,0.17033,0.174,0.6992,0.721833,0.57975,0.785857143,0.721833,0.80422,0.8,0.241,0.9,0.8)
yz <- c(0.67,0.8,0.7475,0.7095,0.44733,0.16067,0.6952,0.715167,0.57925,0.799285714,0.72567,0.76922,0.831,0.2545,0.4968,0.5942)
xyz <- c(0.33,0.8,0.5,1,0,0.33,0.6952,0.7267,0.38125,0.786,0.718833,0.81533,0.8,0.235,0.4964,0.8)

col = brewer.pal(n=7,name='Set1')

# Plot x
plot(xdata, x, type='o', col=col[1], pch=15, lty=3, ylim=c(0,1.2), lwd=2, 
     ylab='Normalized Damerau-Levenshtein distance', main="EPIC data, average edit distance for dimensions",
     xlab='Video', las=1, xaxt='n', cex.lab=1.4)
axis(side=1, at=1:16, labels=xdata, cex.axis=1)

# Plot y
points(xdata, y, col=col[2], pch=16)
lines(xdata, y, col=col[2], lty=1, lwd=2)

# Plot z
points(xdata, z, col=col[3], pch=17)
lines(xdata, z, col=col[3], lty=1, lwd=2)

# Plot xy
points(xdata, xy, col=col[4], pch=18)
lines(xdata, xy, col=col[4], lty=3, lwd=2)

# Plot xz
points(xdata, xz, col=col[5], pch=20)
lines(xdata, xz, col=col[5], lty=2, lwd=2)

# Plot yz
points(xdata, yz, col=col[6], pch=19)
lines(xdata, yz, col=col[6], lty=3, lwd=2)

# Plot yz
points(xdata, xyz, col=col[7], pch=15)
lines(xdata, xyz, col=col[7], lty=3, lwd=2)



# Plot legend in 3 columns
legend_order <- matrix(1:8, ncol=4, byrow=TRUE)

legend(1,1.23, c('x','y','z','xy','xz','yz','xyz')[legend_order], 
       col=c(col[1],col[2],col[3],col[4],col[5],col[6],col[7])[legend_order], 
       pch=c(15,16,17,18,20,19,15)[legend_order], lty=c(3,1,1,3,2,3,3)[legend_order], ncol=4, cex=1.2)

