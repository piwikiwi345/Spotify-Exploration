'''
This script contains functions that are used in the jupyter notebook located in its home folder.
'''

import sqlite3
import csv

def create_table_track_and_artist_info(country, db_path):
    '''
    This function creates an SQL table in a SQL database
    
    country: a string containing the name of a country
    
    '''
    
    try:
        # Connect to the database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Create the table using the table_name parameter
        create_table_query = f'''
            create table {country}_track_and_artist_info (
                name TEXT, 
                artist_id TEXT, 
                track_id TEXT, 
                track_name TEXT, 
                popularity INTEGER
            )
        '''
        cursor.execute(create_table_query)

        connection.commit()

    except sqlite3.Error as e:
        print(f"Error: {e}")

    finally:
        # Close the database connection when done
        if connection:
            connection.close()

def create_SQL_commands(country):
    print(f'''create table {country}_track_and_artist_info (
          name TEXT, 
          artist_id TEXT, 
          track_id TEXT, 
          track_name TEXT, 
          popularity INTEGER);''')
          
    print(f'''.import --skip 1 /Users/prithvivenkataswamy/Documents/Spotify-Exploration/data/{country}/top_songs_{country}_track_and_artist_info.csv {country}_track_and_artist_info
    ''')
          
    print(f'''
        create table {country}_genres (artist_id TEXT, name TEXT, 'Genre 1' TEXT, 'Genre 2' TEXT, 'Genre 3' TEXT, 'Genre 4' TEXT, 'Genre 5' TEXT, 'Genre 6' TEXT);
    ''')
          
    print(f'''
    .import --skip 1 /Users/prithvivenkataswamy/Documents/Spotify-Exploration/data/{country}/top_songs_{country}_genres.csv {country}_genres
    ''')
          
    print(f'''
    create table {country}_audio_features (id TEXT, danceability FLOAT, energy FLOAT, key INTEGER, loudness FLOAT, mode INTEGER, speechiness FLOAT, acousticness FLOAT, instrumentalness FLOAT, liveness FLOAT, valence FLOAT, tempo FLOAT,duration_ms INTEGER,time_signature INTEGER);
    ''')
          
    print(f'''
    .import --skip 1 /Users/prithvivenkataswamy/Documents/Spotify-Exploration/data/{country}/top_songs_{country}_audio_features.csv {country}_audio_features
    ''')

def combine_tables(country, db_path):
    '''
    This function joins three specific tables into one.
    
    country: a string containing the name of a country
    db_path: a string containing the database local path
    '''
    # Replace 'your_database.db' with the path to your SQLite database file.
    

    try:
        # Connect to the database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Create the table using the table_name parameter
        create_table_query = f'''
            CREATE TABLE {country} AS
            SELECT DISTINCT *
            FROM {country}_track_and_artist_info
            JOIN {country}_audio_features ON {country}_track_and_artist_info.track_id = {country}_audio_features.id
            JOIN {country}_genres ON {country}_track_and_artist_info.artist_id = {country}_genres.artist_id;
        '''
        cursor.execute(create_table_query)

        connection.commit()

        rows = cursor.fetchall()

        # Replace 'exported_table.csv' with the desired CSV file name
        csv_file = f'{country}.csv'

        # Write the data to the CSV file
        with open(csv_file, 'w', newline='') as file:
            csv_writer = csv.writer(file)

            # Write the column headers as the first row in the CSV file
            column_names = [description[0] for description in cursor.description]
            csv_writer.writerow(column_names)

            # Write the data rows to the CSV file
            csv_writer.writerows(rows)

    except sqlite3.Error as e:
        print(f"Error: {e}")

    finally:
        # Close the database connection when done
        if connection:
            connection.close()

