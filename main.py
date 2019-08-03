import os
import gameManager

game = gameManager.GameManager()
choice = 0

print("Menu :")
print("1. NEW GAME")
print("2. LOAD GAME")
print("3. QUIT")

while choice != "1" and choice != "2" and choice != "3":
    choice = input("CHOICE : ")
    if choice != "1" and choice != "2" and choice != "3":
        print("PLEASE ENTER A VALID CHOICE !")

if choice == "1":
    game.new_game()

elif choice == "2":
    game.load_game()

elif choice == "3":
    os.sys.exit("GOODBYE :)")
