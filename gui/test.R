library(randomForest)
RFk <- readRDS("/Users/kobypascual/Documents/School Folders/Grad School - CS/Fall 2016 - OU/Data Mining/student_retainer/gui/RFk.RDS")
load("/Users/kobypascual/Documents/School Folders/Grad School - CS/Fall 2016 - OU/Data Mining/student_retainer/gui/classification2.RDATA")

predict_new_point <- function(value)
{
    act_sat_conv<-value[[1]]
    aphours<-value[[2]]
    hsgpa<-value[[3]]
    trig<-value[[4]]
    algI<-value[[5]]
    algII<-value[[6]]
    collalg<-value[[7]]
    geometry<-value[[8]]
    precalc<-value[[9]]
    stats<-value[[10]]
    mathsenior<-value[[11]]
    FC<-value[[12]]
    AE<-value[[13]]
    IC<-value[[14]]
    GRIT<-value[[15]]
    major<-value[[16]]
    kmode<-value[[17]]

    pt <- data.frame(act_sat_conv,aphours,hsgpa,trig,algI,algII,collalg,geometry,precalc,stats,mathsenior,FC,AE,IC,GRIT,major,kmode)

    levels(pt$kmode) <- levels(classification2$kmode)
    levels(pt$major)   <- levels(classification2$major)

    pred <- predict(RFk, newdata=pt, type="prob", predict.all=TRUE)

    return(pred$aggregate)
}