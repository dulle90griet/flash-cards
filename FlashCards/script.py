import csv
from os import listdir
from os.path import isfile, join, dirname, abspath

testDict = {"A": 1}
mypath = dirname(abspath(__file__))


# Deliver welcome message and check for files
# I'll replace this later with an ASCII title graphic
print("Welcome to PyFlashCards! \n")

# Create a list of CSVs in the script's directory
file_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]
file_list = [f for f in file_list if f.lower()[-4:] == ".csv"]

# If there are no CSVs yet, prompt the user to create one
if (len(file_list) < 1):
    print("It seems no card decks exist yet. We'd better make one. \n")
    print("Each flash card should consist of two paired values. These " \
            "might be a question and an answer, a heading and what " \
            "falls under it, or just two things that belong together. \n")
    print("Try to keep it consistent within each deck. But also, don't " \
            "sweat it too much. \n")
    i = 0
    new_deck = []
    taking_content = True

    # Generate our ASCII card title
    # First, generate the title string and space it
    title_string = f"CARD NO. {i + 1}"
    for j in range(1, len(title_string)):
        insert_point = (j * 2) - 1
        title_string = title_string[:insert_point] + " " + \
                title_string[insert_point:]

    # Next, generate the card with border
    top_line = "00=="
    for j in range(len(title_string)):
        top_line += "="
    top_line += "==00"
    mid_line = "\n||  " + title_string + "  ||\n"
    card_string = top_line + mid_line + top_line

    # Finally, print the card
    print(card_string + "\n")

    print("What would you like your first value to be?\n")
    while(taking_content):
        valueA = input(f"Enter value A for card {i+1}, " \
                "then press [Enter].\n: ")
        valueB = input(f"Enter value B for card {i+1}, " \
                "then press [Enter].\n: ")
        print(f"Got it. Value A is '{valueA}'. Value B is '{valueB}'.")
        is_correct = input("Is that correct? [Y/N]\n: ").upper()
        if(is_correct == "Y"):
            new_deck.append([valueA, valueB])
            more_to_add = input("Great. Would you like to add " \
                    "another card to this deck? [Y/N]\n: ").upper()
            if(more_to_add == "Y"):
                i += 1
            else:
                taking_content = False
        elif(is_correct == "N"):
            print("Okay. Let's try that again.\n")

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

