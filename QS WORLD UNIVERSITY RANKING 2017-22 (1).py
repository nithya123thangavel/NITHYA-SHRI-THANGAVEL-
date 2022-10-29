
intstu_country


# In[60]:


fig, ax = plt.subplots(figsize=(10,5),dpi=100)
ax.get_xaxis().set_visible(False)
sns.barp#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import chart_studio.plotly as py
import plotly.express as px
import plotly.io as pio
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import warnings
warnings.filterwarnings("ignore")


# #Data Dscription
# 
# The dataset has a total of 15 columns.
# university - name of the university
# year - year of ranking
# rank_display - rank given to the university
# score - score of the university based on the six key metrics mentioned above
# link - link to the university profile page on QS website
# country - country in which the university is located
# city - city in which the university is located
# region - continent in which the university is located
# logo - link to the logo of the university
# type - type of university (public or private)
# research_output - quality of research at the university
# student_faculty_ratio - number of students assigned to per faculty
# international_students - number of international students enrolled at the university
# size - size of the university in terms of area
# faculty_count - number of faculty or academic staff at the university

# # Load and Explore data

# In[2]:


df = pd.read_csv('qs-world-university-rankings-2017-22-V2.csv')
df


# In[3]:


corr_df = df.corr()
sns.heatmap(corr_df)
plt.show


# In[ ]:





# In[4]:


df.info()


# In[5]:


df.head()


# In[6]:


df.shape


# # Data Cleaning and Preprocessing

# In[7]:


pd.DataFrame(df.isnull().sum(),columns=['No. of Missing values'])


# In[8]:


missing_per = round(df.isna().mean() * 100, 1)
pd.DataFrame(missing_per[missing_per>0], columns=['% of Missing values'])


# In[9]:


print(len(df[df.isnull().sum(axis=1)>4]))
drop_index = df[df.isnull().sum(axis=1) > 4].index.tolist()

df.drop(drop_index,inplace=True)
print('Row which have more than 4 null values have been dropped')


# In[10]:


#Let's drop 'link' and 'logo' column as they are hyperlinks. 
#Although 'score' column can be very useful for analysis, its missing nearly 56% values. 
#When I looked for these values on the QS website, 
#I could see they have given a score only for the top 500 universities although 1000+ universities have been ranked. 
#So, I'm ignoring this column as well.


# In[11]:


df.drop(['link','logo','score'],axis=1,inplace=True)
df


# # Visualizing Univesities By Year and Type

# In[12]:


year_df = df['year'].value_counts().sort_values()
fig, ax = plt.subplots(figsize=(12,5), dpi=90)
ax.get_yaxis().set_visible(False)
sns.countplot(data=df, x='year', palette='flare');
ax.bar_label(ax.containers[0])
fig.suptitle('Number of universities ranked over the years', fontsize=15, color = '#ff4800');


# With each year, more and more universities are considered for the rankings and 2022 has the highest number of universities.

# In[13]:


explode = [0,0.1]
pie_bar_colors = ['#FB8E7E','#8EC9BB']
plt.pie(df['type'].value_counts().values, labels = df['type'].value_counts().index, explode=explode, colors=pie_bar_colors, autopct='%1.1f%%') 


# In[14]:


ax=plt.figure(figsize=(8,6))
bar_color = ['#FB8E7E','#8EC9BB']
df['type'].value_counts().plot(kind='bar',color=bar_color)
plt.title('University Types',color='#ff4800')


# In[15]:


ucw = pd.DataFrame()
ucw['Count'] = df.groupby('region')['region'].count().sort_values(ascending=False)
ucw = ucw.reset_index()
ucw


# # Distribution of Universities across continents

# In[16]:


fig, ax=plt.subplots(figsize=(8,6),dpi=90)
plt.title('Distribution of universities across continent',color='#ff4800')
fig = sns.barplot(data=ucw,x='region',y='Count',palette='rocket')
ax.bar_label(ax.containers[0])
fig


# Europe tends to be the continent with more number of universities though we have to consider the fact that they have included Russia in Europe although it belongs to both Europe and Asia. It is followed by Asia and North America.

# # Universities by Countries

# In[17]:


print('Number of contries with ranked universities: ',df['country'].nunique())


# In[18]:


University_df = df['university'].value_counts()

fig, ax = plt.subplots(figsize=(10,20),dpi=170)


sns.countplot(data=df,y='country',order=df.country.value_counts().index,palette='icefire')

ax.set_xlabel('Count',fontsize=14,color='b')

ax.set_ylabel('country',fontsize=14,color='b')


# United States consists of more number of universities that have been ranked over the years followed by United Kingdom and Germany.Out of the 195 countries in the world, only 97 countries have universities that are ranked.

# In[19]:


sort_df = df.sort_values(by='rank_display').drop_duplicates('university')
sort_df = pd.DataFrame(sort_df['city'].value_counts()[:20])
sort_df


# #  Universities by Cities 

# In[20]:


fig, ax = plt.subplots(figsize=(14,5),dpi=100)
plt.xticks(rotation=90,fontsize=14)

ax.get_yaxis().set_visible(False)


sns.barplot(data=sort_df,y='city',x=sort_df.index,palette='icefire')

plt.xticks(rotation=90,fontsize=14)
ax.bar_label(ax.containers[0])

ax.set_xlabel('City Name',fontsize=14,color='b')
fig.suptitle('Distribution of universities across cities',fontsize=16,color='b')


# The above graph considers the top 20 cities with high number of unique universities. London is an academic hotspot with a whooping 19 universities that are ranked globally!

# # Top 10 Universities in the World

# In[22]:


df10 = df[:10]
df10['university']


# # Research output of Universities

# In[23]:


fig, ax = plt.subplots(figsize=(8,4),dpi=90)
ax.get_yaxis().set_visible(False)

sns.countplot(data=df,x='research_output',hue='type',palette='Paired')
for container in ax.containers:
    ax.bar_label(container)
fig.suptitle('Research Output',fontsize=13,color='#ff4800')


# Clearly, most number of universities under consideration have "Very High" research output. Public universities outperform private universities in terms of research.

# # Student Faculty Ratio

# In[24]:


df['student_faculty_ratio'].describe()


# On average, universities tend to have 13 students per faculty.
# There are universities that have as low as 1 student per faculty.
# While there are universities that have 67 students per faculty.

# In[25]:


plt.figure(figsize=(10,5),dpi=100)
sns.histplot(data=df,x='student_faculty_ratio',bins=60,palette='rocket')


# We have a right skewed distribution. The outliers doesn't seem to affect the mean much. Most of the universities have somewhere between 5 to 20 students per faculty.

# # International Students

# In[59]:


df['international_students'].describe()


# In[37]:





# In[45]:


# S1.2: Create a function to replace the commas with periods in a Pandas series.
def comma_to_period(series):
    new_series = pd.Series(data=[float(str(item).replace(',', '.')) for item in series], index=df.index)
    return new_series


# In[39]:


df['international_students'] = comma_to_period(df['international_students'])


# In[40]:


df['international_students'].dtype


# In[54]:


df['international_students'].describe()


# In[48]:


df.iloc[df['international_students'].idxmax()]


# In[50]:


plt.figure(figsize=(10,4),dpi=100)
sns.histplot(data=df,x='international_students',bins=50,color='b')
plt.xlabel('International Students',color='b')
plt.title('Distribution of international students',color='b')


# We have a right skewed distribution here as well. There are very few outliers. Most of the universities have an intake between 0 to 5000.

# # 10 Most popular country of choice for International Students

# In[57]:


intstu_country = pd.DataFrame(df.groupby(['country'], sort=False)['international_students'].sum().sort_values(ascending=False)[:10])


# In[58]:

lot(data=intstu_country,x='international_students',y=intstu_country.index,palette='rocket')


# In[ ]:





