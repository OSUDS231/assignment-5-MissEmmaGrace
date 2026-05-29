# DS231 Assignment 5

## Overview and Objectives

In this assignment, you will build a data loading pipeline for the Iris dataset — a structured program that reads a raw text file, parses its contents line by line, organizes the data into a dictionary, and assembles it into a pandas DataFrame for analysis. The primary goal is to practice file handling in Python and to understand how raw data can be progressively structured into a format suitable for computation.

## Instructions

1. All your code goes into `iris_data.py`, the starter file provided. You do not need to create any new Python files. The functions you need to implement are: `parse_line()`, `add_to_dict()`, `load_data()`, and `species_mean()`.

2. Ensure that your program runs without errors. If your code fails to execute due to a syntax error or uncaught exception at import time, a flat **20% point deduction** will be applied, regardless of the nature of the error.

3. All functions in this assignment are graded on their **return values**, with the exception of `add_to_dict()`, which is graded on the **state of the dictionary** after it runs and the **message it prints** when an error is detected. Each task description will make clear which grading basis applies.

4. To be eligible for partial credit on select functions, use the intermediate variable names specified in each task's ***Function specification*** section.

5. `import pandas as pd` is already included at the top of `iris_data.py` — do not remove or modify this line.


## The Iris Dataset

The Iris dataset contains measurements of 150 flowers from three species: *Iris setosa*, *Iris versicolor*, and *Iris virginica*. Each flower is described by four numerical measurements and a species label.

Rather than providing the data as a `.csv` file, this assignment stores it in a plain text file — `iris.txt` — where the five values on each line are separated by a pipe character (`|`). A few example lines from the file are shown below.

```text
5.1|3.5|1.4|0.2|Iris-setosa
6.4|3.2|4.5|1.5|Iris-versicolor
7.2|3.6|6.1|2.5|Iris-virginica
```

Each line contains five fields in the following order:

| Column | Type | Description |
|---|---|---|
| `sepal_length` | float | Length of the sepal in cm |
| `sepal_width` | float | Width of the sepal in cm |
| `petal_length` | float | Length of the petal in cm |
| `petal_width` | float | Width of the petal in cm |
| `species` | str | Species name |

Your job is to write the functions that parse this file, populate a dictionary, assemble a DataFrame, and query it by species.


## Part 1. Building the Data Pipeline [75 Points]

This part asks you to implement three functions that together form a data loading pipeline. Here is a summary of all three functions for reference:

- `parse_line(line)` — takes one raw line of text from `iris.txt` and returns a list of its five parsed values.
- `add_to_dict(parsed_line, data_dict)` — inserts a parsed row of values into a dictionary that stores each column as a list.
- `load_data(filename)` — reads every line from the file, builds and fills the dictionary using the two functions above, and returns the result as a pandas DataFrame.

### Task 1.1 — Parse a Line [20 Points]

**`parse_line(line)`** takes a single raw line of text from `iris.txt` and returns a list of its five values with the correct types.

1. Strip any leading or trailing whitespace from `line` — this handles the newline character `\n` present at the end of each line.
2. Split the cleaned string on the `|` separator. Store the result in a variable named `fields`.
3. Convert the first four elements of `fields` to `float`. Leave the fifth element (the species name) as a string.
4. Return the resulting list.

***Function specification.***
- Input: `line` (str) — one raw line from `iris.txt`
- Return: a list of five elements — four `float` measurements followed by one `str` species name (list)
- Intermediate variable for partial credit: `fields` — the list of strings produced by splitting on `|`, before any type conversion [10 pts]

***Function demonstration.***

```python
>>> parse_line("5.1|3.5|1.4|0.2|Iris-setosa\n")
[5.1, 3.5, 1.4, 0.2, 'Iris-setosa']

>>> parse_line("6.4|3.2|4.5|1.5|Iris-versicolor\n")
[6.4, 3.2, 4.5, 1.5, 'Iris-versicolor']
```

***Hint.***
- Use `str.strip()` to remove leading and trailing whitespace, including `\n`.
- Use `str.split(separator)` to split a string on a given character.
- Use `float()` to convert a string to a floating-point number.
- Use indexing to access individual elements of `fields`.


### Task 1.2 — Add a Row to the Dictionary [25 Points]

**`add_to_dict(parsed_line, data_dict)`** inserts one parsed row of data into a dictionary where each key is a column name and each value is a list accumulating that column's entries.

1. Check whether the number of elements in `parsed_line` matches the number of keys in `data_dict`. If they do not match, raise `ValueError("number of fields does not match dictionary keys.")`. A Traceback message may be displayed above the error line — this is acceptable.
2. If the lengths match, append each element of `parsed_line` to the corresponding list in `data_dict`, in the same order as the keys.

***Function specification.***
- Input: `parsed_line` (list), `data_dict` (dict) — keys are column name strings, values are lists
- Return: `None` (the dictionary is modified in place)
- Raises: `ValueError` if the number of elements in `parsed_line` does not match the number of keys in `data_dict`
- Graded on: the state of `data_dict` after the call, and the error raised when a mismatch is detected

***Function demonstration.*** A Traceback message may be displayed above the error line — this is acceptable.

```python
>>> d = {"sepal_length": [], "sepal_width": [], "petal_length": [], "petal_width": [], "species": []}
>>> add_to_dict([5.1, 3.5, 1.4, 0.2, "Iris-setosa"], d)
>>> d["sepal_length"]
[5.1]
>>> d["species"]
['Iris-setosa']

>>> add_to_dict([5.1, 3.5], d)
ValueError: number of fields does not match dictionary keys.
```

***Hint.***
- Use `len()` on both `parsed_line` and `data_dict` to compare their lengths.
- To append values in order, use `list(data_dict.keys())` to get the keys as a list, then loop through the indices, using each index to access both the key in `data_dict` and the corresponding value in `parsed_line`.


### Task 1.3 — Load the Full Dataset [30 Points]

**`load_data(filename)`** reads `iris.txt` from start to finish, builds the data dictionary, and returns the result as a pandas DataFrame.

1. Create a dictionary named `data_dict` with the five column names as keys and empty lists as values: `sepal_length`, `sepal_width`, `petal_length`, `petal_width`, `species`.
2. Open `filename` for reading and iterate over its lines. For each line, call `parse_line()` to get the parsed values, then call `add_to_dict()` to insert them into `data_dict`.
3. Convert `data_dict` to a `pd.DataFrame` and return it.

***Function specification.***
- Input: `filename` (str) — path to the data file
- Return: a pandas DataFrame with 150 rows and 5 columns (DataFrame)
- Intermediate variable for partial credit: `data_dict` — [5 pts] if it contains the correct five column names as keys, regardless of their values; [additional 15 pts] if each list in `data_dict` has the correct length (150 entries)

***Function demonstration.***

```python
>>> df = load_data("iris.txt")
>>> df.shape
(150, 5)
>>> list(df.columns)
['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']
>>> df.head(2)
   sepal_length  sepal_width  petal_length  petal_width      species
0           5.1          3.5           1.4          0.2  Iris-setosa
1           4.9          3.0           1.4          0.2  Iris-setosa
```

***Hint.***
- Use `open(filename, "r")` to open the file and a `for` loop to iterate over its lines.
- The file may contain empty lines at the end. Before processing each line, check whether it is empty after stripping — if so, skip it.
- To convert the completed dictionary to a DataFrame, use `pd.DataFrame(data_dict)`.


## Part 2. Querying the Data [25 Points]

With the data loaded as a DataFrame, you can now write a function to extract summary statistics by species.

### Task 2.1 — Species-Wise Mean [25 Points]

**`species_mean(data, species, measurement)`** returns the average value of one measurement across all flowers belonging to a given species. You may assume that both `species` and `measurement` are valid values present in the DataFrame.

1. Filter `data` to keep only the rows where the `species` column equals the `species` argument.
2. From those filtered rows, select the column named `measurement`.
3. Compute and return the mean of that column.

***Function specification.***
- Input: `data` (DataFrame), `species` (str), `measurement` (str)
- Return: the mean value of the specified measurement for the specified species (float or np.float64)

***Function demonstration.***

```python
>>> df = load_data("iris.txt")
>>> species_mean(df, "Iris-setosa", "sepal_length")
5.006
>>> species_mean(df, "Iris-versicolor", "petal_length")
4.26
>>> species_mean(df, "Iris-virginica", "petal_width")
2.026
```

***Hint.***
- pandas supports boolean indexing: you can filter a DataFrame to only rows that match a condition by passing a boolean expression inside square brackets.
- Once you have the filtered rows, select a single column by name and call `.mean()` on it.
