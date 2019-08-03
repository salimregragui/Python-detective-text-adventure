'''The npc module'''
import json

class Npc:
    '''the npc class'''
    def __init__(self, name):
        self.name = name #name of the npc
        self.description = "" #his description(exp:clothes/hair/etc)
        self.state = "" #the state of the npc(scared/normal/...)
        self.path = "" #the first available path of talk for the player
        self.paths = [] #all the paths of talk available to the player
        self.requires = None #something required in order to talk to the player

    def load_npc(self, case, current_location):
        '''function that loads all the data of an npc and stores it in the object'''
        npc_file = f"case {case}/location {current_location}/npcs/{self.name}.npc"

        with open(f"cases/{npc_file}", "r") as f:  # we open the file in read mode
            # we get all the json data from the file and stock it in a dictionnary
            self.data = json.load(f)

        self.name = self.data["name"]
        self.description = self.data["description"]
        self.state = self.data["state"]
        self.path = self.data["path"]
        self.paths = self.data["paths"]

        if "requires" in self.data:
            self.requires = self.data["requires"]
