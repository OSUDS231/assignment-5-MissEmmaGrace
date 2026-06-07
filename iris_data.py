# Author: Emma Oliver
# GitHub username: MissEmmaGrace
# Date: 06/07/2026
# Description: This code reads a .txt file, parses each of the five values in each line into a dataframe, and computes the mean value of summary statistics from the dataframe

import pandas as pd

def parse_line(line):
    """
    Input: one string with 5 values (created specifically for the iris.txt dataset)
    Return: a list with the first four values as float values and the fifth value as a string value
    """
    #Removes newline character
    line = line.strip()
    #Splits string into list
    fields = line.split('|')
    fields[0] = float(fields[0])
    fields[1] = float(fields[1])
    fields[2] = float(fields[2])
    fields[3] = float(fields[3])
    return fields


def add_to_dict(parsed_line, data_dict):
    """
    Input: (1) parsed_line, a list with five values and (2) data_dict, a directory with five entries and lists as values
    Return: None. Instead, mutates data_dict by adding a value from parsed_line to the respective list entry in data_dict
    """
    #Makes sure the length of parsed_line is appropriate for the directory
    if len(parsed_line) != len(data_dict):
        raise ValueError("number of fields does not match dictionary keys.")
    #Adds values from parsed_line into the directory
    keys = list(data_dict.keys())
    count = 0
    for i in keys:
        data_dict[i].append(parsed_line[count])
        count += 1


def load_data(filename):
    """
    Input: a file
    Return: a dataframe with each line of the file parsed into 5 columns: sepal_length, sepal_width, petal_length, petal_width, and species
    """
    # Creates directory
    data_dict = {"sepal_length": [], "sepal_width": [], "petal_length": [], "petal_width": [], "species": []}
    with open(filename, "r") as file:
        for row in file:
            if len(row.strip()) != 0:
                parsed_line = parse_line(row)
                add_to_dict(parsed_line, data_dict)
        # Creates dataframe
        dataframe = pd.DataFrame(data_dict)
        return dataframe


def species_mean(data, species, measurement):
    """
    Input: (1) data, a dataframe, (2) species, a species name to filter by, and (3) measurement, a measurement to calculate the mean of
    Return: the mean of the measurement for the species specified
    """
    #Filters by species
    new_df = data[data["species"] == species]
    #Returns mean value of measurement
    return new_df[measurement].mean()

df = load_data('iris.txt')
print(species_mean(df, 'Iris-setosa', 'sepal_length'))