---
output: 
  html_document: 
    keep_md: yes
---
Title: Accessing MongoDB from R with mongolite
Date: 2015-05-18
Tags: mongodb, R
Slug: mongodb-in-r

```{r, echo = FALSE, results='hide'}
library(knitr)
suppressPackageStartupMessages(library(ggplot2))
suppressPackageStartupMessages(library(dplyr))
theme_update(plot.background = element_rect(fill = "transparent", colour = NA))

opts_chunk$set(dev.args=list(bg="transparent"))
```

Recently, I have moved away from text files as data storage, and started using [MongoDB](https://www.mongodb.org/). While there are already two R packages (`RMongo` and `rmongodb`) interfacing with MongoDB, I was never completed satified with them - especially in comparison to the excellent [PyMongo](http://api.mongodb.org/python/current/). A couple of days ago, a new package, `mongolite`, was released and seems very promising.

Here, I quickly want to showcase some of the functions of mongolite, using [Fisher's Iris data set](http://en.wikipedia.org/wiki/Iris_flower_data_set). 
```{r}
data(iris)
# remove . to avoid problems with MongoDBs naming structure
names(iris)[1:4] = gsub("[.]","",names(iris)[1:4] ) 
head(iris)

```

First, we need to insert the data from R into a new collection in MongoDB. This is done by first establishing a connection to the collection in the database, and then calling the `insert` function on the connection handler. 
```{r, echo=FALSE, results='hide'}
library(mongolite)
c = mongo(collection = "iris", db = "tutorials")
c$drop()
```
```{r, collapse =TRUE}
library(mongolite)
c = mongo(collection = "iris", db = "tutorials")
c$insert(iris)
```
We get some nice feedback from the function, showing us that we inserted 150 rows (which is the total number of rows in the Iris data set). Let's start exploring the data with `mongolite`. You can easily get the total number of rows, as well as the unique values within the `Species` column/field: 

```{r, collapse=TRUE}
c$count()
c$distinct("Species")
```

It's also possible to utilize MongoDB's aggregate function through `$aggregate`:
```{r}
c$aggregate('[{"$group": {
                "_id":"$Species", 
                "count": {"$sum":1}, 
                "avgPetalLength":{"$avg":"$PetalLength"}
              }}]')
```

Of course, with a small data set such as the Iris data, there is no drawback in simply doing the aggregating in `dplyr`, but if you are dealing with a big data set, querying the MongoDB database directly might give you some performance benefits, as not all the data has to be loaded into memory.

```{r}
iris %>%
  group_by(Species) %>%
  summarise(count = n(), avg = mean(PetalLength))
```

Similary, let's suppose we don't need all columns/fields for an analysis. For example, maybe we're only interesting in the sepal width for one particular analysis. Instead of loading all the data into memory, we can use `mongolite` to only return chosen fields:

```{r, collapse=TRUE}
sw = c$find('{}', '{"SepalWidth": 1, "Species": 1, "_id": 0}')
```
```{r sepalwidth_plot, fig.height=7, fig.width=7,}
ggplot(sw, aes(x = Species, y = SepalWidth)) + 
         geom_boxplot()
```

Of course, you can also update and remove entries in your database, as well as other functions. If you'd like to know more, have a look at the package on [github](https://github.com/jeroenooms/mongolite) and [CRAN](http://cran.r-project.org/web/packages/mongolite/).

