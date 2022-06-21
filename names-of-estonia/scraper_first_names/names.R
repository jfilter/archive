library("ggplot2")

data <- read.csv("/Users/filter/code/names-of-estonia/results.csv", header=TRUE, encoding="UTF-8")

data <- subset (data, n > 1000)

data$name <- factor(data$name, levels = data$name[order(data$n)])

ggplot(data, aes(x = name, y = n, width = 1)) + geom_bar(stat = "identity") +
  theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank(),
        axis.title.y=element_blank(), axis.ticks.y=element_blank(),
        panel.grid.major.x = element_blank(), panel.grid.minor.y = element_blank(),
        panel.grid.major.y = element_line( size=1, color="white" ))
