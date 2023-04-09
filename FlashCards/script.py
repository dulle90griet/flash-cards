import csv
from os import listdir
from os.path import isfile, join, dirname, abspath

testDict = {"A": 1}
mypath = dirname(abspath(__file__))


# Deliver welcome message and check for files
# I'll replace this later with an ASCII title graphic
print("Welcome to PyFlashCards!")

# Create a list of CSVs in the script's directory
file_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]
file_list = [f for f in file_list if f.lower()[-4:] == ".csv"]

# If there are no CSVs yet, prompt the user to create one
if (len(file_list) < 1):
    print("It seems no card decks exist yet. We'd better make one.")
    print("Each flash card should consist of two paired values. These " \
            "might be a question and an answer, a heading and what " \
            "falls under it, or just two things that belong together.")
    print("Try to keep it consistent within each deck. But also, don't " \
            "sweat it too much.")
    print("What would you like your first value to be?")
    i = 0
    taking_content = True
    while(taking_content):
        valueA = input(f"Enter value A for card {i+1}, " \
                "then press [Enter]: ")
        valueB = input(f"Enter value B for card {i+1}, " \
                "then press [Enter]: ")
        print(f"Got it. Value A is '{valueA}'. Value B is '{valueB}'.")
        is_correct = input("Is that correct? [Y/N]: ").upper()
        if(is_correct == "Y"):
            more_to_add = input("Great. Would you like to add " \
                    "another card to this deck? [Y/N]: ").upper()
            if(more_to_add == "Y"):
                i += 1
            else:
                taking_content = False
        elif(is_correct == "N"):
            print("Okay. Let's try that again.")

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

