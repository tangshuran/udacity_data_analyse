setwd("E:/learning_R")
statesInfo <- read.csv("stateData.csv")
stateSubset <- subset(statesInfo,state.region==1)
stateSubsetBracket <- stateInfo[subset(statesInfo,state.region==1,)]
