# Spotify Exploration Using SQL

In this markdown file, I have included the SQL code I used and my reasoning for using it. Included in this repository is the spotify [database](spotify.db) which holds the relevant data for this project. 


## Creating Tables & Importing Data

The following code is an example of how I imported the releveant .csv files into their corresponding tables. I then repeated this process for the rest of the .csv files for the different regional country charts.

```SQL
create table usa_track_and_artist_info (name TEXT, artist_id TEXT, track_id TEXT, track_name TEXT, popularity INTEGER);

.mode csv
.headers on

.import --skip 1 data/usa/top_songs_usa_track_and_artist_info.csv usa_track_and_artist_info
```

```SQL
create table usa_genres (artist_id TEXT, name TEXT, 'Genre 1' TEXT, 'Genre 2' TEXT, 'Genre 3' TEXT, 'Genre 4' TEXT, 'Genre 5' TEXT, 'Genre 6' TEXT);

.import --skip 1 data/usa/top_songs_usa_genres.csv usa_genres
```

```SQL
create table usa_audio_features (id TEXT, danceability FLOAT, energy FLOAT, key INTEGER, loudness FLOAT, mode INTEGER, speechiness FLOAT, acousticness FLOAT, instrumentalness FLOAT, liveness FLOAT, valence FLOAT, tempo FLOAT,duration_ms INTEGER,time_signature INTEGER);

.import --skip 1 data/usa/top_songs_usa_audio_features.csv usa_audio_features
```

While I have traditionally used the terminal to run SQL code through sqlite3, for the majority of the SQL code in this project, I actually ended up using SQLiteStudio as its GUI makes creating tables, importing data, and querying much more enjoyable. :)


## Queries

I ran some initial queries to answer some initial questions I had about the charts.

What artists have multiple songs in the top 50 USA charts? How many songs do they have?

```SQL
SELECT name, COUNT(*) 
FROM usa_track_and_artist_info 
GROUP BY name
ORDER BY COUNT(*) desc;
```

Taylor Swift	6
Morgan Wallen	4
SZA	2
Post Malone	2
Peso Pluma	2
Fuerza Regida	2
Drake	2

What are the most danceable tracks in the top 50 USA charts?

```SQL
SELECT name, track_name
FROM usa_track_and_artist_info
JOIN usa_track_and_artist_info ON usa_track_and_artist_info.track_id = usa_audio_features.id
ORDER BY usa_audio_features.danceability DESC;
```

What are the most common genres in the top 50 USA charts?

```SQL
SELECT genre, COUNT(*) AS genre_count
FROM (
    SELECT 'Genre 1' AS genre FROM songs
    UNION ALL
    SELECT 'Genre 2' AS genre FROM songs
    UNION ALL
    SELECT 'Genre 3' AS genre FROM songs
    UNION ALL
    SELECT 'Genre 4' AS genre FROM songs
    UNION ALL
    SELECT 'Genre 5' AS genre FROM songs
    UNION ALL
    SELECT 'Genre 6' AS genre FROM songs
) AS combined_genres
GROUP BY genre
ORDER BY genre_count DESC;
```

## Combining and Exporting CSV files using JOINS

While I could have joined the original pandas dataframes in my jupyter notebooks, I wanted to showcase my knowledge on JOINS to combine the .csv files for each region and export them so I could use them for analysis as shown in this [notebook](Analysis.ipynb).

### Combined USA Table & Export

Create the combined table

```
CREATE TABLE usa AS
SELECT *
FROM usa_track_and_artist_info
JOIN usa_audio_features ON usa_track_and_artist_info.track_id = usa_audio_features.id
JOIN usa_genres ON usa_track_and_artist_info.artist_id = usa_genres.artist_id;
```

Drop duplicate columns

```SQL
ALTER TABLE usa
DROP COLUMN 'artist_id:1';

ALTER TABLE usa
DROP COLUMN 'name:1';
```

Export 'usa' table

```SQL
.mode csv
.output data/usa/usa.csv
SELECT * FROM usa
```

