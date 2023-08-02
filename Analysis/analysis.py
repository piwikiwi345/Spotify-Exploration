'''
This script contains functions that are used in the jupyter notebook located in the same folder 'Analysis'
'''

import math
import matplotlib.pyplot as plt
import pandas as pd

def count_unique_genres(dataframe):
    '''
    This function counts the unique genres present in a given dataframe. It is currently setup to work with the 
    'genre' csv files in this project (Which contain a maximum of 6 genres for one song).
    '''
    # Create an empty dictionary to store genre counts
    genre_counts = {}
    
    # Get all the columns with genre information
    genre_columns = ["Genre 1", "Genre 2", "Genre 3", "Genre 4", "Genre 5", "Genre 6"]
    
    # Iterate through each row in the DataFrame
    for index, row in dataframe.iterrows():
        # Iterate through each genre column
        for column in genre_columns:
            genre = row[column]
            # If the genre is not empty, update the genre_counts dictionary
            if genre and genre != "":
                if genre in genre_counts:
                    genre_counts[genre] += 1
                else:
                    genre_counts[genre] = 1
    
    # Drop NaN item
    def is_nan(value):
        return isinstance(value, float) and math.isnan(value)
    
    for key in genre_counts.keys():
        if is_nan(key) == True:
            del genre_counts[key]
            break

    return genre_counts


def plot_bar_chart(data_dict, title=None, x_label=None, y_label=None, bar_width = 0.8):
    '''
    This function creates a bar chart.
    '''
    # Extract keys and values from the dictionary
    keys = list(data_dict.keys())
    values = list(data_dict.values())

    # Create a bar chart
    plt.figure(figsize=(12, 6))  # Increase the figure width as needed
    plt.bar(keys, values, width=bar_width)

    # Set the title and labels (if provided)
    if title:
        plt.title(title)
    if x_label:
        plt.xlabel(x_label)
    if y_label:
        plt.ylabel(y_label)

    # Rotate the x-axis labels if there are many bars to avoid overlap
    if len(keys) > 10:
        plt.xticks(rotation=90, ha='right')
        
    # Remove top and right spines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # Show the plot
    plt.tight_layout()
    plt.show()
    
def plot_histogram(data, column_name, bins=12, intervals=1, extremes=False):
    '''
    This function plots a histogram when given data.
    '''
    # Remove top and right spines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    
    # Only show min and max
    if extremes == True:
        min_value = data.min()
        max_value = data.max()
        plt.xticks([min_value, max_value])
    else:
        x_tick_positions = [i for i in range(0, bins, )]  
        plt.xticks(x_tick_positions)

    # Create the histogram
    plt.hist(data, bins)  # You can adjust the number of bins as per your preference
    plt.xlabel(column_name)
    plt.ylabel('Frequency')
    plt.title(f'Histogram of {column_name}')
    plt.show()
    
def milliseconds_to_minutes(milliseconds):
    seconds = milliseconds / 1000
    minutes = seconds / 60
    return minutes

def df_export_csv(df, filename):
    '''
    This function exports a dataframe as a .csv file with the name of the dataframe as the filename.
    
    df: a pandas dataframe
    '''
    
    # export dataframe to csv
    df.to_csv(f'{filename}.csv', sep = ',', index=False, encoding='utf-8')

def get_genre_counts(df, filepath, show_dict=True):
    '''
    This function takes a dataframe of spotify genre data and exports the unique genres and their counts as a .csv file
    at a designated location and with a given name

    It also prints the information if requested.

    df: a genre dataframe
    filepath: a string containing the filepath
    show_dict: a Boolean which determines whether the function will print  the unique genres and their counts
    '''

    unique_genres = count_unique_genres(df)
    
    
    genres = unique_genres.keys()
    genres = list(genres)
    counts = unique_genres.values()
    counts = list(counts)
    if show_dict == True:
        print(genres)
        print(counts)
    else:
        x = 5
    
    
    genre_counts = {
    'genres': genres,
    'count' : counts
}

    df = pd.DataFrame(genre_counts)

    df_export_csv(df, filepath)