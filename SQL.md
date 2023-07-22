# Spotify Exploration Using SQL

In this markdown file, I have included the SQL code I used and my reasoning for using it. All SQL code was inputted into sqlite3 run through the terminal. Included in this repository is the spotify [database](spotify.db) which holds the relevant data for this project. 

# Creating Tables & Importing Data

```SQL
create table usa_track_and_artist_info (name TEXT, artist_id TEXT, track_id TEXT, track_name TEXT)

.import data\\top_songs_usa_track_and_artist_info.csv usa_track_and_artist_info
```



