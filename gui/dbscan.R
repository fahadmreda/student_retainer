library(gdata)
library(fpc)
library("dbscan")
library(factoextra)
library(proxy)
library(clValid)

data <- read.csv('/Users/kobypascual/Documents/School Folders/Grad School - CS/Fall 2016 - OU/Data Mining/out.csv')

# get rid of excess column
data <- data[,-8]
data <- as.matrix(data)

# function to get distance matrix
get_dist <- function(data)
{
	d <- dist(data)
	return (d)
}

# function to find the best min_pts value based on a given k
find_best_eps <- function(k)
{
	#find best eps with k = 500
	dbscan::kNNdistplot(data, k)
	# plot it ~ result is 50 for every 100 k
	abline(h = 0.15, lty = 2)
}

# Function to get the dbscan cluster
dbs <- function(eps, minPts)
{
	db <- dbscan::dbscan(data, eps, minPts, method="binary")
	db
	return(db)
}

# function to get dbscan
optics <- function(eps, minPts, eps_cl)
{
	db <- optics(data, eps, minPts, eps_cl)
	db
}

# function to visualize the clusters
plt <- function(db,data)
{
	fviz_cluster(db, data, geom = "point")
}