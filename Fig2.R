
rm(list=ls())

nyrs = 38
expvar = scan('expvar.txt')
dim(expvar) = c(6,4,2,nyrs)

# ASCII file with data dimensions
# 6 columns:  year,domain,iteration,mean,trend,parabola
# 4*2*nyrs rows: iteration,domain,year

# Normalized mean-squared error
mse = 1-expvar

lplotfile = FALSE
if (!lplotfile) pdf('Fig2a.pdf')
xlim = c(0.6,4.3)
ylim = c(0,2.5)
ys = mse[4,,1,]; ym = apply(ys,1,median); ysort = apply(ys,1,sort)
plot(ym,xlim=xlim,ylim=ylim,type='l',lwd=2,col='blue',xlab='experiment',ylab='',xaxt='n',main=substitute(paste('(b) Pacific ',italic('MSE'),'                                        ',sep='')),cex.axis=1.5,cex.main=1.8,cex.lab=1.5)
for (z in 1:1000) {
   lines(ym+(ysort[28,]-ym)*z/1000,lwd=1,col='lightgreen')
   lines(ym-(ym-ysort[10,])*z/1000,lwd=1,col='lightgreen')
   lines(c(2.65,4.15),3+rep(-0.825+0.3*z/1000,2),lwd=1,col='lightgreen')
   }
text(3.4,3-0.7,'JJAS mean',cex=1.8,col='darkgreen')
ys = mse[5,,1,]; ym = apply(ys,1,median); ysort = apply(ys,1,sort)
for (z in 1:1000) {
   lines(ym+(ysort[28,]-ym)*z/1000,lwd=1,col='lightskyblue1')
   lines(ym-(ym-ysort[10,])*z/1000,lwd=1,col='lightskyblue1')
   lines(c(2.65,4.15),3+rep(-1.200+0.3*z/1000,2),lwd=1,col='lightskyblue1')
   }
text(3.4,3-1.075,'JJAS trend',cex=1.8,col='blue')
lo = ysort[28,]  # "lo" now upper for blue
ys = mse[6,,1,]; ym = apply(ys,1,median); ysort = apply(ys,1,sort)
for (z in 1:1000) {
   lines(ym+(ysort[28,]-ym)*z/1000,lwd=1,col='orange1')
   lines(ym-(ym-ysort[10,])*z/1000,lwd=1,col='orange1')
   lines(c(2.65,4.15),3+rep(-1.450+0.3*z/1000,2),lwd=1,col='orange1')
   }
text(3.4,3-1.325,'JJAS parabola',cex=1.8,col='darkorange3')
hi = ysort[10,]  # "hi" now lower for orange
for (z in 1:1000) {
   lines(lo+(hi-lo)*z/1000,lwd=1,col='lightskyblue3')
   lines(c(2.65,4.15),3+rep(-1.200+0.05*z/1000,2),lwd=1,col='lightskyblue3')
   }

text(3.85,1.3,'IQR',cex=1.3)
text(3.85,1.16,'overlap',cex=1.3)
lines(c(3.575,3.25),1-c(-0.2,0.285),lwd=2)

ys = mse[4,,1,]; ym = apply(ys,1,median); ysort = apply(ys,1,sort)
points(ym,pch=16,cex=2,col='darkgreen'); lines(ym,lwd=2,col='darkgreen')
maxval = apply(ys,1,median)[4]
text(4.05,maxval,round(maxval,2),cex=1.2,col='darkgreen',pos=4)
minval = apply(ys,1,median)[1]
text(0.96,minval,round(minval,2),cex=1.2,col='darkgreen',pos=2)
ys = mse[5,,1,]; ym = apply(ys,1,median); ysort = apply(ys,1,sort)
points(ym,pch=16,cex=2,col='blue'); lines(ym,lwd=2,col='blue')
maxval = apply(ys,1,median)[4]
text(4.05,maxval,round(maxval,2),cex=1.2,col='blue',pos=4)
minval = apply(ys,1,median)[1]
text(0.96,minval,round(minval,2),cex=1.2,col='blue',pos=2)
ys = mse[6,,1,]; ym = apply(ys,1,median); ysort = apply(ys,1,sort)
points(ym,pch=16,cex=2,col='darkorange3'); lines(ym,lwd=2,col='darkorange3')
maxval = apply(ys,1,median)[4]
text(4.05,maxval,round(maxval,2),cex=1.2,col='darkorange3',pos=4)
minval = apply(ys,1,median)[1]
text(0.96,minval,round(minval,2),cex=1.2,col='darkorange3',pos=2)
lines(c(0.65,4.35),c(1,1),lty=2,lwd=2.5)
axis(side = 1, at=c(1,2,3,4),c("Control", "1", "2", "3"), cex.axis=1.8)
box()
if (!lplotfile) dev.off()


if (!lplotfile) pdf('Fig2b.pdf')
xlim = c(0.6,4.3)
ylim = c(0,2.5)
ys = mse[4,,2,]; ym = apply(ys,1,median); ysort = apply(ys,1,sort)
plot(ym,xlim=xlim,ylim=ylim,type='l',lwd=2,col='blue',xlab='experiment',ylab='',xaxt='n',main=substitute(paste('(a) Indian Ocean ',italic('MSE'),'                             ',sep='')),cex.axis=1.5,cex.main=1.8,cex.lab=1.5)
mtext(side=2,padj=-2,substitute(paste(italic('MSE'),' (unit-less)',sep='')),cex=1.5)
ys = mse[5,,2,]; ym = apply(ys,1,median); ysort = apply(ys,1,sort)
for (z in 1:1000) {
   lines(ym+(ysort[28,]-ym)*z/1000,lwd=1,col='lightskyblue1')
   lines(ym-(ym-ysort[10,])*z/1000,lwd=1,col='lightskyblue1')
   lines(c(2.65,4.15),3+rep(-1.200+0.3*z/1000,2),lwd=1,col='lightskyblue1')
   }
text(3.4,3-1.075,'JJAS trend',cex=1.8,col='blue')
lo = ysort[28,]  # "lo" now upper for blue
ys = mse[6,,2,]; ym = apply(ys,1,median); ysort = apply(ys,1,sort)
for (z in 1:1000) {
   lines(ym+(ysort[28,]-ym)*z/1000,lwd=1,col='orange1')
   lines(ym-(ym-ysort[10,])*z/1000,lwd=1,col='orange1')
   lines(c(2.65,4.15),3+rep(-1.450+0.3*z/1000,2),lwd=1,col='orange1')
   }
text(3.4,3-1.325,'JJAS parabola',cex=1.8,col='darkorange3')
hi = ysort[10,]  # "hi" now lower for orange
for (z in 1:1000) {
   lines(lo+(hi-lo)*z/1000,lwd=1,col='lightskyblue3')
   lines(c(2.65,4.15),3+rep(-1.200+0.05*z/1000,2),lwd=1,col='lightskyblue3')
   }
ys = mse[4,,2,]; ym = apply(ys,1,median); ysort = apply(ys,1,sort)
for (z in 1:1000) {
   lines(ym+(ysort[28,]-ym)*z/1000,lwd=1,col='lightgreen')
   lines(ym-(ym-ysort[10,])*z/1000,lwd=1,col='lightgreen')
   lines(c(2.65,4.15),3+rep(-0.825+0.3*z/1000,2),lwd=1,col='lightgreen')
   }
text(3.4,3-0.7,'JJAS mean',cex=1.8,col='darkgreen')

text(3.85,1.3,'IQR',cex=1.3)
text(3.85,1.16,'overlap',cex=1.3)
lines(c(3.575,3.25),1-c(-0.2,0.285),lwd=2)

ys = mse[5,,2,]; ym = apply(ys,1,median); ysort = apply(ys,1,sort)
points(ym,pch=16,cex=2,col='blue'); lines(ym,lwd=2,col='blue')
maxval = apply(ys,1,median)[4]
text(4.05,maxval,round(maxval,2),cex=1.2,col='blue',pos=4)
minval = apply(ys,1,median)[1]
text(0.96,minval,round(minval,2),cex=1.2,col='blue',pos=2)
ys = mse[6,,2,]; ym = apply(ys,1,median); ysort = apply(ys,1,sort)
points(ym,pch=16,cex=2,col='darkorange3'); lines(ym,lwd=2,col='darkorange3')
maxval = apply(ys,1,median)[4]
text(4.05,maxval,round(maxval,2),cex=1.2,col='darkorange3',pos=4)
minval = apply(ys,1,median)[1]
text(0.96,minval,round(minval,2),cex=1.2,col='darkorange3',pos=2)
lines(c(0.65,4.35),c(1,1),lty=2,lwd=2.5)
ys = mse[4,,2,]; ym = apply(ys,1,median); ysort = apply(ys,1,sort)
points(ym,pch=16,cex=2,col='darkgreen'); lines(ym,lwd=2,col='darkgreen')
maxval = apply(ys,1,median)[4]
text(4.05,maxval,round(maxval,2),cex=1.2,col='darkgreen',pos=4)
minval = apply(ys,1,median)[1]
text(0.96,minval,round(minval,2),cex=1.2,col='darkgreen',pos=2)
axis(side = 1, at=c(1,2,3,4),c("Control", "1", "2", "3"), cex.axis=1.8)
box()
if (!lplotfile) dev.off()

