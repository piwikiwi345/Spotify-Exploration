# Spotify-Exploration
Hi! Welcome to my exploration of Spotify using Python, SQL, and Tableau to gather, analyze, and visualize insights from track data on the Spotify Weekly Charts.

Please feel free to use any code from this project for your own projects! The code is meant to be reusable and able to be implemented into your own projects. 

## Gathering Data through Spotify API

I used python to grab different 'Top Songs' playlists from Spotify using their API. Then, for each track inside each playlist, I grabbed relevant audio analysis, artist information, track information, and genre. This is all shown in the [Spotify API](Data%20Importing/Spotify%20API.ipynb) notebook.

## Handling Data with SQL

For each country's chart, I created a combined .csv file that holds all the information which was originally split between the following three different .csv files:

1. Audio Features
2. Genre
3. Artist & Track Information

I accomplished this by using JOINS in SQL and then exporting the combined tables as .csv files. You can see my process in the following markdown [file](Data%20Handling/SQL.md).

I then combined each country's combined tables into one master table that lives in [this](/Users/prithvivenkataswamy/Documents/Spotify-Exploration/data/master.csv) .csv file. You can see my process and code in the following jupyter [notebook](/Users/prithvivenkataswamy/Documents/Spotify-Exploration/Data Handling/handling.ipynb).

## Exploratory Analysis

### Python

The following jupyer [notebook](/Users/prithvivenkataswamy/Documents/Spotify-Exploration/Analysis/Analysis.ipynb) contains written analysis on descriptive statistics and graphics created using matplotlib and [Tableau](/Users/prithvivenkataswamy/Documents/Spotify-Exploration/Analysis/graphics).s

### Excel

I imported the 'master.csv' file I created into google sheets in order to create a pivot table and use Advanced Excel to answer some of my questions more easily.

The Pivot table was not as useful to me as I thought it would be, but it illuminated many descriptive statistics about the data which helped me frame my questions (and consqeuently my COUNTIFS and SUMIFS). Using medians, averages, and standard deviations, I could find trends in the data by answering my own questions.



