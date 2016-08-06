library("dplyr")
library("ggplot2")
library("gbm")
library("reshape2")
library("grid")
library("gridExtra")

#Set BaseDir
BaseDir <- "/media/pwmiller/store/Projects/R/PISA/data"

# 
# Download the student2012.rda and the school2012.rda into the BaseDir
#  
# http://beta.icm.edu.pl/PISAcontest/data/school2012.rda
# http://beta.icm.edu.pl/PISAcontest/data/student2012.rda
#

SchoolGraphic <- function(){
  FileNames <- c("school2012", "student2012")
  #       "school2012dict", "student2012dict")
  
  for(fn in FileNames){
    load(paste0(BaseDir, "/", fn, ".rda"))
  }
  
  latinAmericanCountries <- c("Argentina", "Brazil", 
    "Chile", "Colombia", "Costa Rica",  "Mexico",
    "Peru",  "Uruguay")
  
  keepColumns <- c(
    "CNTSCHOOLID",# "Unique School identifier"
    "CNT",        # "Country code 3-character"
    "SC03Q01",    # "School Location"
    "SC01Q01",    # "Public or private" 
    
    "SCHSIZE",    # "Total school enrolment"
    
    "SC22Q01",    # "Learning Hindrance - Student truancy"
    
    "SC11Q03",    # "Student Computers - Computers with Internet" 
    "CREACTIV",   # "Extracurricular creative activities at school"
    "SC16Q06",    # "Activities - Mathematics competitions"
    
    "SC10Q61",    # "No. of math teachers - <ISCED5A> Qual Full Time"
    "PROPMATH",   # "Proportion of math teachers" 
    
    "PV1MATH", 
    "PV1READ", 
    "PV1SCIE")
  
  student2012$AvgScore <- (student2012$PV1MATH + student2012$PV1READ + student2012$PV1SCIE) / 3
  student2012$CNTSCHOOLID <- paste0(student2012$CNT, student2012$SCHOOLID)
  
  school2012$CNTSCHOOLID <- paste0(school2012$CNT, school2012$SCHOOLID)
  
  studentCols <- c("CNTSCHOOLID", "PV1MATH", "PV1READ", "PV1SCIE", "AvgScore")
  student2012 <- student2012[, studentCols] 
  student2012$PV1MATH <- as.numeric(student2012$PV1MATH)
  student2012$PV1READ <- as.numeric(student2012$PV1READ)
  student2012$PV1SCIE <- as.numeric(student2012$PV1SCIE)
  student2012$AvgScore <- as.numeric(student2012$AvgScore)
  
  groupedStudent <-  student2012 %.% group_by(CNTSCHOOLID) %.% 
    summarise(
      Math.median=median(PV1MATH),        
      Reading.median=median(PV1READ),
      Science.median=median(PV1SCIE),
      Total.median=median(AvgScore)
    )
  
  allDat <- left_join(school2012[, is.element(names(school2012), keepColumns)], 
                      groupedStudent, by="CNTSCHOOLID")
  
  rm(groupedStudent)
  rm(school2012)
  rm(student2012)
  gc()
  
  allDat$HaveComputers <- allDat$SC11Q03 > 0
  
  computerDat <- allDat[!is.na(allDat$SC11Q03) & !is.na(allDat$SC01Q01) , ]
  
  latamDat <- computerDat[is.element(computerDat$CNT, latinAmericanCountries), ]
  
  summaryDat <- latamDat %.% group_by("CNT", "HaveComputers") %.%
    summarise(count=length(Math.median), Total.median=mean(Total.median))
  
  
  summaryDat <- summaryDat[!is.na(summaryDat$HaveComputers), ]
  
  
  finalPlotDat <- dcast(summaryDat, CNT ~ HaveComputers, value.var="Total.median")
  names(finalPlotDat) <- c("Country", "ComputerNo", "ComputerYes")
  
  finalPlotDat$Diff <- round(finalPlotDat$ComputerYes - finalPlotDat$ComputerNo)
  
  finalPlotDat <- finalPlotDat[order(finalPlotDat$ComputerNo, decreasing=TRUE), ]
  
  padding <- 5
  barwidth <- 10
  ytext <- 0.35
  
  finalPlotDat$Ymin <- c(0:(nrow(finalPlotDat)-1)) * (barwidth + padding) + padding
  finalPlotDat$Ymax <- c(1:nrow(finalPlotDat)) * (barwidth + padding)
  
  finalPlotDat$YText <- (c(0:(nrow(finalPlotDat)-1)) + ytext) * (barwidth + padding) + padding
  finalPlotDat$XText <- (finalPlotDat$ComputerYes + finalPlotDat$ComputerNo) / 2
  
  plotDD <- finalPlotDat[, c("Country", "ComputerNo", "ComputerYes")]
  names(plotDD) <- c("Country", "Schools without computers", "Schools with computers")
  plotDD <- melt(plotDD, id.vars="Country")
  plotDD$YText <- finalPlotDat$YText[match(plotDD$Country, finalPlotDat$Country)]
  
  finalPlotDat$Country <- paste0(finalPlotDat$Country, ": ", finalPlotDat$Diff, " pts better")
  
  theme_pisa <- theme_grey() + theme(panel.grid.minor = element_blank(), 
     panel.grid.major = element_line(color="darkgray", linetype="dashed", size=.3),
     panel.background = element_rect(color="black"),
     plot.title = element_text(size = 19, vjust=2, face="italic"),
     axis.title = element_text(vjust=-.1, size = 14),
     axis.title.x = element_text(vjust=-.11), 
     axis.title.y = element_text(angle=90, vjust=2),
     axis.text = element_text(size=12, color="black"), plot.margin = unit(c(1,1,1,1), "cm"),
     legend.position = "bottom", legend.background = element_rect(color="black"),
     legend.title = element_blank(), legend.text = element_text(size = 14),
     strip.background = element_rect(color="black", fill="slategray1"), 
     strip.text = element_text(size = 14))
  
  outPlot1 <- ggplot(finalPlotDat) +
    
    geom_rect(aes(xmin=ComputerNo, xmax=ComputerYes, ymin=Ymin, ymax=Ymax),
              fill="white", color="black") +
    
    geom_point(data=plotDD, aes(x=value, y=YText, color=variable), size=4, shape=18) +
    
    geom_text(aes(x=XText, y=YText, label=Country),
              color="black", size=5) +
    
    labs(x="Median test score at the average school", y=NULL,
         title="Students at schools that provide computers with internet outperform on tests") +
    
    theme_pisa + theme(
      axis.text.y = element_blank(),
      axis.line.y = element_blank(),
      axis.ticks.y = element_blank(),
      panel.grid.major.y = element_blank(),
      panel.grid.minor.y = element_blank(),
      plot.margin = unit(c(0,1,1,1), "lines"))
  
  
  plotDat2 <- latamDat
  plotDat2$CompVar <- "with computers"
  plotDat2$CompVar[!plotDat2$HaveComputers] <- "without computers"
  
  plotDat2$SC01Q01 <- paste0(as.character(plotDat2$SC01Q01), " Schools")
  
  plotDat2$SC01Q01 <- factor(plotDat2$SC01Q01, levels=c("Private Schools", "Public Schools"))
  
  outPlot2 <- ggplot(plotDat2, aes(y=Total.median, x=CompVar)) +
    geom_boxplot() + facet_grid(~SC01Q01) + 
    labs(x=NULL, y="Median test scores",
         title="This trend persists when breaking down private versus public schools") +
    theme_pisa + theme(
      axis.line = element_blank(),
      panel.grid.major.x = element_blank(),
      panel.grid.minor.x = element_blank(),
      plot.margin = unit(c(1,10,6,8), "lines"))
  
  plotTitle <- textGrob(label="Internet Connectivity in Latin American Schools",
                        gp=gpar(fontsize=24))
  
  
  outGrob <- arrangeGrob(plotTitle, outPlot1, outPlot2, heights=c(1/8, 4/8, 3/8))
  
  grid.arrange(outGrob)
}

#
# Create Latin America school .png
#
png(paste0(BaseDir, "/InternetLatinAmerica.png"), width=850, height=1100)
SchoolGraphic()
dev.off()