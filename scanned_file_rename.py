# This script is originally written to rename files to a specific format specified by my supervisor
# The database is directly acquired from company's Excel sheets and will thus NOT be included here
# This is a personal script with the assumption that the user (me) will not enter the wrong inputs
# and thus does NOT do any input sanitization checks beyond filtering between ID search and name search
# All company-related information and data have been removed from this file and set up as separate variables
import os
import csv

print("Loading CSV files...")

input_file_name_format = "FORMAT"
filenames = []
# The row number of each file must correspond to the order of the filenames
emp_id_row_num = [] # CHECK
emp_name_row_num = [] # CHECK
filter_words = [] # Add each word that you want filtered out of the employee name for data sanitization purpose

employees = dict()
for filename in filenames:
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            employee_name = row[emp_name_row_num[filenames.index(filename)]].split(' ')
            employee_id = 0
            # Removing words from the employee name that would directly conflict with Windows file naming rules
            for word in filter_words:
                try:
                    employee_name.remove(word)
                except ValueError:
                    pass
            try:
                employee_id = int(row[emp_id_row_num[filenames.index(filename)]])
                # To deal with multiple files having potential overlaps
                if employee_id in employees:
                    pass
            except ValueError:
                pass # This implies the employee in question does NOT exit, hence skipping
                
            # Sanitizing the employee name through removing weird UTF-8 characters by encoding in, and
            # decoding back to, ASCII while skipping characters that can't be converted
            employees[employee_id] = ' '.join(employee_name).encode('ascii', 'ignore').decode('ascii')

print("Loading CSV files done!")
print("PLEASE SET CHROME OR ANY WEB BROWSERS AS THE DEFAULT APP FOR PDF FILES BEFORE CONTINUING.")
print("Once done, press enter to continue.")
input()

files = [a for a in os.listdir() if input_file_name_format in a]

print(f"FOUND {len(files)} FILES.")

for file in files:
    os.startfile(file)
    print(f"--- FILE '{file}' OPENED ---")
    print("Enter employee ID OR partial name: ", end="")
    # Implementing both employee ID and case-insensitive partial name search using exception handling
    emp_id = int()
    user_input = str()
    try:
        user_input = input()
        emp_id = int(user_input)
    except ValueError:
        for k, v in employees.items():
            if user_input.lower() in v.lower():
                emp_id = k
                
    if not employees[emp_id]: # Empty string is falsey value; essentially checking if the associated name is empty
        print("EMPLOYEE ID DOES NOT HAVE AN ASSOCIATED NAME, please type their name manually.")
        employees[emp_id] = input("Enter name here: ")
        
    name = f"{'_'.join(employees[emp_id].split(' '))}_{emp_id}.pdf"
    os.rename(file, name)
    print(f"RENAMED {file} TO {name}")
    
print("----------\nAll files renamed.")
