library(sqldf)
library(factoextra)
library(fastcluster)
library(clValid)
library(cluster)
library(fpc)

ff <- read.csv("~/Yutian/Data Mining/final/final.csv", header=FALSE, na.strings=".")
ff = ff[-1,]
final<-ff[,1:7]
colnames(final)<-c("course1", "course2","course3","course4","course5","course6","course7")

pra<-final
factor1 <- sqldf("select distinct course1 as 'class_type' from pra")
factor2 <- sqldf("select distinct course2 as 'class_type' from pra")
factor3 <- sqldf("select distinct course3 as 'class_type' from pra")
factor4 <- sqldf("select distinct course4 as 'class_type' from pra")
factor5 <- sqldf("select distinct course5 as 'class_type' from pra")
factor6 <- sqldf("select distinct course6 as 'class_type' from pra")
factor7 <- sqldf("select distinct course7 as 'class_type' from pra")

factor<-c(factor1, factor2, factor3, factor4, factor5, factor6, factor7) 
vec <- unique(Reduce(c,factor))

fac<-as.data.frame.vector(vec)
#delete missing value
fac1 <- fac[!is.na(fac$vec), ]
fac2<-as.data.frame.vector(fac1)
pre<-t(fac2)

list<-as.list(fac1)
#creating an empty matrix
pre1<-matrix( 0, nrow = 7247, ncol = 630)
use<-rbind(pre,pre1)
colnames(use) <- unlist(use[1,])
use1<-use[-1,]
use2<-as.data.frame(use1)
na.zero <- function (x) {
  x[is.na(x)] <- 0
  return(x)
}

###for the first course
ve<-pra[,1]
rr<-as.data.frame.vector(ve)
mat0<-cbind(rr, use2)
mat<-as.matrix(mat0)
mm1 <- outer(ve,colnames(mat),"==")
storage.mode(mm1) <- "numeric" 
dimnames(mm1) <- dimnames(mat) 
mm1=mm1[,-1]
mm1<-na.zero(mm1)

###for second course
ve<-pra[,2]
rr<-as.data.frame.vector(ve)
mat0<-cbind(rr, use2)
mat<-as.matrix(mat0)
mm2 <- outer(ve,colnames(mat),"==")
storage.mode(mm2) <- "numeric" 
dimnames(mm2) <- dimnames(mat) 
mm2=mm2[,-1]
mm2<-na.zero(mm2)

###for third course
ve<-pra[,3]
rr<-as.data.frame.vector(ve)
mat0<-cbind(rr, use2)
mat<-as.matrix(mat0)
mm3 <- outer(ve,colnames(mat),"==")
storage.mode(mm3) <- "numeric" 
dimnames(mm3) <- dimnames(mat) 
mm3=mm3[,-1]
mm3<-na.zero(mm3)

###for the forth course
ve<-pra[,4]
rr<-as.data.frame.vector(ve)
mat0<-cbind(rr, use2)
mat<-as.matrix(mat0)
mm4 <- outer(ve,colnames(mat),"==")
storage.mode(mm4) <- "numeric" 
dimnames(mm4) <- dimnames(mat) 
mm4=mm4[,-1]
mm4<-na.zero(mm4)

###for the fifth course
ve<-pra[,5]
rr<-as.data.frame.vector(ve)
mat0<-cbind(rr, use2)
mat<-as.matrix(mat0)
mm5 <- outer(ve,colnames(mat),"==")
storage.mode(mm5) <- "numeric" 
dimnames(mm5) <- dimnames(mat) 
mm5=mm5[,-1]
mm5<-na.zero(mm5)

###for the six course
ve<-pra[,6]
rr<-as.data.frame.vector(ve)
mat0<-cbind(rr, use2)
mat<-as.matrix(mat0)
mm6 <- outer(ve,colnames(mat),"==")
storage.mode(mm6) <- "numeric" 
dimnames(mm6) <- dimnames(mat) 
mm6=mm6[,-1]
mm6<-na.zero(mm6)

###for the seventh course
ve<-pra[,7]
rr<-as.data.frame.vector(ve)
mat0<-cbind(rr, use2)
mat<-as.matrix(mat0)
mm7 <- outer(ve,colnames(mat),"==")
storage.mode(mm7) <- "numeric" 
dimnames(mm7) <- dimnames(mat) 
mm7=mm7[,-1]
mm7<-na.zero(mm7)

#sum up values:
mm=mm1+mm2+mm3+mm4+mm5+mm6+mm7

write.csv(mm, file = "C:/Users/Mandy Nespeca/Documents/Yutian/Data Mining/Homework/clustering.csv")

distance<-dist(mm,method="binary",diag= FALSE, upper= FALSE, p=2)
ward<-hclust(distance, method = "ward.D", members = NULL)
members<-cutree(ward,k=9)
cent<-NULL
for(k in 1:9){
  cent <- rbind(cent, colMeans(mm[members == k, , drop = FALSE]))
}
hc2 <- hclust(dist(cent)^2, method = "ward.D", members = table(members))
opar <- par(mfrow = c(1, 2))
plot(ward,  labels = FALSE, hang = -1, main = "Original Tree")
plot(hc2, labels = FALSE, hang = -1, main = "Ward's cut 9 clusters")
par(opar)

#plot to determine cluster numbers
ren<-fviz_nbclust(mm, hcut, method="silhouette", hc_metric="binary",hc_method="ward.D",k.max=20)
ren1<-fviz_nbclust(mm, hcut, method="wss",hc_metric="binary",hc_method="ward.D",k.max=20)
print(ren)
print(ren1)

###get the validation result
res.hc <- eclust(mm, "hclust", k = 9, hc_metric = "binary",
                 method = "ward.D", graph = FALSE) 
hc_stats <- cluster.stats(d=distance,  res.hc$cluster)
print(hc_stats)

hc_stats1<-hc_stats$within.cluster.ss 
hc_stats2<-hc_stats$clus.avg.silwidths
print(hc_stats1)
print(hc_stats2)


clustering1<-as.data.frame.vector(members)
result<-cbind(members, mm)
result<-as.data.frame(result)
write.csv(clustering1,file = "C:/Users/Mandy Nespeca/Documents/Yutian/Data Mining/final/nine_cluster_id.csv")
write.csv(result,file="C:/Users/Mandy Nespeca/Documents/Yutian/Data Mining/final/nine_cluster.csv")

#dunn index
dunnindex<-dunn(distance = NULL, members, Data = result)
print(dunnindex)
#VRC by Calinski-Harabasz Index
vrc<-calinhara(distance,res.hc$cluster,9)
print(vrc)
