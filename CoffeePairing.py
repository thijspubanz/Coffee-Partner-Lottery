import pandas as pd
import csv
import random
import copy
import os
from dotenv import load_dotenv
from form_api import export_form_data_to_csv
from conversation_starters import get_random_conversation_starter

# Load environmental variables
load_dotenv()

# path to the CSV files with participant data
participants_csv = "Coffee Partner Lottery participants.csv"

# header names in the CSV file (name and e-mail of participants)
header_name = "Name"
header_email = "Email"

# Write answers to csv in the right format
export_form_data_to_csv(header_name, header_email)

# path to TXT file that stores the pairings of this round
new_groups_txt = "Coffee Partner Lottery new groups.txt"

# path to CSV file that stores the pairings of this round
new_groups_csv = "Coffee Partner Lottery new groups.csv"

# path to CSV file that stores all pairings (to avoid repetition)
all_groups_csv = "Coffee Partner Lottery all groups.csv"
        
# init set of old groups
ogroups = set()

DELIMITER=','

# load all previous pairings (to avoid redundancies)
if os.path.exists(all_groups_csv):
    with open(all_groups_csv, "r") as file:
        csvreader = csv.reader(file, delimiter=DELIMITER)
        for row in csvreader:
            group = []
            for i in range(0,len(row)):
                group.append(row[i])                        
            ogroups.add(tuple(group))

# load participant's data
formdata = pd.read_csv(participants_csv, sep=DELIMITER)

# create duplicate-free list of participants
participants = list(set(formdata[header_email]))

 # init set of new groups
ngroups = set()

# running set of participants
nparticipants = copy.deepcopy(participants)

# Ask the user to reset the csv file of all groups
reset_all_pairs = input("Do you want to reset the CSV file of all previous groups? (y/n): ")
if reset_all_pairs.lower() == "y":
    with open(all_groups_csv, "w") as file:
        file.write("")
    print("All groups CSV file reset.")
elif reset_all_pairs.lower() == "n":
    print("All groups CSV file not reset.")
else:
    print("Invalid input. All groups CSV file not reset. Exiting.")
    exit(1)

# Ask the user the desired group size (max = total participants - 2 such that there will always be a minimum of 2 groups)
group_size = input("Enter the desired group size: ")

# Try to convert input to integer, else set to default value of 2
try:
    group_size = int(group_size)
except ValueError:
    group_size = 2
    print(f"Invalid input. Set to default value of {group_size}.")

# Check if group size is too large or too small
if group_size > len(participants)-2:
    group_size = len(participants)-2
    print(f"Group size too large. Set to {group_size}.")
elif group_size < 2:
    group_size = 2
    print(f"Group size too small. Set to {group_size}.")
else:
    print(f"Group size set to {group_size}.")

# Boolean flag to check if new pairing has been found
new_groups_found = False

# try creating new pairing until successful
group_forming_failsafe_max = 1000
group_forming_failsafe_counter = 0
while not new_groups_found:
    # if group size doesn't fit to number of participants, create a group of the remaining participants and then make other groups
    remaining_participants = len(participants) % group_size
    if remaining_participants != 0:
        # Create list of participants for the remaining group
        plist = []
        for i in range(remaining_participants):
            p = random.choice(nparticipants)
            nparticipants.remove(p)
            plist.append(p)
            
        # Sort the list of participants alphabetically
        plist.sort()
                        
        # Add alphabetically sorted list to set of groups
        ngroups.add(tuple(plist))

  
    # while still participants left to pair...
    while len(nparticipants) > 0:
        # take group_size random participants from list of participants
        plist = []
        for i in range(group_size):
            p = random.choice(nparticipants)
            nparticipants.remove(p)
            plist.append(p)

        # Sort the list of participants alphabetically
        plist.sort()
                        
        # Add alphabetically sorted list to set of groups
        ngroups.add(tuple(plist))

 
    # check if all new groups are indeed new, else reset
    if ngroups.isdisjoint(ogroups):
        new_groups_found = True
    else:
        ngroups = set()
        nparticipants = copy.deepcopy(participants)
        group_forming_failsafe_counter += 1
        if group_forming_failsafe_counter > group_forming_failsafe_max:
            print(f"Failed to find new groups after {group_forming_failsafe_max} tries. Exiting.")
            exit(1)



# Ask the user for what type of conversation starter they want
print("\nWhat type of conversation starter would you like?")
print("1. Joke")
print("2. Question")
print("3. Debate topic")
print("4. Random (mix of all types)")
starter_choice = input("Enter your choice (1-4): ")

# Set conversation starter type based on user input
if starter_choice == "1":
    starter_type = "joke"
elif starter_choice == "2":
    starter_type = "question"
elif starter_choice == "3":
    starter_type = "debate"
else:
    starter_type = None  # Random selection

# Get a conversation starter
conversation_starter = get_random_conversation_starter(starter_type)

# assemble output for printout
output_string = ""

output_string += "------------------------\n"
output_string += "Today's coffee partners:\n"
output_string += "------------------------\n"

for group in ngroups:
    group = list(group)
    output_string += "* "
    for i in range(0,len(group)):
        name_email_group = f"{formdata[formdata[header_email] == group[i]].iloc[0][header_name]} ({group[i]})"
        if i < len(group)-1:
            output_string += name_email_group + ", "
        else:
            output_string += name_email_group + "\n"

# Add conversation starter to output
output_string += "\n------------------------\n"
output_string += "Conversation starter:\n"
output_string += "------------------------\n"
output_string += conversation_starter + "\n"
    
# write output to console
print(output_string)

# write output into text file for later use
with open(new_groups_txt, "wb") as file:
    file.write(output_string.encode("utf8"))

# write new groups into CSV file (for e.g. use in MailMerge)
with open(new_groups_csv, "w") as file:
    header = ["name1", "email1", "name2", "email2", "name3", "email3", "conversation_starter"]
    file.write(DELIMITER.join(header) + "\n")
    for group in ngroups:
        group = list(group)
        row_data = ""
        for i in range(0,len(group)):
            name_email_group = f"{formdata[formdata[header_email] == group[i]].iloc[0][header_name]}{DELIMITER} {group[i]}"
            if i < len(group)-1:
                row_data += name_email_group + DELIMITER + " "
            else:
                row_data += name_email_group
        
        # Add conversation starter to the row
        row_data += DELIMITER + " " + conversation_starter + "\n"
        file.write(row_data)
                
# append groups to history file
if os.path.exists(all_groups_csv):
    mode = "a"
else:
    mode = "w"

with open(all_groups_csv, mode) as file:
    for group in ngroups:
        group = list(group)
        for i in range(0,len(group)):
            if i < len(group)-1:
                file.write(group[i] + DELIMITER)
            else:
                file.write(group[i] + "\n")


             
# print finishing message
print()
print("Job done.")
