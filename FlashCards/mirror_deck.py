import csv

target_file = "metres_to_feet_dista.csv"

deck_cards = []

with open(target_file, "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",",
                            quotechar="^")
    loaded_deck = list(csv_reader)
    deck_cards = [loaded_deck[i] for i in range(1,
                    len(loaded_deck))]

deck_reversed = [[card[1], card[0]] for card in deck_cards]

with open(target_file, "a") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=",",
                            quotechar="^")
    for card in deck_reversed:
        csv_writer.writerow(card)
