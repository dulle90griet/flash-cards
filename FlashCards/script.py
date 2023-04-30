import csv
import time
import re # Regex, for stripping illegal chars from file names
from os import listdir
from os.path import isfile, join, dirname, abspath

# Generates an ASCII title box and returns it as a string
def title_box(title_string, new_line = 0):
    # First, generate the title string and space it
    # title_string = f"CARD NO. {card_no + 1}"
    for i in range(1, len(title_string)):
        insert_point = (i * 2) - 1
        title_string = title_string[:insert_point] + " " + \
                title_string[insert_point:]

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

# Define variables
mypath = dirname(abspath(__file__))
sleep_time = 1
max_file_name_len = 20

# Deliver welcome message and check for files
# I'll replace this later with an ASCII title graphic
print("Welcome to PyFlashCards!\n")
print("Loading cards . . .\n")
time.sleep(sleep_time)

# Create a list of CSVs in the script's directory
# Later I need to update this to use Python 3's os.scandir iterator
file_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]
file_list = [f for f in file_list if f.lower()[-4:] == ".csv"]

# If there are no CSVs yet, prompt the user to create one
if (len(file_list) < 1):
    print("It seems no card decks exist yet. We'd better make one. \n")
    time.sleep(sleep_time)
    print("Each flash card should consist of two paired values.\n")
    time.sleep(sleep_time)
    print("These " \
            "might be a question and an answer, a heading and what " \
            "falls under it, or just two things that belong together. \n")
    time.sleep(sleep_time)
    print("Try to keep it consistent within each deck. But also, don't " \
            "sweat it too much.\n")
    time.sleep(sleep_time)
    i = 0
    new_deck = []
    taking_content = True

    while(taking_content):
        print(title_box(f"CARD NO. {i + 1}", 1))
        if i == 0:
            print("What would you like your first card to be?\n")
        valueA = input(f"Enter side A for card {i+1}, " \
                "then press [Enter].\n: ")
        valueB = input(f"Enter side B for card {i+1}, " \
                "then press [Enter].\n: ")
        new_deck.append([valueA, valueB])
        print(f"\nGot it. Value A is '{valueA}'. Value B is '{valueB}'.")
        more_to_add = input("Press [Enter] if you would like to add " \
                "another card, or type N if you're finished. " \
                "\n: ").upper()
        if(more_to_add in ["N", "NO"]):
            taking_content = False
        else:
            i += 1
        blank_line()

    deck_title = input("Finally, what title would you like to give " \
            "this deck? (Up to 30 characters.)\n: ")[:30]

    # Print out the completed deck, with title box
    print("\nGreat. Here's your deck in review:\n")
    time.sleep(sleep_time / 3)
    print(title_box(deck_title.upper(), 1))
    time.sleep(sleep_time / 3)
    
    # Loop through the cards in the deck and print them
    deck_size = len(new_deck)
    num_width = len(str(deck_size + 1))
    tab_size = num_width + 5
    for i in range(deck_size):
        # Print the first line
        line_str = f"{i + 1}."
        for j in range(tab_size - len(line_str)):
            line_str += " "
        line_str += f"Side A.    {new_deck[i][0]}"
        print(line_str)
        # Print the second line
        line_str = ""
        for j in range(tab_size):
            line_str += " "
        line_str += f"Side B.    {new_deck[i][1]}"
        print(line_str + "\n")
        time.sleep(sleep_time / 3)
    time.sleep(sleep_time * 2 / 3)

    # Prompt the user for a filename
    file_name = input("If you would like to save this deck, please " \
            "enter a file name up to 20 characters. If you would like " \
            "to cancel, type CANCEL.\n: ")[:max_file_name_len]
    time.sleep(sleep_time)

    if file_name == "CANCEL":
        print("Cancelling.\n")
        time.sleep(sleep_time)
        restart = input("Would you like to start again? [Y/N]\n" \
                "If not, PyFlashCards will quit.\n: ").upper()
        if(restart in ["Y", "YES", ""]):
            # TK -- call deck creation function
            pass
        else:
            print("Quitting PyFlashCards.\n")
            time.sleep(sleep_time)
            exit()
    else:
        # Strip the filename of illegal characters
        file_name_clean = re.sub(r"\W+", "", file_name)

        # If the filename is already taken, add a number to the end
        i = 0
        while isfile(file_name_clean + ".csv"):
            i += 1
            affix_str = f"({i})"
            # Calculate available length left after addition of affix
            new_max_len = max_file_name_len - len(affix_str)
            if i > 1:
                # An affix already exists. Take the length of
                # everything from the last opening parenthesis in the
                # file name onwards, inclusive
                affix_len = len(file_name_clean.split("(")[1]) + 1
                # Use it to strip out the old affix
                end_indx = len(file_name_clean) - affix_len
                file_name_clean = file_name_clean[:end_indx]
            # Make sure there's space for the new affix, and add it
            if len(file_name_clean) > new_max_len:
                file_name_clean = file_name_clean[:new_max_len]
            file_name_clean += affix_str

        # Finally, add the filetype extension
        file_name_clean += ".csv"
    
    # Open the file for writing
    with open(file_name_clean, "x", newline="") as csv_file:
        field_names = ["side A", "side B"]
        csv_writer = csv.DictWriter(csv_file, delimiter=",", \
                quotechar="^", quoting=csv.QUOTE_MINIMAL, \
                fieldnames = field_names)
        csv_writer.writeheader()
        # Loop through the new deck and write each line
        for card in new_deck:
            csv_writer.writerow({"side A": card[0], "side B": card[1]})


# Otherwise, give them the loading list


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

