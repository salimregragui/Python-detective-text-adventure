import os
import json
import glob
import time
import keyboard
import player

class GameManager:
    '''The class that manages everything'''
    def __init__(self):
        self.state = "Playing"

    def new_game(self):
        '''Function that creates a new game by creating the json save file'''

        os.system("cls")

        print("WELCOME TO DETECTIVE GAME !")
        name = input("WHAT IS YOUR NAME : ")

        #the name that's going to be used in the save folder exp "MAX.save"
        save_name = f"{name.upper()}.save"
        saves_available = [os.path.basename(save) for save \
                           in glob.glob('saves/*.save')] #get all the saves in folder

        #if the user didn't type a name or the name is not available
        while not name or save_name in saves_available:
            if not name: #if the user didn't type a name
                print("PLEASE TYPE A VALID NAME !")
                name = input("WHAT IS YOUR NAME : ")

            if save_name in saves_available: #if the name is not available
                print("THIS NAME IS NOT AVAILABLE !")
                name = input("WHAT IS YOUR NAME : ")

                #the name that's going to be used in the save folder exp "MAX.save"
                save_name = f"{name.upper()}.save"

        new_player_data = {
            "case": 0,
            "case data": {
                "case completion": 0,
                "clues found": 0,
                "locations visited": [],
                "total clues": 8
            },
            "case finished": False,
            "case started": False,
            "clues found": [],
            "current location": 1,
            "current room": "1.room",
            "current text": 3,
            "name": name.upper(),
            "notes": [],
            "npcs talked to": [],
            "inventory" : []
        }

        #we open the save file that we want to add to the data
        with open(f"saves/{save_name}", "w") as outfile:
            #we put the json data in the new save
            json.dump(new_player_data, outfile, sort_keys=True, indent=4)

        print("NEW SAVE ADDED WITH SUCCESS")
        os.system("Pause")

        self.cplayer = player.Player(new_player_data) #we create a new player that is going to play

        self.cplayer.load_location_data()
        self.cplayer.load_room_data()
        self.cplayer.load_case_data()
        self.cplayer.load_room_npcs()

        self.game_loop()

    def load_game(self):
        '''Function to load an already started save'''

        print("WELCOME TO DETECTIVE GAME !")
        name = input("WHAT IS THE NAME OF THE SAVE YOU WANT TO LOAD : ")
        save_name = f"{name.upper()}.save" #the name of the save file exp "MAX.save"

        saves_available = [os.path.basename(save) for save \
                           in glob.glob('saves/*.save')] #get all the saves in folder

        while save_name not in saves_available:
            if save_name not in saves_available:
                print("SORRY ! THIS SAVE DOESN'T EXIST !")
                name = input("WHAT IS THE NAME OF THE SAVE YOU WANT TO LOAD : ")
                save_name = f"{name.upper()}.save" #the name of the save file exp "MAX.save"

        with open(f"saves/{save_name}", "r") as f: #we open the file in read mode
            save_data = json.load(f) #we get all the json data and stock it in a dictionnary

        self.cplayer = player.Player(save_data) #we create a new player that is going to play

        self.cplayer.load_location_data()
        self.cplayer.load_room_data()
        self.cplayer.load_case_data()
        self.cplayer.load_room_npcs()

        self.game_loop()

    def slow_print(self, text, *text_data):
        '''Function that shows a string character by character'''
        slow_text = True #bool that determines if we show character by character
        number_of_characters = 0
        for i, char in enumerate(text):
            #if the player types space we show all the text without slowing
            if keyboard.is_pressed('space'):
                slow_text = False

            #if it's a case name we start it with an indentation to the left
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
                    os.sys.stdout.write(char) #we show the current character
                    os.sys.stdout.flush()
                    number_of_characters += 1
                else:
                    print(char)
                    print("  |  ", end='')
                    number_of_characters = 0

            if len(text_data) > 1: #if the dev specified how much time between each letter print
                if slow_text:
                    time.sleep(text_data[1]) #we wait for a number of milliseconds
            else: #if the dev didn't specifie how much time between each letter print
                if slow_text:
                    time.sleep(.10)

        print("\n")

    def hud(self):
        '''Method that shows the location and room of the player as well as general infos'''
        print("  ----------------------------------------------------------------------------\n")
        print(f"  |  LOCATION : {self.cplayer.current_location_data['name']}")
        print(f"  |  ROOM : {self.cplayer.current_room_data['name']}")
        print(f"  |  CLUES FOUND : {self.cplayer.data['case data']['clues found']} / {self.cplayer.data['case data']['total clues']}")
        print(f"  |  CASE COMPLETION : {self.cplayer.data['case data']['case completion'] * 10} %\n")
        print("  ----------------------------------------------------------------------------\n")

    def game_loop(self):
        '''The main loop of the game where everything is done'''
        case_name = f"CASE {self.cplayer.data['case']} : {self.cplayer.current_case_data['title']}" #we get the current case name

        os.system("cls")
        print("\n\n\n")
        self.slow_print(case_name, True)
        os.system("pause")

        #if the player has not started the case yet we show him the prologue text
        if not self.cplayer.data['case started']:
            os.system("cls")
            print("  ----------------------------------------------------------------------------\n")
            self.slow_print(self.cplayer.current_case_data['starting text'], False, 0.05)
            print("  ----------------------------------------------------------------------------\n")

            #we set the player has started the chapter so he doesn't see the prologue text again.
            self.cplayer.data['case started'] = True
            os.system("pause")

        while self.state == "Playing":
            os.system("cls")
            if self.cplayer.current_location_data['name'] not in self.cplayer.data['case data']['locations visited']: #add the current location to the visited ones
                self.cplayer.data['case data']['locations visited'].append(self.cplayer.current_location_data['name'])

            self.hud()
            action = input("    What would you like to do ? ") #the action that the player wants to do
            print("")
            self.cplayer.parser.parse(action) #we parse the action the player wants to do
