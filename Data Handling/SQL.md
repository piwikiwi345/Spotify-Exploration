# Data Handling Using SQL

In this markdown file, I have included the SQL code I used to handle the raw .csv files I imported from the Spotify API. Included in this repository is my own Spotify [database](spotify.db) which holds the relevant data for this project. 



## Creating Tables & Importing Data

The following code is an example of how I imported the releveant .csv files into their corresponding tables. I then repeated this process for the rest of the .csv files for the other country charts.

```SQL
create table thailand_track_and_artist_info (name TEXT, artist_id TEXT, track_id TEXT, track_name TEXT, popularity INTEGER);

.mode csv
.headers on

.import --skip 1 /Users/prithvivenkataswamy/Documents/Spotify-Exploration/data/thailand/top_songs_thailand_track_and_artist_info.csv thailand_track_and_artist_info
```

```SQL
create table thailand_genres (artist_id TEXT, name TEXT, 'Genre 1' TEXT, 'Genre 2' TEXT, 'Genre 3' TEXT, 'Genre 4' TEXT, 'Genre 5' TEXT, 'Genre 6' TEXT);

.import --skip 1 /Users/prithvivenkataswamy/Documents/Spotify-Exploration/data/thailand/top_songs_thailand_genres.csv thailand_genres
```

```SQL
create table thailand_audio_features (id TEXT, danceability FLOAT, energy FLOAT, key INTEGER, loudness FLOAT, mode INTEGER, speechiness FLOAT, acousticness FLOAT, instrumentalness FLOAT, liveness FLOAT, valence FLOAT, tempo FLOAT,duration_ms INTEGER,time_signature INTEGER);

.import --skip 1 /Users/prithvivenkataswamy/Documents/Spotify-Exploration/data/thailand/top_songs_thailand_audio_features.csv thailand_audio_features
```

While I have traditionally used the terminal to run SQL code through sqlite3, for the majority of the SQL code in this project, I actually ended up using SQLiteStudio; its GUI makes creating tables, importing data, and querying much more enjoyable. :)



## Combining and Exporting CSV files using JOINS

While I could have joined the original pandas dataframes in my jupyter notebooks, I wanted to showcase my knowledge on SQL joins to combine the .csv files for each region and export them so I could use them for analysis as shown in this [notebook](Analysis.ipynb).

### Combined USA Table & Export

Create the combined table

```
CREATE TABLE usa AS
SELECT DISTINCT *
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


## Queries

I ran some queries to answer some initial questions I had about the charts.

### What artists have multiple songs in the top 50 USA charts? How many songs do they have?

```SQL
SELECT name, COUNT(*) as songs
FROM usa_track_and_artist_info 
GROUP BY name
ORDER BY COUNT(*) desc;
```
<br>

| name            |songs|
|-----------------|-----|
| Taylor Swift    |  6  |
| Morgan Wallen   |  4  |
| SZA             |  2  |
| Post Malone	  |  2  | 
| Peso Pluma	  |  2  |
| Fuerza Regida	  |  2  |  
| Drake	          |  2  |
<br>
<br>

### What are the most danceable tracks in the top 50 USA charts?

```SQL
SELECT track_name, name, danceability
FROM usa
ORDER BY danceability DESC;
```
<br>

| track_name                          | name         | danceability |
|-------------------------------------|--------------|--------------|
| Peso Pluma: Bzrp Music Sessions, Vol. 55   | Bizarrap     | 0.854 |
| fukumean                           | Gunna        | 0.847        |
| Search & Rescue                    | Drake        | 0.817        |
| La Bebe (Remix)                    | Yng Lvcas    | 0.812        |
| Seven (feat. Latto)                | Jung Kook    | 0.802        |
| Calm Down                          | Rema         | 0.799        |
| All My Life (feat. J. Cole)        | Lil Durk     | 0.787        |
| TQM                                 | Fuerza Regida| 0.786        |
| SABOR FRESA                        | Fuerza Regida| 0.785        |
| Cupid - Twin Ver.                  | FIFTY FIFTY  | 0.783        |
<br>
<br>

### What is the average popularity for the top 50 Hong Kong charts?

```SQL
SELECT AVG(popularity)
FROM hong_kong;
```
<br>
The average popularity is 73.22
<br>
<br>

### What songs on the top 50 India charts come from the film "Kabir Singh"?

```SQL
SELECT track_name as "Track Name", name as "Name"
FROM india
WHERE track_name LIKE "%KABIR SINGH%";
```
<br>

| Track Name | Name |
|------------|------|
| Tujhe Kitna Chahne Lage (From "Kabir Singh") | Arijit Singh |
| Kaise Hua (From "Kabir Singh") | Vishal Mishra |
<br>
<br>

### Grab descriptive statistics for popularity for the top 50 Mexico chart.

```SQL
SELECT
    (SELECT MAX(popularity) FROM mexico) AS Maximum,
    (SELECT MIN(popularity) FROM mexico) AS Minimum,
    (SELECT AVG(popularity) FROM mexico) AS Mean,
    SQRT(SUM(power_diff_sq) / (COUNT(*) - 1)) AS "Std. Dev"
FROM (
    SELECT POWER(popularity - AVG(popularity) OVER(), 2) AS power_diff_sq
    FROM mexico
) AS subquery;
```
<br>

| Maximum | Minimum | Mean | Std. Dev |
|---------|---------|------|----------|
| 99 | 48	| 87.86	| 8.86867912305745|
<br>
<br>
