import unicodecsv
import pandas as pd

def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

enrollments = read_csv('D:\udacity\data_analyst\project2/enrollments.csv')
daily_engagement = read_csv('D:\udacity\data_analyst\project2/daily_engagement.csv')
project_submissions = read_csv('D:\udacity\data_analyst\project2/project_submissions.csv')
df_enrollments = pd.DataFrame(enrollments)
df_daily_engagement = pd.DataFrame(daily_engagement)
df_project_submissions= pd.DataFrame(project_submissions)
print "df_enrollments"
print df_enrollments.shape
print "df_enrollments_unique"
print df_enrollments["account_key"].unique().shape
print "df_daily_engagement"
print df_daily_engagement.shape
print "df_daily_engagement_unique"
print df_daily_engagement["acct"].unique().shape
print "df_project_submissions"
print df_project_submissions.shape
print "df_project_submissions"
print df_project_submissions["account_key"].unique().shape

