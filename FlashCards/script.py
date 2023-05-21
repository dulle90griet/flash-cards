import csv
import time
import re # Regex, for stripping illegal chars from file names
from os import listdir
from os.path import isfile, join, dirname, abspath
from random import randint
from copy import deepcopy


# Class for card decks and their titles
class CardDeck:
    def __init__(self, title="User Flash Card Deck", cards=[]):
        self.title = title
        # Next line inexplicably necessary to avoid all decks'
        # card lists being stored at the same address
        self.cards = [] if cards == [] else cards
        self.size = len(cards)

    def add_card(self, sideA, sideB):
        self.cards.append([sideA, sideB])
        self.size += 1

    def remove_card(self, card_no):
        self.cards.pop(card_no)
        self.size -= 1


# Prints a blank line
def blank_line():
    print("")


# Prints a dividing line
def divider():
    print("========================================\n")


# Loads a CSV file into a CardDeck object
def load_deck(file):
    with open(file, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",", quotechar="^")
        loaded_deck = CardDeck()
        i = 0
        for row in csv_reader:
            if i < 1 and len(row) < 2:
                # If the first row has only one value, it's our title
                loaded_deck.title = row[0]
            else:
                # Otherwise, assume it's a card
                loaded_deck.add_card(row[0], row[1])
            i += 1
    # Return a pointer to the new CardDeck
    return loaded_deck


# Generates an ASCII title box and returns it as a string
def title_box(title_string, tailing_lines = 0):
    # First, generate the title string and space it
    for i in range(1, len(title_string)):
        insert_point = i*2 - 1
        title_string = (title_string[:insert_point] + " " +
                title_string[insert_point:])

    # Next, generate the card with border
    top_bottom = "00=="
    for i in range(len(title_string)):
        top_bottom += "="
    top_bottom += "==00"
    mid_line = "\n||  " + title_string + "  ||\n"
    card_string = top_bottom + mid_line + top_bottom

    # Add tailing newlines as required 
    for i in range(tailing_lines):
        card_string += "\n"

    # Return the result
    return card_string


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
        # Calculate characters remaining after addition of affix
        new_max_len = max_len - len(affix_str)
        if i > 1:
            # An affix already exists, so take its length
            affix_len = len(name.split("(")[1]) + 1
            # Use it to strip out the old affix
            end_indx = len(name) - affix_len
            name = name[:end_indx]
        # Make sure there's space for the new affix, then add it
        if len(name) > new_max_len:
            name = name[:new_max_len]
        name += affix_str

    # Finally, add the filetype extension and return the result
    return name + "." + extension


# LOOP - takes user input and handles exceptions, with an initial prompt
# and an optionally customizable error message
def input_loop(prompt, accepted="*", times=3, blank_allowed=False, 
               cancellable=False, quittable=False, numerical=False,
               case_sensitive=False,
               err_msg = ("I'm sorry, that input wasn't recognised. "
                          "Please try again.")):
    i = 0
    # Loop ends only when a valid input is given
    while True:
        # Take the user's input
        # On the first and every times+1th iteration, show the full prompt
        if i % (times + 1) == 0:
            user_input = input(prompt + "\n: ")
        else:
            # Display the error message and re-prompt
            user_input = input(err_msg + "\n: ")
        blank_line()
        # If we don't want case-sensitivity, make all upper-case
        if not case_sensitive:
            user_input = user_input.upper()
            accepted = [str(item).upper() for item in accepted]
        # If allowing cancel or quit, handle those inputs first
        if ((cancellable and user_input == "CANCEL") 
            or (quittable and user_input in ["QUIT","EXIT"]) 
            or (blank_allowed and user_input == "")):
            return user_input
        # If expecting a number only, strip out all but numbers
        if numerical:
            user_input = "".join(_ for _ in user_input
                                 if _ in "0123456789.")
        # Check the input is among those accepted. "*" accepts all.
        if (user_input in accepted) or ("*" in accepted):
            # Successful input; exit loop and return value
            return user_input
        # If unsuccessful, go to the next iteration
        i += 1


# LOOP - Confirm the user would like to quit
def quit_confirm_loop():
    accepted = ["","Y","YES","QUIT","EXIT","N","NO","CANCEL"]
    user_input = input_loop("Are you sure you would like to quit?\n"
                            "Type Y or press [Enter] to continue quit"
                            "ting, or N or CANCEL to cancel.",
                            accepted).upper()
    blank_line()
    if user_input in accepted[:5]:
        print("Quitting PyFlashCards.")
        time.sleep(sleep_time)
        blank_line()
        exit()
    elif user_input in accepted[5:]:
        return False


# LOOP - manu menu
def main_menu_loop(load=True):
    divider()

    if load:
        print("Loading cards . . .\n")
        time.sleep(sleep_time)

        # Create a list of CSVs in the script's directory
        # Later I need to update this to use Py3's os.scandir iterator
        file_list = [f for f in listdir(mypath)
                     if isfile(join(mypath, f))
                     and f.lower()[-4:] == ".csv"]
        # Sort the list of files alphabetically, w/o regard for capitals
        file_list.sort(key=str.lower)

    # If there are no CSVs yet, prompt the user to create one
    if (len(file_list) < 1):
        print("It looks like no card decks exist. Let's create one.\n")
        deck_creation_loop(file_list)

    # Otherwise, files exist, so give the user the choice
    else:
        # Print title box
        print(title_box("Main Menu", 1))
        # Take user input
        accepted = ["LOAD","MAKE","QUIT","EXIT"]
        user_input = input_loop("Card decks found. Type LOAD to load, "
                                "or MAKE to create a new one.", accepted)
        blank_line()
        if user_input == "LOAD":
            # Run the file selection loop and store the file number
            file_number = deck_loading_loop(file_list)
            # Load the chosen file and call the testing loop 
            loaded_deck = load_deck(file_list[file_number])
            testing_loop(loaded_deck)
        elif user_input == "MAKE":
            # Call the deck creation loop
            deck_creation_loop(file_list)
        elif user_input in ["QUIT","EXIT"]:
            # Call the quit confirm loop
            if not quit_confirm_loop():
                main_menu_loop(load=False)

    blank_line()


# LOOP - handles new deck creation (card and title input)
# and saves the created deck to CSV
def deck_creation_loop(file_list):
    divider()

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
    new_deck = CardDeck()
    while True:
        print(title_box(f"CARD NO. {i + 1}", 1))
        if i == 0:
            print("What would you like your first card to be?\n")
            valueA = input(f"Enter side A for card {i+1}, "
                           "then press [Enter].\n: ")
        else:
            valueA = input(f"Enter side A for card {i + 1} if "
                    "you'd like to continue, or type N if you're "
                    "finished.\n: ")
            if(valueA.upper() in ["N", "NO"]):
                break
        valueB = input(f"Enter side B for card {i+1}, "
                       "then press [Enter].\n: ")
        new_deck.add_card(valueA, valueB)
        print(f"\nGot it. Value A is '{valueA}'. Value B is '{valueB}'.")
        blank_line()
        i += 1
    blank_line()
    new_deck.title = input("Finally, what title would you like to give "
            f"this deck? (Up to {max_title_len} characters.\nThis can be "
            "different to its file name.)\n: ")[:max_title_len]

    # Print out the completed deck, with title box
    num_width = len(str(new_deck.size + 1))
    tab_size = num_width + 5
    print("\nGreat. Here's your deck in review:\n")
    time.sleep(sleep_time / 3)
    print(title_box(new_deck.title.upper(), 1))
    time.sleep(sleep_time / 3)
    for i in range(new_deck.size):
        # Print the first line of our two-column table
        line_str = f"{i + 1}."
        for j in range(tab_size - len(line_str)):
            line_str += " "
        line_str += f"Side A.    {new_deck.cards[i][0]}"
        print(line_str)
        # Print the second line of our two-column table
        line_str = ""
        for j in range(tab_size):
            line_str += " "
        line_str += f"Side B.    {new_deck.cards[i][1]}"
        print(line_str + "\n")
        time.sleep(sleep_time / 3)
    time.sleep(sleep_time * 2 / 3)

    # Prompt the user for a filename
    file_name = input("If you would like to save this deck, please "
            f"enter a file name up to {max_file_name_len} characters. "
            "If you would like to cancel, type CANCEL."
            "\n: ")[:max_file_name_len]
    blank_line()
    time.sleep(sleep_time)
    if file_name.upper() == "CANCEL":
        print("Cancelling.\n")
        time.sleep(sleep_time)
        restart = input("Would you like to start again? Type Y for 'yes',"
                        " N or [Enter] for 'no'.\n").upper()
        if restart in ["Y", "YES"]:
            deck_creation_loop(file_list)
        else:
            print("Quitting New Deck Creation Mode.\n")
            time.sleep(sleep_time)
            main_menu_loop()
    else:
        file_name_clean = file_name_handler(file_name, "csv",
                                            max_file_name_len)
        # Open the file for writing
        with open(file_name_clean, "x", newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",", \
                    quotechar="^", quoting=csv.QUOTE_MINIMAL)
            # Write the file name row
            csv_writer.writerow([new_deck.title])
            # Loop through the new deck and write each line
            for card in new_deck.cards:
                csv_writer.writerow([card[0], card [1]])
        # Give a lil progress bar simulation
        time.sleep(sleep_time / 3)
        for i in range(3):
            print(".")
            time.sleep(sleep_time / 6)
        print("\nDeck saved successfully.")
        blank_line()
    main_menu_loop()


# LOOP - list all available files and return the user's selection
def deck_loading_loop(file_list):
    divider()

    # Print title box
    print(title_box("Saved Deck Loading Mode", 1))
    time.sleep(sleep_time / 3)
    # We list the available files in sections, page by page
    page = 0
    files_per_page = 10
    listing = True
    final_page = False
    print("Which deck would you like to open first?\n")
    while listing:
        if final_page:
            # The previous iteration already found the last page
            print("All files already shown.\nEnter a number to make "
                  "a selection.\n")
        else:
            list_size = len(file_list)
            files_listed = page * files_per_page
            print(f"Showing files {files_listed+1} to "
                  f"{files_listed+files_per_page} of {list_size}.")
            msg = "Enter a number to make a selection"
            # Check this isn't the final page of files
            if (list_size <= (page + 1) * files_per_page):
                final_page = True
            else:
                msg += ", or press [Enter] to see more files"
            print(msg + ".\n")
            time.sleep(sleep_time / 3)
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
                    # time.sleep(sleep_time / 3)
            blank_line()

        # User input loop for file selection
        while True:
            # Get the file number user input
            accepted = list(range(1, list_size + 1))
            err_msg = ("There isn't a file with that number. "
                       "Please try again.")
            file_number = input_loop("", accepted, blank_allowed=True,
                                     cancellable=True, quittable=True,
                                     numerical=True, err_msg=err_msg)
            # Handle the non-numerical inputs first
            if file_number == "CANCEL":
                print("You asked to CANCEL. Returning to main menu.\n")
                main_menu_loop()
            elif file_number in ["QUIT","EXIT"]:
                if not quit_confirm_loop():
                    # User cancelled quit; reload same page
                    break
            elif file_number == "":
                # The user just hit [Enter], so move to the next page
                page +=1
                break
            else:
                # The user's selection is numerical and in range, so
                # exit both loops
                listing = False
                break
    
    # Finally, return the result
    return int(file_number) - 1


# LOOP - the core function of PyFlashCards: testing the user on cards!
def testing_loop(loaded_deck):
    divider()

    # Make a destructible copy of the loaded deck
    testing_deck = deepcopy(loaded_deck)
    # Print the current deck's title card
    print(title_box(testing_deck.title.upper(), 1))

    # Ask the user for round size
    prompt = ("How many cards would you like to be tested on per round?\n"
              "(Round size is capped at deck size.)")
    round_size = input_loop(prompt, numerical=True)
    # Set to default if blank
    round_size = (default_round_size if round_size in ["", "0"]
                  else int(round_size))
    # Cap round size at total deck size
    if round_size > testing_deck.size:
        round_size = testing_deck.size
    blank_line()

    # Begin the testing loop
    asked_total = 0
    asked_this_round = 0
    questions_correct = 0
    while True:
        # First, check whether we've already finished the round
        if asked_this_round >= round_size:
            print(f"Round complete! So far you've got {questions_correct}"
                  f" of {asked_total} correct.\n")
            user_input = input("Do you want to continue? Type Y or press "
                               "[Enter] for 'yes', N for 'no'."
                                "\n: ").upper()
            blank_line()
            if user_input in ["N", "NO"]:
                # End the testing session
                break
            else:
                # Initiate the new round
                asked_this_round = 0
        # Randomly select one of the available cards
        card_no = randint(0, testing_deck.size-1)
        cur_card = testing_deck.cards[card_no]
        # Print the card
        print("Press [Enter] to flip the card. "
              "Side A:\n\n      " + cur_card[0] + "\n")
        user_input = input("")
        print("Side B:\n\n      " + cur_card[1] + "\n")
        user_input = input("Type Y or press [Enter] if right. "
                "Type N if wrong.\n").upper()
        blank_line()
        if user_input not in ["N", "NO"]:
            # Increment the correct answers counter
            questions_correct += 1
        # Increment the questions asked counters
        asked_total += 1
        asked_this_round += 1
        # Remove the card from the working deck
        testing_deck.remove_card(card_no)
        # Check whether we've exhausted the deck, and end if so
        if testing_deck.size < 1:
            print("Well done! You've completed the deck. "
                    f"You got {questions_correct} of "
                    f"{asked_total} correct.")
            user_input = input("Would you like to test yourself on this "
                               "deck again? Type Y or press [Enter] for "
                               "'yes', N for 'no'.\n: ").upper()
            blank_line()
            if user_input not in ["N","NO"]:
                # Restart the testing session
                testing_loop(loaded_deck)
            elif user_input in ["QUIT","EXIT"]:
                # Allow the user to quit directly from this point
                quit_confirm_loop()
            # Otherwise, end the testing session
            break
        # If we are continuing, re-print the deck's title
        print(title_box(testing_deck.title.upper(), 1))
    # The testing loop over, return to the main menu
    print("Returning to main menu.\n")
    time.sleep(sleep_time)
    main_menu_loop()
    

# Define variables
mypath = dirname(abspath(__file__))
sleep_time = 1
max_file_name_len = 40
max_title_len = 30
default_round_size = 10
files_per_page = 10
ASCII_title = (
        "888888ba            88888888b dP                   dP       "
        " a88888b.                         dP\n"
        "88    `8b           88        88                   88       "
        "d8'   `88                         88\n"
        "88aaaa8P' dP    dP a88aaaa    88 .d8888b. .d8888b. 88d888b. "
        "88        .d8888b. 88d888b. .d888b88 .d8888b.\n"
        "88        88    88  88        88 88'  `88 Y8ooooo. 88'  `88 "
        "88        88'  `88 88'  `88 88'  `88 Y8ooooo.\n"
        "88        88.  .88  88        88 88.  .88       88 88    88 "
        "Y8.   .88 88.  .88 88       88.  .88       88\n"
        "dP        `8888P88  dP        dP `88888P8 `88888P' dP    dP "
        " Y88888P' `88888P8 dP       `88888P8 `88888P'\n"
        "               .88\n"
        "            d8888P\n")

# Deliver welcome message and check for files
print(ASCII_title)
print("Welcome to PyFlashCards!\n")

main_menu_loop()

blank_line()

