
import csv
from typing import final

# Prep --
# List of files to be used.
files_list = ["1 peak.csv", "2 peak.csv"]

# The columns to be used (0 based).
link_column = 5
population_column = 7
province_id_column = 5
urbanization_column = 10
cases_column = 20

percentage_of_change_in_cases = {}
combined_data = {}

top_30_UGroup_results = {"UGroup 1": 0, "UGroup 2": 0, "UGroup 3": 0}
bottom_30_UGroup_results = {"UGroup 1": 0, "UGroup 2": 0, "UGroup 3": 0}

top_30_PGroup_results = {"PGroup 1": 0, "PGroup 2": 0, "PGroup 3": 0}
bottom_30_PGroup_results = {"PGroup 1": 0, "PGroup 2": 0, "PGroup 3": 0}

# Population brackets are "Group 1" = Above Average, "Group 2" = In Average Range, "Group 3" = Below Average
population_brackets = {"PGroup 1": [], "PGroup 2": [], "PGroup 3": []}
population_range_threshold = 0.5

# Urbanization brackets
urbanization_brackets = {"UGroup 1": [], "UGroup 2": [], "UGroup 3": []}
urbanization_range_threshold = 0.5

# Holds consistent entries present in all files, after cleaning.
consistent_entries_list = []

# Prep //

# Function that cleans each file from rows with "0"s, and creates a new file with "_clean" extension.
def clean_data(file_name):

    file_reader = open(file_name, 'r')

    csv_reader = csv.reader(file_reader, delimiter=',')
    next(csv_reader)

    clean_data_list = []
    write_row = False

    for row in csv_reader:
        for cell in row:
            if cell == "0":
                write_row = False
                break
            else:
                write_row = True

        if write_row == True:
            clean_data_list.append(row)
    
    clean_file_name = file_name[:len(file_name) - 4] + "_clean.csv"
    csv_clean = open(clean_file_name, "w", newline='')
    writer = csv.writer(csv_clean)
    writer.writerows(clean_data_list)

# In case of multiple files, this function creates a list of entries by province codes and returns a list of consistent entries. 
def find_valid_entries(files_list):
    list_of_entries_per_file = []

    if len(files_list) > 1:
        for file in files_list:
            clean_file_name = file[:len(file) - 4] + "_clean.csv"
            file_reader = open(clean_file_name, "r")
            csv_reader = csv.reader(file_reader)

            current_file_entries = []
            for row in csv_reader:
                current_file_entries.append(row[link_column])
            list_of_entries_per_file.append(current_file_entries)
        
        current_list_id = 0
        while current_list_id < len(list_of_entries_per_file):
            for entry in list_of_entries_per_file[current_list_id]:
                loop_id = 0
                while current_list_id != loop_id and loop_id < len(list_of_entries_per_file):
                    if not any(entry in x for x in list_of_entries_per_file[loop_id]):
                        break
                    else:
                        consistent_entries_list.append(entry)
                    loop_id += 1

            current_list_id += 1

# Creates valid files with consistant entries.
def create_valid_data(files_list):
    if len(files_list) > 1:
        for file_name in files_list:
            clean_data = []
            clean_file_name = file_name[:len(file_name) - 4] + "_clean.csv"
            file_reader = open(clean_file_name, "r")
            csv_reader = csv.reader(file_reader)
            for row in csv_reader:
                if any(row[link_column] in x for x in consistent_entries_list):
                    clean_data.append(row)
            consice_file_name = clean_file_name[:len(file_name) - 4] + "_consice.csv"
            clean_file = open(consice_file_name, "w", newline='')
            writer = csv.writer(clean_file)
            writer.writerows(clean_data)

# General functions
def find_population_brackets(file_name, column_number):
    population_total = 0
    population_percentage = []

    file_reader = open(file_name, "r")
    csv_reader = csv.reader(file_reader)
    next(csv_reader)
    for row in csv_reader:
        population_total += int(row[column_number])
    
    file_reader = open(file_name, "r")
    csv_reader = csv.reader(file_reader)
    next(csv_reader)
    for row in csv_reader:
        population_percentage.append((float(row[column_number])/population_total) * 100)
    
    percentage_total = 0
    for entry in population_percentage:
        percentage_total += entry
    
    percentage_average = percentage_total/len(population_percentage)

    file_reader = open(file_name, "r")
    csv_reader = csv.reader(file_reader)
    next(csv_reader)
    for index, row in enumerate(csv_reader):
        if population_percentage[index] > percentage_average - population_range_threshold and population_percentage[index] < percentage_average + population_range_threshold:
            population_brackets["PGroup 2"].append(row[province_id_column])
        elif population_percentage[index] > percentage_average + population_range_threshold:
            population_brackets["PGroup 1"].append(row[province_id_column])
        elif population_percentage[index] < percentage_average - population_range_threshold:
            population_brackets["PGroup 3"].append(row[province_id_column])
    
    return population_brackets

def find_urbanization_brackets(file_name, column_number):
    urbanization_total = 0
    urbanization_percentage = []

    file_reader = open(file_name, "r")
    csv_reader = csv.reader(file_reader)
    next(csv_reader)
    for row in csv_reader:
        urbanization_total += float(row[column_number])
    
    file_reader = open(file_name, "r")
    csv_reader = csv.reader(file_reader)
    next(csv_reader)
    for row in csv_reader:
        urbanization_percentage.append((float(row[column_number])/urbanization_total) * 100)
    
    percentage_total = 0
    for entry in urbanization_percentage:
        percentage_total += entry
    
    percentage_average = percentage_total/len(urbanization_percentage)

    file_reader = open(file_name, "r")
    csv_reader = csv.reader(file_reader)
    next(csv_reader)
    for index, row in enumerate(csv_reader):
        if urbanization_percentage[index] > percentage_average - urbanization_range_threshold and urbanization_percentage[index] < percentage_average + urbanization_range_threshold:
            urbanization_brackets["UGroup 2"].append(row[province_id_column])
        elif urbanization_percentage[index] > percentage_average + urbanization_range_threshold:
            urbanization_brackets["UGroup 1"].append(row[province_id_column])
        elif urbanization_percentage[index] < percentage_average - urbanization_range_threshold:
            urbanization_brackets["UGroup 3"].append(row[province_id_column])

    return urbanization_brackets

# Creates a dictionary with percentage of change between peak 1 and peak 2.
def find_percentage_of_change_in_cases(files_list, cases_column):
    cases_and_provinces_first_peak = {}
    first_peak_provinces = []
    first_peak_cases = []
    cases_and_provinces_second_peak = {}
    second_peak_provinces = []
    second_peak_cases = []

    change_keys = []
    change_percentages = []

    file_reader = open(files_list[0], "r")
    csv_reader = csv.reader(file_reader)
    next(csv_reader)
    for row in csv_reader:
        first_peak_provinces.append(row[province_id_column])

    file_reader = open(files_list[0], "r")
    csv_reader = csv.reader(file_reader)
    next(csv_reader)
    for row in csv_reader:
        first_peak_cases.append(int(row[cases_column]))

    file_reader = open(files_list[1], "r")
    csv_reader = csv.reader(file_reader)
    next(csv_reader)
    for row in csv_reader:
        second_peak_provinces.append(row[province_id_column])

    file_reader = open(files_list[1], "r")
    csv_reader = csv.reader(file_reader)
    next(csv_reader)
    for row in csv_reader:
        second_peak_cases.append(int(row[cases_column]))
    
    cases_and_provinces_first_peak = dict(zip(first_peak_provinces, first_peak_cases))
    cases_and_provinces_second_peak = dict(zip(second_peak_provinces, second_peak_cases))

    for key in cases_and_provinces_first_peak:
        change_keys.append(key)
        change_percentages.append(((cases_and_provinces_second_peak[key]- cases_and_provinces_first_peak[key]) / cases_and_provinces_first_peak[key]) * 100)
    
    percentage_of_change_in_cases = dict(zip(change_keys, change_percentages))
    percentage_of_change_in_cases = {k: v for k, v in sorted(percentage_of_change_in_cases.items(), key=lambda item: item[1], reverse=True)}

    return percentage_of_change_in_cases

# Creates a dictionary with combined data of percentage change in cases with Urbanization and Population brackets.
def create_combined_data_for_provinces():
    combined_data = percentage_of_change_in_cases
    for key in combined_data:
        urbanization_group = 0
        population_group = 0

        for list in urbanization_brackets:
            if any(key in x for x in urbanization_brackets[list]):
                urbanization_group = list
        
        for list in population_brackets:
            if any(key in x for x in population_brackets[list]):
                population_group = list
        
        combined_data[key] = [percentage_of_change_in_cases[key], urbanization_group, population_group]

    return combined_data


# Execution order
# 1. Loops through all files in the list of files and cleans them.
#for file in files_list:
#    clean_data(file)

# 2. Return consistant entries across files.
#find_valid_entries(files_list)

# 3. Create files with consistant entries.
#create_valid_data(files_list)


# Execution without cleaning
population_brackets = find_population_brackets(files_list[0], population_column)

urbanization_brackets = find_urbanization_brackets(files_list[0], urbanization_column)

percentage_of_change_in_cases = find_percentage_of_change_in_cases(files_list, cases_column)

combined_data = create_combined_data_for_provinces()

i = 0
for entry in combined_data:
    if i == 30:
        break
    if combined_data[entry][1] == "UGroup 1":
        top_30_UGroup_results["UGroup 1"] += 1
    elif combined_data[entry][1] == "UGroup 2":
        top_30_UGroup_results["UGroup 2"] += 1
    elif combined_data[entry][1] == "UGroup 3":
        top_30_UGroup_results["UGroup 3"] += 1
    i += 1

i = len(combined_data) - 31
for index, entry in enumerate(combined_data):
    if index > i:
        if combined_data[entry][1] == "UGroup 1":
            bottom_30_UGroup_results["UGroup 1"] += 1
        elif combined_data[entry][1] == "UGroup 2":
            bottom_30_UGroup_results["UGroup 2"] += 1
        elif combined_data[entry][1] == "UGroup 3":
            bottom_30_UGroup_results["UGroup 3"] += 1

i = 0
for entry in combined_data:
    if i == 30:
        break
    if combined_data[entry][2] == "PGroup 1":
        top_30_PGroup_results["PGroup 1"] += 1
    elif combined_data[entry][2] == "PGroup 2":
        top_30_PGroup_results["PGroup 2"] += 1
    elif combined_data[entry][2] == "PGroup 3":
        top_30_PGroup_results["PGroup 3"] += 1
    i += 1

i = len(combined_data) - 31
for index, entry in enumerate(combined_data):
    if index > i:
        if combined_data[entry][2] == "PGroup 1":
            bottom_30_PGroup_results["PGroup 1"] += 1
        elif combined_data[entry][2] == "PGroup 2":
            bottom_30_PGroup_results["PGroup 2"] += 1
        elif combined_data[entry][2] == "PGroup 3":
            bottom_30_PGroup_results["PGroup 3"] += 1



# Writes the combined list of data for each province.
consice_file_name = "combined_data.csv"
clean_file = open(consice_file_name, "w", newline='')
writer = csv.writer(clean_file)

final_data = []
for key in combined_data:
    prep_data = []
    prep_data.append(key)
    for item in combined_data[key]:
        prep_data.append(item)
    final_data.append(prep_data)
writer.writerow(['Province Name', "Percentage Increase", "Urbanization Group", "Population Group"])
writer.writerows(final_data)


print("")
print("Top 30 COVID cases Urbanization brackets:    {}".format(top_30_UGroup_results))
print("Bottom 30 COVID cases Urbanization brackets: {}".format(bottom_30_UGroup_results))
print("")
print("Top 30 COVID cases Population brackets:      {}".format(top_30_PGroup_results))
print("Bottom 30 COVID cases Population brackets:   {}".format(bottom_30_PGroup_results))
print("")
