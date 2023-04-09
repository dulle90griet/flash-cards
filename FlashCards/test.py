max_file_name_len = 20

def fnc(string, afx):
    afx = int(afx)
    affix_str = f"({afx})"
    new_max_len = max_file_name_len - len(affix_str)
    if afx > 1:
        # end_indx = len(string) - len(f"({afx-1})")
        end_indx = len(string) - (len(string.split("(")[-1]) + 1)
        string = string[:end_indx]
    if len(string) > new_max_len:
        string = string[:new_max_len]
    string += affix_str
    print(string)
    print(f"{len(string)} characters")

quitting = False
while not quitting:
    user_in = input("Enter [string], [int], or type QUIT to quit\n: ")
    if user_in == "QUIT":
        quitting = True
    else:
        inputs = user_in.split(",")
        fnc(inputs[0], inputs[1])
exit()
    
