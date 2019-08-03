import os
import glob
import json
import time
import keyboard
import parsing
import npc


class Player:
    '''Player class'''
    def __init__(self, data):
        self.data = data  # all the data about the player's current save
        # all the data about the current location of the player
        self.current_location_data = {}
        self.rooms_available = []  # all the rooms the player can visit in the current location
        self.current_room_data = {}  # all the data on the current room the player is in
        self.current_case_data = {} # all the data on the current case the player is playing
        self.old_actions = []  # all the actions the user typed before
        self.current_room_npcs = []

        self.parser = parsing.Parser(self)

    def load_location_data(self):
        '''Function that load the data of the location in wich the player is '''

        location_file = f"case {self.data['case']}/location {self.data['current location']}/infos.data"

        with open(f"cases/{location_file}", "r") as f:  # we open the file in read mode
            # we get all the json data from the file and stock it in a dictionnary
            self.current_location_data = json.load(f)
            self.rooms_available = [os.path.basename(room) for room in glob.glob(
                f"cases/case {self.data['case']}/location {self.data['current location']}/rooms/*.room")]

    def load_room_data(self):
        ''' Function that load the data of the room in wich the player is '''

        room_file = f"case {self.data['case']}/location {self.data['current location']}/rooms/{self.data['current room']}"

        with open(f"cases/{room_file}", "r") as f:  # we open the file in read mode
            # we get all the json data from the file and stock it in a dictionnary
            self.current_room_data = json.load(f)

    def load_room_npcs(self):
        for i,n in enumerate(self.current_room_data["npcs in room"]):
            self.current_room_npcs.append(npc.Npc(n))

        for j,k in enumerate(self.current_room_npcs):
            k.load_npc(self.data["case"], self.data["current location"])

        print(self.current_room_npcs)

    def slow_print(self, text, *text_data):
        '''Function that shows a string character by character'''
        slow_text = True  # bool that determines if we show character by character
        number_of_characters = 0
        for i, char in enumerate(text):
            # if the player types space we show all the text without slowing
            if keyboard.is_pressed('space'):
                slow_text = False

            # if it's a case name we start it with an indentation to the left
            if i == 0 and text_data[0]:
                print(f"\t\t\t\t{char}", end='')
                number_of_characters += 1
            else:
                if i == 0 and not text_data[0]:
                    print("  |  ", end='')

                if char == '\n':
                    number_of_characters = 0

                if(number_of_characters <= 68):
                    if text[i-1] == '\n':
                        print("  |  ", end='')
                    os.sys.stdout.write(char)  # we show the current character
                    os.sys.stdout.flush()
                    number_of_characters += 1
                else:
                    print(char)
                    print("  |  ", end='')
                    number_of_characters = 0

            if len(text_data) > 1:  # if the dev specified how much time between each letter print
                if slow_text:
                    # we wait for a number of milliseconds
                    time.sleep(text_data[1])
            else:  # if the dev didn't specifie how much time between each letter print
                if slow_text:
                    time.sleep(.10)

        print("\n")

    def load_case_data(self):
        ''' Function that load the data of the current case'''

        case_file = f"case {self.data['case']}/case_infos.case"

        with open(f"cases/{case_file}", "r") as f:  # we open the file in read mode
            # we get all the json data from the file and stock it in a dictionnary
            self.current_case_data = json.load(f)

    def save_game(self):
        '''Function that saves the data of the player's advancement'''

        save_name = f"{self.data['name'].upper()}.save"

        # we open the save file that we want to add to the data
        with open(f"saves/{save_name}", "w") as outfile:
            # we put the json data in the new save
            json.dump(self.data, outfile, sort_keys=True, indent=4)

    def add_clue(self, clue):
        '''function that add's a clue to the players save '''
        print(
            "  ----------------------------------------------------------------------------\n")
        try:
            self.slow_print("NEW CLUE ADDED TO YOUR DATA", False, 0.02)
        except TypeError:
            print(clue)
        print(
            "  ----------------------------------------------------------------------------\n")
        self.data['case data']['clues found'] += 1
        self.data['clues found'].append(clue)

    def add_note(self, note):
        '''function that add's a note to the players save '''
        print(
            "  ----------------------------------------------------------------------------\n")
        self.slow_print(
            f"NEW ENTRY TO YOUR NOTES : {note['name']}", False, 0.02)
        print(
            "  ----------------------------------------------------------------------------\n")
        # adding the note to the players notes
        self.data['notes'].append(note)

    def show_notes(self):
        '''Function that shows all the notes that the player has found'''
        os.system("cls")

        print(
            "  ----------------------------------------------------------------------------\n")
        print(
            f"   NOTES YOU HAVE ON THE CURRENT CASE\n")
        print(
            "  ----------------------------------------------------------------------------\n")

        # if the player found at least one note
        if self.data["notes"]:
            for i, note in enumerate(self.data["notes"]):
                self.slow_print(f"NOTE {i+1} : {note['name']}", False, 0.01)
                print(
                    "  ----------------------------------------------------------------------------\n")

            while True:  # while the player didn't type a number
                try:
                    # the player chooses wich note he wants to check
                    choice = input("Wich note would you like to check ? ")

                    if choice == "quit":  # if the player typed quit we leave the notes showing
                        return 0

                    choice = int(choice)
                    break
                except ValueError:  # if the player didn't type a number
                    print("PLEASE TYPE A VALID NUMBER !")

            os.system("cls")
            # we go throught all the texts of note and show them to the player
            for i, text in enumerate(self.data["notes"][choice - 1]['texts']):
                print(
                    "  ----------------------------------------------------------------------------\n")
                self.slow_print(f"{text}", False, 0.02)
                print(
                    "  ----------------------------------------------------------------------------\n")

            os.system("pause")
            self.show_notes()  # we go back to the show_notes view
        else:
            print(
                "  ----------------------------------------------------------------------------\n")
            print(
                f"   YOU DON't HAVE A SINGLE NOTE YET.\n")
            print(
                "  ----------------------------------------------------------------------------\n")
