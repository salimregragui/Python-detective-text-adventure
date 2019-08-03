'''Parsing module'''
from difflib import get_close_matches
import random
import os
import json
import time
import keyboard


class Parser:
    '''Hello'''

    def __init__(self, cplayer):

        self.sentence = ""
        self.old_sentences = []
        self.available_actions = ["get", "take",
                                  "look", "go", "help", "analyse", "minimap", "clues", "save", "quit", "talk", "notes", "inventory"]
        self.exception_words = ["the", "than", "and", "then", "to", "on", "of"]
        self.old_sentences_pointer = len(self.old_sentences) - 1
        self.cplayer = cplayer

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

    def normalized_print(self, text, slow=False):
        '''function that prints text with bars on top and bottom'''

        if not slow:
            print(
                "\n  ----------------------------------------------------------------------------\n")
            print(f"{text}\n")
            print(
                "  ----------------------------------------------------------------------------\n")

        else:
            print(
                "  ----------------------------------------------------------------------------\n")
            self.slow_print(
                f"{text}", False, 0.02)
            print(
                "  ----------------------------------------------------------------------------\n")

    def show_minimap(self):
        '''Function that shows the map of the current location of the player'''

        os.system("cls")
        # we open the map file in read mode
        with open(f"cases/case {self.cplayer.data['case']}/location {self.cplayer.data['current location']}/minimap.map", "r") as f:
            # we get all the lines from the file
            minimap = f.readlines()

        print("\n\n")
        self.normalized_print(
            f"    MAP OF THE LOCATION : {self.cplayer.current_location_data['name']}")

        for i, line in enumerate(minimap):  # showing the minimap line by line
            print(f"\t\t{line}")
            time.sleep(.1)

        self.normalized_print(
            f"    YOU ARE CURRENTLY IN THE : {self.cplayer.current_room_data['name']}")

    def show_clues(self):
        '''Function that shows all the clues that the player has found'''
        os.system("cls")

        self.normalized_print(f"    CLUES FOUND ON THE CURRENT CASE")

        # if the player found at least one clue
        if self.cplayer.data["clues found"]:
            for i, clue in enumerate(self.cplayer.data["clues found"]):
                self.slow_print(f"CLUE {i+1} : {clue}", False, 0.01)
                print(
                    "  ----------------------------------------------------------------------------\n")
        else:
            self.normalized_print(f"    YOU HAVENT FOUND A SINGLE CLUE YET.")

    def show_inventory(self):
        '''Function that shows all the objects in the players inventory'''
        os.system("cls")

        self.normalized_print(f"    OBJECTS FOUND ON THE CURRENT CASE")

        # if the player found at least one clue
        if self.cplayer.data["inventory"]:
            for i, obj in enumerate(self.cplayer.data["inventory"]):
                self.slow_print(f"OBJECT {i+1} : {obj}", False, 0.01)
                print(
                    "  ----------------------------------------------------------------------------\n")
        else:
            self.normalized_print("   YOU HAVENT FOUND A SINGLE OBJECT YET.\n")

    def talk_to_npc(self, name):
        '''Method that allows the player to talk to a npc'''
        os.system("cls")
        name = name.lower()  # we put the name entered by the player to lowercase

        # we set all the names of the npcs in the room to lower in a list
        lowered_npc_names_list = [
            npc.lower() for npc in self.cplayer.current_room_data["npcs in room"]]

        if name in lowered_npc_names_list:  # if the name entered by the player is in the room
            # we go throught all the npcs of the room
            for i, npc in enumerate(self.cplayer.current_room_npcs):
                if npc.name.lower() == name:  # once we find the npc the player wants to talk to we add his data to a variable
                    npc_to_talk_to = npc

            current_path = None  # this will determine wich text to show to the player from the npc

            # we go throught the list of all the npcs the player already talked to
            for i, n in enumerate(self.cplayer.data["npcs talked to"]):
                # if we find the name of the npc the player is currently talking to
                if n["name"] == npc_to_talk_to.name:
                    # we resume the path where the player was
                    current_path = n["current path"]
                    # we resume the current state of the npc
                    current_state = n["state"]

            if not current_path or current_path == "None":  # if the player never talked to the npc before
                current_path = npc_to_talk_to.path  # we set the path to the first one
                current_state = npc_to_talk_to.state  # we set the state to the first one

            # if the player has done what is required to talk to the npc
            player_has_achieved_required = True

            if npc_to_talk_to.requires:  # if the npc has a requirement in order to talk to him.
                player_has_achieved_required = False
                if "npc" in npc_to_talk_to.requires:  # if the npc requires the player to have talked to another npc
                    # we go throught the list of all the npcs the player already talked to
                    for i, n in enumerate(self.cplayer.data["npcs talked to"]):
                        # if we find the name of the npc the player is currently talking to
                        if n["name"] == npc_to_talk_to.requires["npc"]:
                            player_has_achieved_required = True

                # if the npc requires the player to have a certain object.
                elif "object" in npc_to_talk_to.requires:
                    # we go throught the list of all the objects the player has
                    for i, obj in enumerate(self.cplayer.data["inventory"]):
                        # if we find the name of the npc the player is currently talking to
                        if obj == npc_to_talk_to.requires["object"]:
                            player_has_achieved_required = True

            if npc_to_talk_to.requires and not player_has_achieved_required:
                # if the player hasn't achieved the requirement to talk to the npc
                self.normalized_print(
                    f"{npc_to_talk_to.name} is not here for the moment.\nCome back later maybe you could find him.", True)
                return 0
            else:

                save_npc_to_data = {
                    "current path": current_path,
                    "name": npc_to_talk_to.name,
                    "state": npc_to_talk_to.state
                }

                while True:
                    if current_path != "None":  # if there are still texts to show to the player
                        # we go throught all the paths of the npc
                        for i, path in enumerate(npc_to_talk_to.paths):
                            if current_path in path:  # we find the current path index
                                path_playing = i

                        self.normalized_print(
                            f"{npc_to_talk_to.paths[path_playing][current_path]}", True)

                        # variable that stocks all the data of the current path in wich the player is
                        answers = npc_to_talk_to.paths[path_playing]

                        # if the current path gives the player a clue
                        if "clue" in answers and answers["clue"] not in self.cplayer.data['clues found']:
                            self.cplayer.add_clue(answers["clue"])

                        print("POSSIBLE ANSWERS : \n")

                        # we go throught all the possible answers to the path the player is in
                        for i, answer in enumerate(answers["possible answers"]):
                            self.normalized_print(
                                f"{answer['new state']} : {answer['answer']}", True)

                        # the user chooses one of the responses available
                        choice = input("WHAT'S YOUR CHOICE :")
                        choice = choice.strip()  # removing all the trailing white spaces

                        # we go throught all the possible answers to the path the player is in
                        for i, answer in enumerate(answers["possible answers"]):
                            # if the choice of the player is in the possible choices
                            if answer["new state"].lower() == choice.lower():
                                # we set the current path to the next path.
                                current_path = answer["path"]

                        os.system("cls")
                    else:  # if there are no texts left for the player
                        self.normalized_print("End of conversation !", True)
                        save_npc_to_data["current path"] = current_path
                        save_npc_to_data["state"] = npc_to_talk_to.state

                        self.cplayer.data["npcs talked to"].append(
                            save_npc_to_data)  # we add the npc to the talked to npc's
                        break

        else:  # if the person typed by the player isn't here.
            self.normalized_print(
                "The person you want to talk to is not here !", True)

    def execute(self, action):
        # all the actions possible in the current room
        possible_actions = self.cplayer.current_room_data['possible actions']
        # list of objects in the room
        objects_in_room = self.cplayer.current_room_data['objects in room']

        with open(f"global_actions.data", "r") as f:  # we open the file in read mode
            # we get all the global actions from the file
            global_actions = json.load(f)

        # we add to the possible actions all the global actions
        possible_actions = possible_actions + global_actions['global actions']

        # the name of the action the player wants to do
        action_name = action[0]

        if(len(action) >= 1):  # if there is at least one action

            if action[0] == "minimap":  # if the player wants to see the minimap
                self.show_minimap()
                return 0

            if action[0] == "clues":  # if the player wants to see the clues he found
                self.show_clues()
                return 0

            if action[0] == "inventory":
                self.show_inventory()

                return 0

            if action[0] == "save":
                self.cplayer.save_game()
                self.normalized_print("GAME SAVED SUCCESSFULLY !", True)

                return 0

            if action[0] == "notes":
                self.cplayer.show_notes()
                return 0

            if action[0] == "talk" and len(action) >= 2:
                action.pop(0)
                npc_name = " ".join(action)
                self.talk_to_npc(npc_name)

                return 0

            if action[0] == "quit":
                self.cplayer.save_game()
                os.sys.exit(
                    "THIS IS THE END OF YOUR GAME SESSION GOODBYE ! SEE YOU SOON ;)")

            # this dictionnary will store all the action finishes of the action the player chose if it's available
            action_data = {}
            first = True  # if we are in the first dictionnary element

            # looking in the possible actions of the room for the action the user wants to do
            for i, dic in enumerate(possible_actions):
                # if the action typed by the player is found and it's the first element
                if dic['action'] == action_name and first:
                    action_data = dic  # the action dictionnary is the current dictionnary
                    first = False
                # if the action typed by the player is found and it's not the first element
                elif dic['action'] == action_name and not first:
                    # we update the action finishes to includes those of this dictionnary I added all of this to be able to have actions both in a room and in global actions
                    action_data["action finish"].update(dic['action finish'])

            if action_data:  # if the action that the user wants to do is there than we are ok
                # we select only the action finish of the selected action
                action_data = action_data['action finish']
            else:
                self.normalized_print(
                    "You can't do this action in here !", True)
                return False

            # we join the entire sentence the user typed
            full_action = " ".join(action)
            obj = {}  # this is going to contain the object that has the action typed by the player if it's there

            # we search all the objects in the room
            for i, dic in enumerate(objects_in_room):
                # if one of them needs the actions put by the player
                if dic['action needed'] == full_action:
                    obj = dic  # we stock that object

            # we remove the first word of the list of actions in here "look"
            action.pop(0)
            # we join all the words left in list_of_actions appart from the first word
            join_list = " ".join(action)

            if not join_list:  # if the player typed an action without anything left exemple typed just look
                # we select a random response if the action is unavailable.
                response = random.choice(action_data['empty'])
                self.normalized_print(f"{response}", True)

            # if the joined sentence is a key of the action_data dictionnary
            if join_list in action_data and join_list[0] != '$':
                # if the action shows something from the room data
                if action_data[join_list][0] == '$':
                    what_to_print = self.cplayer.current_room_data[action_data[join_list][1:len(
                        action_data[join_list])]]  # we remove the '$' and find the key of the room dictionnary

                else:  # if the action only shows what's in it's dictionnary
                    what_to_print = action_data[join_list]

                self.normalized_print(what_to_print, True)

            # if the action finish that the user has chosen is unavailable in finishes of the room
            elif join_list and join_list not in action_data:

                # if the action has something to print in the case of unavailable action finish
                if "none of the above" in action_data:
                    # we select a random response if the action is unavailable.
                    response = random.choice(action_data['none of the above'])

                else:
                    response = "I don't understand what you mean...I'm sorry !"

                self.normalized_print(f"{response}", True)

            if obj:  # if we found an object that needs the action put by the player
                os.system("pause")
                os.system("cls")
                # we print all the texts of the object
                for i, text in enumerate(obj['texts']):
                    self.normalized_print(f"{text}", True)

                note = {
                    "name": obj['name'],
                    "texts": obj['texts']
                }

                # if the player doesn't have this note already
                if note not in self.cplayer.data['notes']:
                    self.cplayer.add_note(note)

                # if the player doesn't have this clue already
                if obj["clue"] and obj["clue"] not in self.cplayer.data['clues found']:
                    self.cplayer.add_clue(obj['clue'])

                # if the player doesn't have the object already and the object can be stored we add it to his inventory
                if obj["name"] not in self.cplayer.data["inventory"] and obj["storable"]:
                    self.normalized_print(
                        f"NEW OBJECT ADDED TO YOUR INVENTORY : {obj['name'].upper()}", True)
                    self.cplayer.data["inventory"].append(obj["name"])

                if "requires" in obj:  # if the object requires something before happening
                    act = input("What would you like to do ?")
                    act = act.strip()  # we remove all the trailing white spaces

                    # if the action typed by the player is the one needed to activate this path
                    if act == obj["requires"]["action"]:
                        # if the object requires the player to have another object
                        if "object" in obj["requires"]:
                            # if the player has the required object
                            if obj["requires"]["object"] in self.cplayer.data["inventory"]:
                                # we show the texts of the required object
                                for i, text in enumerate(obj['requires']["texts"]):
                                    self.normalized_print(f"{text}", True)

                                # if the requires option has a clue.
                                if obj["requires"]["clue"] and obj["requires"]["clue"] not in self.cplayer.data['clues found']:
                                    self.cplayer.add_clue(
                                        obj["requires"]['clue'])

                                note = {
                                    "name": obj['requires']["action"],
                                    "texts": obj["requires"]['texts']
                                }

                                # if the player doesn't have this note already
                                if note not in self.cplayer.data['notes']:
                                    self.cplayer.add_note(note)
                            else:
                                self.normalized_print(
                                    "IT APPEARS YOU ARE MISSING SOMETHING TO DO THIS.\nLET'S KEEP LOOKING AROUND.", True)
                    else:
                        self.normalized_print(
                            "YOUR ACTION HAS NO EFFECT", True)

        else:
            self.normalized_print(
                f"You didn't specify something after the action {action_name}", True)

    def parse(self, user_action):
        '''function that parses a sentence typed by the player'''
        if user_action:  # if the user typed something

            user_action = user_action.lower()  # we set all the words to lowercase
            user_action = user_action.strip()  # we remove all the trailing white spaces

            # we add the action to the actions typed by the user
            self.old_sentences.append(user_action)

            # we create a list of all the words in the sentence
            list_of_actions = user_action.split(" ")

            # we remove all the exception words
            list_of_actions = [word for word in list_of_actions if word not in self.exception_words]

            if list_of_actions[0] in self.available_actions: #if the action typed by the player is a possible one
                self.execute(list_of_actions)

            else:
                self.normalized_print(
                    f"I don't understand your action did you mean '{get_close_matches(list_of_actions[0],self.available_actions)}..", True)

            os.system("pause")
            return True

        else:
            self.normalized_print(
                "You need to type an action in order to do something duh :)", True)
            os.system("pause")
            return True
