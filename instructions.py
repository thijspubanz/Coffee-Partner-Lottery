"""
This module contains instructions for users on how to fill out the form and download the CSV file.
"""

def get_setup_instructions():
    """
    Returns instructions for setting up the form and downloading CSV file.
    """
    instructions = """
==========================================================
CAFÉCONNECT - SETUP INSTRUCTIONS
==========================================================

1. CREATE AND SET UP THE FORM:
   - We use Google Forms to collect participant information
   - Required fields: Full Name and Email Address
   - Google Form link: https://docs.google.com/forms/d/e/1FAIpQLSceBJ7UdstAzoVEjIAb3kL6_EkB5UaQ0XZ_To4Sp81ZXQcCiA/viewform?usp=header

2. COLLECT RESPONSES:
   - Share the form link with potential participants
   - Allow sufficient time for people to respond

3. DOWNLOAD RESPONSES AS CSV:
   - In Google Forms: Go to "Responses" tab
   - Click the three dots menu (⋮) in the top-right corner
   - Select "Download responses (.csv)"
   - Save the file as "Coffee Partner Lottery participants.csv" in the same directory as this program

4. FORMAT VERIFICATION:
   - Ensure the CSV file has columns for:
     - "What is your full name?" (for names)
     - "What is your email adress?" (for emails)
   - The program will use these columns to create coffee pairings

5. ENVIRONMENT SETUP:
   - Make sure your .env file contains:
     - GOOGLE_CREDENTIALS: Your Google API credentials (for Google Forms API)
     - SPREADSHEET_ID: The ID of your Google Spreadsheet (from the form responses)

6. RUN THE PROGRAM:
   - Execute the CoffeePairing.py script
   - Follow the prompts to generate groups and conversation starters

==========================================================
"""
    return instructions

def get_usage_instructions():
    """
    Returns instructions on how to use the program after setup.
    """
    instructions = """
==========================================================
USING CAFÉCONNECT
==========================================================

1. RESET OPTIONS:
   - At the start, you'll be asked if you want to reset previous groups
   - Choose 'y' to clear history (everyone can be paired with anyone)
   - Choose 'n' to maintain history (avoid repeating previous pairings)

2. GROUP SIZE:
   - Enter the desired number of people per group (minimum 2)
   - The program will automatically adjust if your number is too large or small
   - You can set a default group size in the config.json file

3. CONVERSATION STARTER TYPE:
   - Choose the type of conversation starter:
     1. Joke - Lighthearted humor to break the ice
     2. Question - Thought-provoking questions to spark discussion
     3. Debate - Topics for friendly discussion or debate
     4. Random - A mix of all types

4. RESULTS:
   - Results will be displayed on screen
   - Saved to "Coffee Partner Lottery new groups.txt" for easy sharing
   - Saved to "Coffee Partner Lottery new groups.csv" for mail merges
   - All pairings are also saved to "Coffee Partner Lottery all groups.csv"

5. SHARING RESULTS:
   - Copy from the text file to share in email or messaging platforms
   - Use the CSV with mail merge tools to send personalized emails

==========================================================
"""
    return instructions