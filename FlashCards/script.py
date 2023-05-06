### TO DO LIST
### > 'If not, PyFlashCards will quit.' - Instead return to main menu
### > Complete main_menu_loop() functionalization
### > Functionalize testing code as testing_loop() function
### > Implement CardDeck class

import csv
import time
import re # Regex, for stripping illegal chars from file names
from os import listdir
from os.path import isfile, join, dirname, abspath
from random import randint


# Class for card decks and their titles
class CardDeck:
    def __init__(self, title="User Flash Card Deck", cards=[]):
        self.title = title
        self.cards = cards
        self.size = len(cards)

    def add_card(sideA, sideB):
        self.cards.append([sideA, sideB])
        self.size += 1

    def remove_card():
        pass


# Generates an ASCII title box and returns it as a string
def title_box(title_string, new_line = 0):
    # First, generate the title string and space it
    # title_string = f"CARD NO. {card_no + 1}"
    for i in range(1, len(title_string)):
        insert_point = (i * 2) - 1
        title_string = (title_string[:insert_point] + " " +
                title_string[insert_point:])

    # Next, generate the card with border
    top_bottom = "00=="
    for i in range(len(title_string)):
        top_bottom += "="
    top_bottom += "==00"
    mid_line = "\n||  " + title_string + "  ||\n"
    card_string = top_bottom + mid_line + top_bottom

    # If required, add an additional carriage return at the end
    if new_line == 1:
        card_string += "\n"

    # Return the result
    return card_string


# Prints a blank line
def blank_line():
    print("")


# LOOP - takes user input and handles exceptions
def input_loop(prompt, accepted, times=3, mode="simple"):
    # This should give an initial prompt and an optionally customizable
    # error message. Probably I should use a Class here.
    
    i = 0 # Count how many times we've run
    # Loop ends only when a valid input is given
    while True:
        # Take the user's input
        # On the first and every times+1th iteration, show the full prompt
        if i % (times + 1) == 0:
            user_input = input(prompt + "\n: ")
        else:
            # Display the error message and re-prompt
            user_input = input("I'm sorry, that input wasn't recognized. "
                               "Please try again.\n: ")
        blank_line()
        # Check the input is among those accepted
        if mode != "case-sensitive":
            user_input = user_input.upper()
            accepted = [item.upper() for item in accepted]
        # The user can pass the wildcard "*" to accept all inputs
        if (user_input in accepted) or (accepted == "*"):
            # Successful input; exit loop and return value
            return user_input
        # If unsuccessful, go to the next iteration
        i += 1

# LOOP - handles new deck creation (card and title input)
# and saves the created deck to CSV
def deck_creation_loop():
    # Print orienting information
    print(title_box("New Deck Creation Mode", 1))
    time.sleep(sleep_time)
    print("Each flash card should consist of two paired values.\n")
    time.sleep(sleep_time)
    print("These might be a question and an answer, a heading and what "
          "falls under it,\nor just two things that belong together. \n")
    time.sleep(sleep_time)
    print("Try to keep it consistent within each deck. But also, don't "
          "sweat it too much.\n")
    time.sleep(sleep_time)

    # User input
    i = 0
    new_deck = []
    taking_content = True
    while(taking_content):
        print(title_box(f"CARD NO. {i + 1}", 1))
        if i == 0:
            print("What would you like your first card to be?\n")
            valueA = input(f"Enter side A for card {i+1}, "
                           "then press [Enter].\n: ")
        else:
            valueA = input(f"Enter side A for card {i + 1} if "
                    "you'd like to continue, or type N if you're "
                    "finished.\n: ")
            # if(more_to_add in ["N", "NO"]):
            #     taking_content = False
            if(valueA.upper() in ["N", "NO"]):
                break
        valueB = input(f"Enter side B for card {i+1}, "
                       "then press [Enter].\n: ")
        new_deck.append([valueA, valueB])
        print(f"\nGot it. Value A is '{valueA}'. Value B is '{valueB}'.")
        blank_line()
        i += 1
    deck_title = input("Finally, what title would you like to give "
            "this deck? (Up to 30 characters. This can be different "
            "to its file name.)\n: ")[:30]

    # Print out the completed deck, with title box
    deck_size = len(new_deck)
    num_width = len(str(deck_size + 1))
    tab_size = num_width + 5
    print("\nGreat. Here's your deck in review:\n")
    time.sleep(sleep_time / 3)
    print(title_box(deck_title.upper(), 1))
    time.sleep(sleep_time / 3)
    for i in range(deck_size):
        # Print the first line of our two-column table
        line_str = f"{i + 1}."
        for j in range(tab_size - len(line_str)):
            line_str += " "
        line_str += f"Side A.    {new_deck[i][0]}"
        print(line_str)
        # Print the second line of our two-column table
        line_str = ""
        for j in range(tab_size):
            line_str += " "
        line_str += f"Side B.    {new_deck[i][1]}"
        print(line_str + "\n")
        time.sleep(sleep_time / 3)
    time.sleep(sleep_time * 2 / 3)

    # Prompt the user for a filename
    file_name = input("If you would like to save this deck, please "
            f"enter a file name up to {max_file_name_len} characters. "
            "If you would like to cancel, type CANCEL."
            "\n: ")[:max_file_name_len]
    time.sleep(sleep_time)
    if file_name.upper() == "CANCEL":
        print("Cancelling.\n")
        time.sleep(sleep_time)
        restart = input("Would you like to start again? [Y/N]\n"
                "If not, PyFlashCards will quit.\n: ").upper()
        if(restart in ["Y", "YES", ""]):
            deck_creation_loop()
        else:
            print("Quitting PyFlashCards.\n")
            time.sleep(sleep_time)
            exit()
    else:
        file_name_clean = file_name_handler(file_name, "csv",
                                            max_file_name_len)
        # Open the file for writing
        with open(file_name_clean, "x", newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",", \
                    quotechar="^", quoting=csv.QUOTE_MINIMAL)
            # Write the file name row
            csv_writer.writerow([deck_title])
            # Loop through the new deck and write each line
            for card in new_deck:
                csv_writer.writerow([card[0], card [1]])
        # Give a lil progress bar simulation
        time.sleep(sleep_time / 3)
        for i in range(3):
            print(".")
            time.sleep(sleep_time / 3)
        print("\nDeck saved successfully.")
        blank_line()


# LOOP - list all available files and return the user's selection
def file_selection_loop():
    # We list the available files in sections, page by page
    page = 0
    files_per_page = 10
    listing = True
    final_page = False
    print("Which deck would you like to open first?\n")
    while listing:
        list_size = len(file_list)
        files_listed = page * files_per_page
        print(f"Showing files {files_listed+1} to "
              f"{files_listed+files_per_page} of {list_size}.")
        msg = "Enter a number to make a selection"
        # Check this isn't the final page of files
        if (list_size < (page + 1) * files_per_page):
            final_page = True
        else:
            msg += ", or press [Enter] to see more files"
        print(msg + ".\n")
        # Print our two-column table of file numbers and file names
        num_width = len(str(list_size + 1))
        tab_size = num_width + 5
        for i in range(files_listed, files_listed + files_per_page):
            if i < list_size:
                line_str = f"{i + 1}"
                for j in range(tab_size - len(line_str)):
                    line_str += " "
                line_str += file_list[i]
                print(line_str)
        blank_line()

        # User input loop for file selection
        taking_input = True
        while taking_input:
            # Get the file number user input
            file_number = input(": ")
            blank_line()
            # ADD LATER - handle "CANCEL" input to return to menu
            # Strip out any character that isn't a number
            file_number = "".join(_ for _ in file_number
                                  if _ in "0123456789")
            # If input is blank, move to the next page
            if file_number == "":
                page += 1
                taking_input = False # Exit the input loop
            else:
                # Check the file number is in range
                file_number = int(file_number)
                if file_number > (list_size + 1):
                    # If out of range, print an error message
                    print("There isn't a file with that number. "
                            "Please try again.\n")
                    continue # Go back to the loop's beginning
                # ADD LATER - Check the file still exists?
                # We now have the user's selection, so exit both loops
                taking_input = False
                listing = False
    
    # Finally, return the result
    return file_number


# Cleans up a file name ready for writing, and avoids
# overwriting existing files
def file_name_handler(name, extension, max_len):
    # Strip the filename of illegal characters
    name = re.sub(r"\W+", "", name)

    # If the filename is already taken, add a number to the end
    i = 0
    while isfile(name + "." + extension):
        i += 1
        affix_str = f"({i})"
        # Calculate available length left after addition of affix
        new_max_len = max_len - len(affix_str)
        if i > 1:
            # An affix already exists. Take the length of
            # everything from the last opening parenthesis in the
            # file name onwards, inclusive
            affix_len = len(name.split("(")[1]) + 1
            # Use it to strip out the old affix
            end_indx = len(name) - affix_len
            name = name[:end_indx]
        # Make sure there's space for the new affix, and add it
        if len(name) > new_max_len:
            name = name[:new_max_len]
        name += affix_str

    # Finally, add the filetype extension and return the result
    name += "." + extension
    return name


# Define variables
mypath = dirname(abspath(__file__))
sleep_time = 1
max_file_name_len = 40

# Deliver welcome message and check for files
# I'll replace this later with an ASCII title graphic
print("Welcome to PyFlashCards!\n")
#### BEGINNING OF CODE TO BECOME LOADING SCREEN / MAIN MENU
#### def main_menu_loop():
print("Loading cards . . .\n")
time.sleep(sleep_time)

# Create a list of CSVs in the script's directory
# Later I need to update this to use Python 3's os.scandir iterator
file_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]
file_list = [f for f in file_list if f.lower()[-4:] == ".csv"]
# Sort the list of files alphabetically, without regard for capitals
file_list.sort(key=str.lower)

# If there are no CSVs yet, prompt the user to create one
if (len(file_list) < 1):
# if (1 == 1):
    deck_creation_loop()

    # At this point when properly functionized we'll return to 
    # what is now line 43
    # main_menu_loop()
    print("Loading cards . . .\n")
    time.sleep(sleep_time)

# Otherwise, files exist, so give the user the loading list
else:
    # This will be the place to ask whether they'd like to open
    # an existing deck or make a new one one
    prompt = ("Card decks found. Type LOAD to load, or MAKE "
              "to create a new one.")
    accepted = ["LOAD", "MAKE"]
    user_input = input_loop(prompt, accepted)
    blank_line()
    if user_input == "LOAD":
        print("Loading mode")
    elif user_input == "MAKE":
        # print("Creation mode")
        deck_creation_loop()

    # Run the file selection loop and store the selected file number
    file_number = file_selection_loop()

    # . . . and load the chosen file
    with open(file_list[file_number - 1], "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",",
                quotechar="^")
        loaded_deck = list(csv_reader)
        loaded_title = loaded_deck[0][0]
        print(title_box(loaded_title.upper(), 1))
        # Populate available cards list (this will be easy to methodize)
        available_cards = [loaded_deck[i] for i in range(1,
                len(loaded_deck))]
        # Ask the user for round size
        default_round_size = 10
        round_size = input("How many cards would you like to be "
                "tested on per round? (Round size is capped at deck "
                "size.)\n: ")
        # Strip out non-numerical characters
        round_size = "".join(_ for _ in round_size if _ in "0123456789")
        # Set to default if blank
        round_size = (default_round_size if round_size == ""
                else int(round_size))
        # Cap round size at total deck size
        if round_size > len(available_cards):
            round_size = len(available_cards)
        blank_line()

        # Begin the testing loop
        testing = True
        asked_total = 0
        asked_this_round = 0
        questions_correct = 0
        while testing:
            # First, check whether we've already finished the round
            if asked_this_round >= round_size:
                print("Round complete! So far you've got " \
                        f"{questions_correct} of {asked_total} " \
                        "correct.\n")
                user_input = input("Do you want to continue? [Y/N] " \
                        "\n: ").upper()
                blank_line()
                if user_input == "N":
                    # End the testing session
                    # Later this should return us to loading
                    testing = False
                    break
                else:
                    # Initiate the new round
                    asked_this_round = 0
            # Randomly select one of the available cards
            card_no = randint(0, len(available_cards)-1)
            cur_card = available_cards[card_no]
            # Print the card
            print("Press [Enter] to flip the card.")
            print("Side A:\n\n      " + cur_card[0] + "\n")
            user_input = input("")
            print("Side B:\n\n      " + cur_card[1] + "\n")
            user_input = input("Type Y or press [Enter] if right. " \
                    "Type N if wrong.\n").upper()
            blank_line()
            if user_input != "N":
                # Increment the correct answers counter
                questions_correct += 1
            # Increment the questions asked counters
            asked_total += 1
            asked_this_round += 1
            # Remove the card from the working deck
            available_cards.pop(card_no)
            # available_cards = available_cards[:card_no] + \
                    # available_cards[card_no+1:]
            # Check we haven't exhausted the deck, and end if so
            if len(available_cards) < 1:
                print("Well done! You've completed the deck. " \
                        f"You got {questions_correct} of " \
                        f"{asked_total} correct.")
                # End the testing session
                # Later this should return us to loading
                testing = False
                break
            # If we are continuing, re-print the deck's title
            print(title_box(loaded_title.upper(), 1))
blank_line()





        




# # Get a list of the dict's keys


# # Get a list of the dict's keys
# values_list = list(testDict.keys())
# print(values_list)

# print(values_list[0])
# print(testDict[values_list[0]])

# prompt = "What is the value of " + values_list[0] + "? "

# user_input = input(prompt)

# if user_input == str(testDict[values_list[0]]):
#     print("Correct!")
# else:
#     print("Wrong!")

