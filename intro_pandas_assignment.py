
# coding: utf-8

# # Instructions
#
# Tonight you're going to practice working in Pandas. You'll walk through instantiating a `DataFrame`, reading data into it, looking at and examining that data, and then playing with it. We'll be using the data in the `data` folder located within this directory (it's the same wine data that we looked at during lecture). Typically, we use IPython notebooks like this for a very specific set of things - presentations and EDA. Tonight, as we'll be playing around with `Pandas`, much of what we'll be doing is considered EDA. Therefore, by using a notebook, we'll get a tighter feedback loop with our work than we would trying to write a script. But, in general, **we do not use IPython notebooks for development**.
#
# Below, we've put a set of questions and then a cell for you to work on answers. However, feel free to add additional cells if you'd like. Often it will make sense to use more than one cell for your answers.
#
# # Assignment Questions
#
# ### Part 1 - The Basics of DataFrames
#
# Let's start off by following the general workflow that we use when moving data into a DataFrame:
#
#     * Importing Pandas
#     * Reading data into the DataFrame
#     * Getting a general sense of the data
#
# Your tasks, right now:
#
# 1. Import pandas
# 2. Read the wine data into a DataFrame.
# 3. Use the `attributes` and `methods` available on DataFrames to answer the following questions:
#     * How many rows and columns are in the DataFrame?
#     * What data type is in each column?
#     * Are all of the variables continuous, or are any categorical?
#     * How many non-null values are in each column?
#     * What are the min, mean, max, median for all numeric columns?

# In[15]:


import pandas as pd
import numpy as np
red_df = pd.read_csv('./data/winequality-red.csv', sep=';')
red_df.head(10)


#  * What data type is in each column?

# In[27]:


red_df.info()


# In[24]:


red_df.describe()


# * How many non-null values are in each column?

# In[30]:


red_df[red_df.isnull().any(axis=1)].count()


# In[37]:


## check to see how to count null values for each column in a more readable way...


# In[31]:


copy_df = red_df
copy_df['dummy'] = np.nan


# In[34]:


copy_df.head()


# In[45]:


copy_df.isnull().sum(axis=0)


# ### Part 2 - Practice with Grabbing Data
#
# Let's now get some practice with grabbing certain parts of the data. If you'd like some extra practice, try answering each of the questions in more than one way (because remember, we can often grab our data in a couple of different ways).
#
# 1. Grab the first 10 rows of the `chlorides` column.

# In[ ]:


red_df.loc[ 0:10, 'chlorides']


# In[56]:


red_df.iloc[ -10:  , 'chlorides']


# #### 2 -  Grab the last 10 rows of the `chlorides` column.

# In[60]:


red_df['chlorides'].tail(10)


# ####  3. Grab indices 264-282 of the `chlorides` **and** `density` columns.

# In[53]:


red_df.loc[264:282, 'density']


# #### 4. Grab all rows where the `chlorides` value is less than 0.10.

# In[66]:


red_df.query('chlorides < .10').sort_values('chlorides')


# #### 5. Now grab all the rows where the `chlorides` value is greater than the column's mean (try **not** to use a hard-coded value for the mean, but instead a method).

# In[74]:

chlorides_mean = red_df['chlorides'].mean()
red_df.query('chlorides < @chlorides_mean')


# #### 6. Grab all those rows where the `pH` is greater than 3.0 and less than 3.5.

# In[79]:


red_df.query('3.0 < pH < 3.5')


# #### 7. Further filter the results from 6 to grab only those rows that have a `residual sugar` less than 2.0.

# In[93]:


red_df = red_df.rename(columns={'residual sugar': 'residual_sugar'})
red_df.columns.values


# In[95]:


red_df.query('3.0 < pH < 3.5 and residual_sugar  < 2.0')


# ### Part 3 - More Practice
#
# Let's move on to some more complicated things. Use your knowledge of `groupby`s, `sorting`, and the other things that you learned in lecture to answer the following.
#
# 1. Get the average amount of `chlorides` for each `quality` value.

# In[99]:


red_df.groupby('chlorides')
red_df.groupby('quality').mean()['chlorides']

# 2 - For observations with a `pH` greater than 3.0 and less than 4.0, find the average `alcohol` value by `pH`.
red_df.query('3.0 < pH < 4.0').groupby('pH').mean()
red_df.query('pH == 3.01')

# 3 -  For observations with an `alcohol` value between 9.25 and 9.5, find the highest amount of `residual sugar`.
red_df = red_df.rename(columns={'residual sugar': 'residual_sugar'})
red_df.query('9.25 < alcohol < 9.5').nlargest(1, 'residual_sugar')

# 4 - Create a new column, called `total_acidity`, that is the sum of `fixed acidity` and `volatile acidity`.
red_df.columns = map(lambda string: string.replace(' ', '_'), red_df.columns)
red_df['total_acidity'] = red_df.apply(lambda row: row['fixed_acidity'] + row['volatile_acidity'], axis=1)
red_df.head()

# 5 -  Find the average `total_acidity` for each of the `quality` values.
red_df[['quality', 'total_acidity']].groupby('quality').mean()

# 6 - Find the top 5 `density` values.
red_df.sort_values('density', ascending=False)[['density']].head(5)

# 7 - Find the 10 lowest `sulphates` values.
red_df.sort_values('sulphates')[['sulphates']].head(10)
#
# ### Part 4 - Practice with Plotting
#
# %%
# 1. Plot the average amount of `chlorides` for each `quality` value (1 from Part 3).
import matplotlib.pyplot as plt

red_df.groupby('chlorides')
red_df.groupby('quality').mean()['chlorides'].plot(kind='bar')
plt.show()

# %%
# 2. Plot the `alcohol` values against `pH` values. Does there appear to be any relationship between the two?
red_df.plot(x='alcohol', y='pH', kind='line')
plt.show()

# %%
# 3. Plot `total_acidity` values against `pH` values. Does there appear to be any relationship between the two?
red_df.plot(x='total_acidity', y='pH', kind='line')
plt.show()
# yes ;

# %%
# 4. Plot a histogram of the `quality` values. Are they evenly distributed within the data set?
red_df[['quality']]
red_df[['quality']].plot(kind='hist')
plt.show()

# %%
# 5. Plot a boxplot to look at the distribution of `citric acid`.
red_df[['citric_acid']].plot(kind='box')
plt.show()

# ### Part 5 - Putting it All Together
#
# Now that you've worked on all the basics with one data set, it's time to do it with a second! This time, though, you'll go through the process of downloading the data set yourself. You'll also go through the process of learning to ask questions of the data (i.e. you won't be given any questions). We'll point you to a number of different data sets, and let you go at it. In reality, this is often how data science works. There isn't a clear-cut set of instructions on what to do - you kind of just dive into the data and see what you find!
#
# Your goal by the end of `Part 5` is to be able to tell a story with your data. Whether that means you query it and find something interesting, examine a number of different columns and their values, or plot a couple of different columns, it doesn't matter. You should aim to find at least one piece of interesting information in your data (and ideally even more than one). Then, tell your peers and the instructors what you've found!
#
# Potential data sources:
#
# 1. [Forest-fires](http://archive.ics.uci.edu/ml/datasets/Forest+Fires)
# 2. [Iris](http://archive.ics.uci.edu/ml/datasets/Iris)
# 3. [Another wine data set](http://archive.ics.uci.edu/ml/datasets/Wine)
# 4. [Abalone](http://archive.ics.uci.edu/ml/datasets/Abalone)
# 5. [Adult Income data set](http://archive.ics.uci.edu/ml/datasets/Adult)
#

# %%
# 5. [Adult Income data set](http://archive.ics.uci.edu/ml/datasets/Adult)
headers = ['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income']
income_df = pd.read_csv('./data/adult_income.csv', names=headers, sep=',')
correlation = income_df.corr()
# rm corr with self
np.fill_diagonal(correlation.values, 0)

fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(correlation, interpolation='nearest')
fig.colorbar(cax)

axis_labels = correlation.columns.values
ax.set_xticks(np.arange(len(axis_labels)))
ax.set_xticklabels(axis_labels, rotation=45, ha='right')
ax.set_yticks(np.arange(len(axis_labels)))
ax.set_yticklabels(axis_labels, rotation=45, ha='right')
plt.show()
correlation

# The links above are all to the home pages of these data sources. At the top of these pages, you will find a link the the `Data Folder` where you can actually find the data. The majority of these data sets don't come in `.csv` format. While one of the datasets is available in `.csv` format, we encourage you to pick whatever data set you find most interesting (regardless of the format), and challenge yourself to read the necessary documentation and go through the process of figuring out how to get the data from the web and into a `DataFrame` (the instructors will also be around to help).
