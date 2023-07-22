# Spotify Exploration Using SQL

In this markdown file, I have included the SQL code I used and my reasoning for using it. All SQL code was inputted into sqlite3 run through the terminal. Included in this repository is the spotify [database](spotify.db) which holds the relevant data for this project. 

## Creating Tables & Importing Data

The following code is an example of how I imported the releveant .csv files into their corresponding tables. I then repeated this process for the rest of the .csv files for the different regional country charts.

```SQL
create table usa_track_and_artist_info (name TEXT, artist_id TEXT, track_id TEXT, track_name TEXT)

.mode csv

.import data/top_songs_usa_track_and_artist_info.csv usa_track_and_artist_info
```

```SQL
create table usa_genres (artist_id TEXT, name TEXT, 'Genre 1' TEXT, 'Genre 2' TEXT, 'Genre 3' TEXT, 'Genre 4' TEXT, 'Genre 5' TEXT, 'Genre 6' TEXT);

.import data/top_songs_usa_genres.csv usa_genres
```

While I have traditionally used the terminal to run SQL code through sqlite3, for the majority of the SQL code in this project, I actually ended up using SQLiteStudio as its GUI makes creating tables, importing data, and querying much more enjoyable. :)

## Queries

I conducted some initial queries to 

## Combining and Exporting CSV files using JOINS

While I could have joined the original pandas dataframes in my jupyter notebooks, I wanted to showcase my knowledge on JOINS to combine the .csv files for each region and export them so I could use them for analysis as shown in this [notebook](Analysis.ipynb).



