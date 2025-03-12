import pandas as pd
import csv
import random
import copy
import os
import sys
import json
from dotenv import load_dotenv
from form_api import export_form_data_to_csv
from conversation_starters import get_random_conversation_starter
from instructions import get_setup_instructions, get_usage_instructions

# Load environmental variables
load_dotenv()

# Check for command line arguments
if len(sys.argv) > 1:
    if sys.argv[1] == "--help" or sys.argv[1] == "-h":
        print(get_setup_instructions())
        print(get_usage_instructions())
        sys.exit(0)
    elif sys.argv[1] == "--setup":
        print(get_setup_instructions())
        sys.exit(0)
    elif sys.argv[1] == "--usage":
        print(get_usage_instructions())
        sys.exit(0)

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

# Display instructions prompt
print("\nWelcome to CaféConnect!")
print("Need instructions? Type 'y' for yes, or any other key to continue.")
show_instructions = input("Show instructions? (y/n): ")
if show_instructions.lower() == 'y':
    print(get_setup_instructions())
    print(get_usage_instructions())
    print("\nPress Enter to continue with the program...")
    input()

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

# Check if participants CSV file exists
if not os.path.exists(participants_csv):
    print(f"\nERROR: Could not find '{participants_csv}'")
    print("Please make sure you've downloaded the participant responses as described in the setup instructions.")
    print("For instructions, run the program with '--setup' flag.")
    print("\nWould you like to see the setup instructions now? (y/n)")
    show_setup = input("> ")
    if show_setup.lower() == 'y':
        print(get_setup_instructions())
    sys.exit(1)

try:
    # load participant's data
    formdata = pd.read_csv(participants_csv, sep=DELIMITER)

    # Check if required columns exist
    if header_name not in formdata.columns or header_email not in formdata.columns:
        print(f"\nERROR: The CSV file does not contain the required columns ({header_name}, {header_email}).")
        print("Please ensure your form data is formatted correctly as described in the setup instructions.")
        sys.exit(1)

    # create duplicate-free list of participants
    participants = list(set(formdata[header_email]))

    print(f"\nSuccessfully loaded {len(participants)} participants.")
except Exception as e:
    print(f"\nERROR: Could not process '{participants_csv}': {str(e)}")
    print("Please ensure your CSV file is formatted correctly.")
    sys.exit(1)

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

# Load configuration from file if it exists
config = {
    "default_group_size": 2,
    "max_group_size": 10
}

if os.path.exists("config.json"):
    try:
        with open("config.json", "r") as config_file:
            loaded_config = json.load(config_file)
            config.update(loaded_config)
        print(f"Configuration loaded. Default group size: {config['default_group_size']}")
    except Exception as e:
        print(f"Error loading configuration file: {str(e)}")
        print("Using default configuration.")

# Ask the user the desired group size (max = total participants - 2 such that there will always be a minimum of 2 groups)
default_size = config["default_group_size"]
max_size = min(config["max_group_size"], len(participants)-2)
group_size = input(f"Enter the desired group size (default: {default_size}, max: {max_size}): ")

# Try to convert input to integer, else use default value from config
if not group_size:  # If user just pressed enter, use default
    group_size = default_size
    print(f"Using default group size: {group_size}")
else:
    try:
        group_size = int(group_size)
    except ValueError:
        group_size = default_size
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
    # If group size doesn't fit to number of participants, distribute them evenly
    # by making some groups slightly larger
    remaining_participants = len(participants) % group_size
    
    # Calculate how many groups we'll have
    num_groups = len(participants) // group_size
    
    # If we have remaining participants, we'll distribute them among the first few groups
    # instead of creating a separate small group
    
    # Create a list to track target size for each group
    group_sizes = [group_size] * num_groups
    
    # Distribute remaining participants among groups
    for i in range(remaining_participants):
        group_sizes[i] += 1
    
    # Shuffle participant list for random distribution
    random.shuffle(nparticipants)


    # Create groups based on calculated sizes
    for size in group_sizes:
        # Take 'size' participants from the list
        plist = []
        for i in range(size):
            if nparticipants:  # Safety check
                p = nparticipants.pop(0)  # Take from the front since we already shuffled
                plist.append(p)
            
        # Sort the list of participants alphabetically
        plist.sort()
        
        # Add alphabetically sorted list to set of groups
        if plist:  # Only add if there are participants in the list
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
    # Default to random if invalid input is provided
    print(f"Invalid choice '{starter_choice}'. Using random conversation starter.")
    starter_type = None  # Random selection

# Get a conversation starter
conversation_starter = get_random_conversation_starter(starter_type)

# assemble output for printout
output_string = ""

output_string += "----------------------------------------\n"
output_string += "TODAY'S COFFEE PARTNER GROUPS\n"
output_string += "----------------------------------------\n\n"

# Display each group as a table
group_number = 1
for group in ngroups:
    group = list(group)
    output_string += f"GROUP {group_number}:\n"
    output_string += "----------------------------------------\n"
    output_string += f"{'Name':<30} | {'Email':<30}\n"
    output_string += "----------------------------------------\n"
    
    for i in range(0, len(group)):
        name = formdata[formdata[header_email] == group[i]].iloc[0][header_name]
        email = group[i]
        output_string += f"{name:<30} | {email:<30}\n"
    
    output_string += "----------------------------------------\n\n"
    group_number += 1

# Add conversation starter to output
output_string += "----------------------------------------\n"
output_string += "CONVERSATION STARTER:\n"
output_string += "----------------------------------------\n"
output_string += conversation_starter + "\n"

# write output to console
print(output_string)

# write output into text file for later use
with open(new_groups_txt, "wb") as file:
    file.write(output_string.encode("utf8"))

# write new groups into CSV file (for e.g. use in MailMerge)
with open(new_groups_csv, "w") as file:
    # Calculate max group size for header
    max_group_size = max(len(group) for group in ngroups)
    
    # Create dynamic header based on the largest group
    header = []
    for i in range(1, max_group_size + 1):
        header.extend([f"name{i}", f"email{i}"])
    header.append("conversation_starter")
    
    file.write(DELIMITER.join(header) + "\n")
    
    # Write each group to CSV
    for group in ngroups:
        group = list(group)
        row_data = []
        
        # Add each member's name and email
        for i in range(max_group_size):
            if i < len(group):
                try:
                    name = formdata[formdata[header_email] == group[i]].iloc[0][header_name]
                    email = group[i]
                    row_data.extend([name, email])
                except Exception:
                    row_data.extend(["Error", group[i]])
            else:
                # Fill empty slots for consistent columns
                row_data.extend(["", ""])
        
        # Add conversation starter
        row_data.append(conversation_starter)
        
        # Write the row
        file.write(DELIMITER.join(row_data) + "\n")

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



# Generate personalized messages for each group and save to text files
print("\nGenerating personalized messages for each group...")
messages_dir = "messages"

# Create messages directory if it doesn't exist
if not os.path.exists(messages_dir):
    os.makedirs(messages_dir)

# Group message template
message_template = """Hello {names}!

You've been matched for a CaféConnect chat! 

Please arrange a time to meet that works for everyone in your group.

To help break the ice, here's a conversation starter:
{conversation_starter}

Enjoy your coffee chat!
"""

# Create a consolidated file for all messages
with open(os.path.join(messages_dir, "all_group_messages.txt"), "w", encoding="utf-8") as all_messages_file:
    all_messages_file.write("===== MESSAGES FOR ALL GROUPS =====\n\n")

    # Create individual messages for each group
    group_number = 1
    for group in ngroups:
        group = list(group)

        # Get the names of all participants in the group
        names = []
        emails = []
        for email in group:
            name = formdata[formdata[header_email] == email].iloc[0][header_name]
            names.append(name)
            emails.append(email)

        # Format names for the message
        if len(names) == 2:
            names_str = f"{names[0]} and {names[1]}"
        else:
            names_str = ", ".join(names[:-1]) + f", and {names[-1]}"

        # Generate the personalized message
        personalized_message = message_template.format(
            names=names_str,
            conversation_starter=conversation_starter
        )

        # Save to individual file
        group_file_name = f"group_{group_number}_message.txt"
        with open(os.path.join(messages_dir, group_file_name), "w", encoding="utf-8") as group_file:
            group_file.write(personalized_message)

        # Add to the consolidated file
        all_messages_file.write(f"===== GROUP {group_number} =====\n")
        all_messages_file.write(f"Participants: {names_str}\n")
        all_messages_file.write(f"Emails: {', '.join(emails)}\n\n")
        all_messages_file.write(personalized_message)
        all_messages_file.write("\n\n")

        group_number += 1

print(f"Messages generated and saved to the '{messages_dir}' directory.")
print(f"Individual messages for each group are saved as separate files.")
print(f"A consolidated file with all messages is saved as 'all_group_messages.txt'.")


# print finishing message
print()
print("Job done.")