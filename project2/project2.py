import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
from scipy.stats.stats import pearsonr
from scipy.stats import ttest_ind

path=r"D:\udacity\data_analyst\project2/titanic_data.csv"
titanic=pd.read_csv(path)
def groupby_into_group_list(data,column):
    li=[]
    grouped=data.groupby(column)
    for name,group in grouped:
        li.append(group)
    return li
def survived_rate_by_group(group):
    survived=group["Survived"]
    return float(survived.sum())/len(survived)
def print_1column_analyse(data,column):
    group_list=groupby_into_group_list(data,column)
    for i in group_list:
        print i[column].iloc[0],":","{0:.2f}%".format(survived_rate_by_group(i)*100)
def result_of_1column_analyse(data,column):
    result=pd.Series()
    for name,group in data.groupby(column):
        if type(name) !=str:
            name=str(name)
        result[name]=survived_rate_by_group(group)
    return result
def print_2column_analyse(data,column1,column2):
    result=pd.DataFrame(columns=[])
    grouped=data.groupby(column1)
    column_list=[]
    for name,group in grouped:
        small_grouped=group.groupby(column2)
        column_list.append(name)
        new_row=pd.Series()
        for small_name,small_group in small_grouped:
            if type(small_name)!=str:
                small_name=str(small_name)
            new_row[small_name]="{0:.2f}%".format(survived_rate_by_group(small_group)*100)+"({:d})".format(small_group["Survived"].sum())
        result=pd.concat([result,new_row],axis=1)
    result.columns=column_list
    return result
def result_of_2column_analyse(data,column1,column2):
    result=pd.DataFrame(columns=[])
    grouped=data.groupby(column1)
    column_list=[]
    for name,group in grouped:
        small_grouped=group.groupby(column2)
        if name!=str:
            name=str(name)
        column_list.append(name)
        new_row=pd.Series()
        for small_name,small_group in small_grouped:
            if type(small_name)!=str:
                small_name=str(small_name)
            new_row[small_name]=survived_rate_by_group(small_group)
        result=pd.concat([result,new_row],axis=1)
    result.columns=column_list
    return result 
def age_classify(row):
    if row["Age"]<=4:
        return "Baby"
    elif row["Age"]<=12:
        return "Child"
    elif row["Age"]<=18:
        return "Youngster"
    elif row["Age"]<=45:
        return "Adult"
    else:
        return "Senior"
def fare_classify(row):
    for i in range(0,100,10):
        if row["Fare"]<=np.percentile(np.array(titanic["Fare"]),i+10):
            return round(np.array(titanic["Fare"])[np.array([a and b for a,b in zip(np.array(titanic["Fare"])>=np.percentile(np.array(titanic["Fare"]),i),np.array(titanic["Fare"])<=np.percentile(np.array(titanic["Fare"]),i+10))])].mean(),2)

def visualize_2column_result(result):
    N=len(result.index)
    M=len(result.columns)
    ind = np.arange(N)
    width = 1/(float(M)+1)
    fig, ax = plt.subplots()
    color=cycle("rybg")
    for i,col in zip(range(M),color):        
        each_rect = ax.bar(ind+i*width, list(result.ix[:,i]), width, color=col)
        each_rect.set_label(result.columns[i])
    ax.set_ylabel('Survived rate')
    ax.set_title('2column result visualisation')
    ax.set_xticks(ind + width)
    ax.set_xticklabels([x for x in result.index])
    ax.legend()
    
           
#result=result_of_2column_analyse(titanic,"Sex","Pclass")                                   
#groupby_Pclass=groupby_into_group_list(titanic,"Pclass")

# find survived percentage of passengers with different class      
print "\nClass:"
print_1column_analyse(titanic,"Pclass")

# find survived percentage of passengers with different Sex
print "\nSex:"
print_1column_analyse(titanic,"Sex")

# find survived percentage of passengers with different embarked port
print "\nEmbarked port:"
print_1column_analyse(titanic,"Embarked")

# find survived percentage of passengers with different age
print "\nAge:"
titanic_Age_cleaned=titanic.dropna(subset=["Age"])# drop all the NAN data in the column "Age"
age_classified=titanic_Age_cleaned.apply(age_classify,axis=1)
age_classified=pd.Series(age_classified,name="Age_C")
titanic_Age_cleaned_classified=pd.concat([titanic_Age_cleaned,age_classified],axis=1)
print_1column_analyse(titanic_Age_cleaned_classified,"Age_C")
data,column1,column2=titanic,"Sex","Pclass"

# multi dimensional analyse
print "\nmultiple dimensional analyse:"
fare_classified=pd.Series(titanic.apply(fare_classify,axis=1),name="Fare_C")
titanic_Fare_classified=pd.concat([titanic,fare_classified],axis=1)
result1=result_of_1column_analyse(titanic_Fare_classified,"Fare_C")
result1_index=[float(x) for x in result1.index]
correlation=pearsonr(result1_index,result1.values)
fig1,ax1=plt.subplots(1)
ax1.scatter(result1_index, result1.values, s=30, c="r", alpha=0.8)
plt.grid()
ax1.set_xlabel("mean ticket price of the group")
ax1.set_ylabel("survive rate")
print result1
print "price mean:",np.array(result1_index).mean()
print "survive rate mean:",result1.mean()
print "correlation: ",correlation[0]
#find survived percentage of passengers with different age and class
print "\nAge and class"
print print_2column_analyse(titanic_Age_cleaned_classified,"Age_C","Pclass")

#find survived percentage of passengers with different Sex and class
print "\nSex and class"
print print_2column_analyse(titanic,"Sex","Pclass")

#visualize 2 dimensional data
result=result_of_2column_analyse(titanic_Age_cleaned_classified,"Sex","Age_C")
visualize_2column_result(result)

#find ratio of survived men and women
fig2,ax2=plt.subplots(1)
survived=titanic.groupby("Survived").get_group(1)
Sex_of_survived=survived["Sex"].values
labels = ['male', "female"]
sizes = [len(Sex_of_survived[Sex_of_survived=="male"]),len(Sex_of_survived[Sex_of_survived=="female"])]
colors = ['yellowgreen', 'mediumpurple'] 
explode = (0, 0)    # proportion with which to offset each wedge

ax2.pie(sizes,              # data
        explode=explode,    # offset parameters 
        labels=labels,      # slice labels
        colors=colors,      # array of colours
        autopct='%1.1f%%',  # print the values inside the wedges
        shadow=True,        # enable shadow
        startangle=70       # starting angle
        )
plt.axis('equal')

plt.show()

# 2 samples t-test
survived_fare=titanic.groupby("Survived").get_group(1)["Fare"]
non_survived_fare=titanic.groupby("Survived").get_group(0)["Fare"]
t, p = ttest_ind(survived_fare, non_survived_fare, equal_var=False)
print "dependent t test"
print "t:",t," p:",p
