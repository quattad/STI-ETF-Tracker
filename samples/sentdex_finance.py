"""
Main script to obtain past year data on both the Straits Times Index (STI) and the Nikko AM ETF(N2I.SG)
Big thanks to:
https://jeffknupp.com/blog/2014/02/04/starting-a-python-project-the-right-way/
sentdex Google Finance Tutorial https://www.youtube.com/watch?v=2BrpKpWwT2A
"""

"""
Libraries to use
- numpy
- pandas
- matplotlib: to plot graphs
- BeautifulSoup: for web scraping
- scikit-learn / sklearn
"""
""" set starting and end-dates to pull"""
import datetime as dt
""" allows plotting of charts and graphs """
import matplotlib.pyplot as plt
""" allow styling of graphs """
from matplotlib import style
import pandas as pd
""" replaces pandas.data.io. allows retrieval of data as a pandas dataframe."""
import pandas_datareader.data as web

style.use('ggplot')

start = dt.datetime(2018, 10, 1)
end = dt.datetime(2018, 10, 30)

df_1 = web.DataReader('ES3.SI', 'yahoo', start, end)   # getting a dataframe. getting method from pandas_datareader.data
df_2 = web.DataReader('G3B.SI', 'yahoo', start, end)

""" Print out graphs. df.head() obtains first 5 rows of a df. df.tail() obtains last 5 rows of a df."""
# print(df_1.head())
# print(df_2.head())

""" Adj Close: split stock to make it more affordable to regular people e.g. """

""" to save data to CSV"""
# df.to_csv('filename.csv')

""" if CSV already available"""
# df = pd.read_csv('filename', parse_dates = True, index_col = 0)

""" plot the graphs. dataframe objects have plot attributes """
# df_1.plot()
# plt.show()

""" print dataframes"""
print(df_1)

""" to plot multiple plots, have multiple subplots. refer to them as ax"""
ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)

ax1.plot(df_1.index, df_1['High'])
ax1.plot(df_2.index, df_2['High'])

plt.xlabel('Date')
plt.ylabel('High')
plt.title('STI vs Nikko')
plt.show()