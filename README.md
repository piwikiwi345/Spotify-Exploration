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

