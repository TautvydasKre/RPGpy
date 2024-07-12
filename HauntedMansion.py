import random
import tkinter as tk
from tkinter import messagebox, Toplevel

# Define the rooms and their connections
rooms = {
    "Foyer": {"description": "A dimly lit foyer with cobwebs everywhere. There are doors to the north, east, and west.", "north": "Living Room", "east": "Library", "west": "Dining Room"},
    "Living Room": {"description": "An old living room with dusty furniture. There's a creepy painting on the wall. Doors lead to the south, east, and north.", "south": "Foyer", "east": "Kitchen", "north": "Bathroom"},
    "Library": {"description": "A dark library filled with ancient books. There's a strange whispering sound. Doors lead to the west and north.", "west": "Foyer", "north": "Study"},
    "Kitchen": {"description": "A kitchen with rusty appliances. You hear faint footsteps. Doors lead to the west and north.", "west": "Living Room", "north": "Pantry"},
    "Study": {"description": "A small study room. There's a flickering candle on the desk. Doors lead to the south and east.", "south": "Library", "east": "Master Bedroom"},
    "Dining Room": {"description": "An elegant dining room with a long table. The chandelier above swings slightly. Doors lead to the east and north.", "east": "Foyer", "north": "Pantry"},
    "Pantry": {"description": "A cramped pantry filled with old canned goods. There's an eerie silence. Doors lead to the south and west.", "south": "Kitchen", "west": "Dining Room"},
    "Master Bedroom": {"description": "A large bedroom with a grand bed. The windows are boarded up. Doors lead to the west and north.", "west": "Study", "north": "Bathroom"},
    "Bathroom": {"description": "A dirty bathroom with a cracked mirror. There's a chilling draft. Doors lead to the south and east.", "south": "Living Room", "east": "Master Bedroom"},
    "Backyard": {"description": "A spooky backyard with overgrown weeds. There's a small shed to the north.", "north": "Shed", "south": "Foyer"},
    "Basement": {"description": "A dark, damp basement. You can hear dripping water. Stairs lead up to the Kitchen.", "up": "Kitchen"},
    "Tunnel": {"description": "A narrow tunnel with a musty smell. It seems to lead somewhere deeper.", "north": "Hidden Chamber", "south": "Basement"},
    "Shed": {"description": "A small shed with gardening tools. There's a trapdoor leading down.", "down": "Tunnel", "south": "Backyard"},
    "Hidden Chamber": {"description": "A hidden chamber with ancient relics. This seems like the heart of the haunted mansion.", "south": "Tunnel"}
}

# Define items and their locations with purposes
items = {
    "Library": {"name": "Ancient Book", "effect": "knowledge"},
    "Kitchen": {"name": "Rusty Key", "effect": "unlock"},
    "Study": {"name": "Old Map", "effect": "map"},
    "Dining Room": {"name": "Silver Knife", "effect": "weapon", "strength": 5},
    "Pantry": {"name": "Health Potion", "effect": "heal", "heal_amount": 20},
    "Master Bedroom": {"name": "Golden Locket", "effect": "defense", "defense": 5},
    "Backyard": {"name": "Shovel", "effect": "dig"},
    "Basement": {"name": "Torch", "effect": "light"}
}

# Define enemies and their locations
enemies = {
    "Living Room": {"name": "Ghost", "health": 20, "strength": 5},
    "Library": {"name": "Zombie", "health": 30, "strength": 10},
    "Kitchen": {"name": "Ghoul", "health": 25, "strength": 7},
    "Master Bedroom": {"name": "Vampire", "health": 50, "strength": 15},
    "Backyard": {"name": "Werewolf", "health": 40, "strength": 12},
    "Basement": {"name": "Goblin", "health": 20, "strength": 5},
    "Tunnel": {"name": "Spider", "health": 15, "strength": 4},
    "Shed": {"name": "Ogre", "health": 35, "strength": 10},
    "Hidden Chamber": {"name": "Lich", "health": 60, "strength": 20}
}

# Initialize player state with levels and experience
player = {
    "health": 100,
    "strength": 10,
    "defense": 0,
    "level": 1,
    "experience": 0,
    "class": None,
    "skills": [],
    "inventory": {}
}

# Define classes and their skills
classes = {
    "Warrior": {"strength": 5, "defense": 3, "skills": ["Power Strike", "Block"]},
    "Mage": {"strength": 2, "defense": 1, "skills": ["Fireball", "Heal"]},
    "Rogue": {"strength": 4, "defense": 2, "skills": ["Backstab", "Stealth"]}
}

# Initialize game state
current_room = "Foyer"

def update_description():
    room = rooms[current_room]
    description.set(f"You are in the {current_room}. {room['description']}")

    if current_room in items:
        item = items[current_room]
        item_label.set(f"You see a {item['name']} here.")
        take_button.pack()  # Show the take button if there's an item
    else:
        item_label.set("")
        take_button.pack_forget()  # Hide the take button if there's no item

    if current_room in enemies:
        enemy = enemies[current_room]
        enemy_label.set(f"A {enemy['name']} is here! It looks hostile.")
        enemy_health_label.set(f"Enemy Health: {enemy['health']}")
        attack_button.pack()  # Show the attack button if there's an enemy
    else:
        enemy_label.set("")
        enemy_health_label.set("")
        attack_button.pack_forget()  # Hide the attack button if there's no enemy

    player_health_label.set(f"Your Health: {player['health']}")
    player_stats_label.set(f"Level: {player['level']} | Strength: {player['strength']} | Defense: {player['defense']} | Class: {player['class']}")

    # Manage directional buttons based on room connections
    if "north" in room:
        move_north_button.pack()
    else:
        move_north_button.pack_forget()

    if "east" in room:
        move_east_button.pack()
    else:
        move_east_button.pack_forget()

    if "south" in room:
        move_south_button.pack()
    else:
        move_south_button.pack_forget()

    if "west" in room:
        move_west_button.pack()
    else:
        move_west_button.pack_forget()

    if "up" in room:
        move_up_button.pack()
    else:
        move_up_button.pack_forget()

    if "down" in room:
        move_down_button.pack()
    else:
        move_down_button.pack_forget()

    update_inventory()

def move(direction):
    global current_room
    room = rooms[current_room]
    if direction in room:
        current_room = room[direction]
        update_description()
    else:
        messagebox.showinfo("Movement", "You can't go that way.")

def take_item():
    if current_room in items:
        item = items[current_room]
        player['inventory'][item['name']] = item
        messagebox.showinfo("Item Taken", f"You took the {item['name']}.")
        del items[current_room]
        update_description()
    else:
        messagebox.showinfo("Item", "There's no item to take here.")

def attack_enemy():
    if current_room in enemies:
        enemy = enemies[current_room]
        player_damage = random.randint(1, player['strength'])
        enemy['health'] -= player_damage
        if enemy['health'] <= 0:
            messagebox.showinfo("Combat", f"You defeated the {enemy['name']}!")
            player['experience'] += 10
            level_up()
            del enemies[current_room]
            update_description()
        else:
            enemy_damage = max(0, random.randint(1, enemy['strength']) - player['defense'])
            player['health'] -= enemy_damage
            if player['health'] <= 0:
                messagebox.showinfo("Game Over", "You have been defeated. Game over!")
                root.quit()
            else:
                messagebox.showinfo("Combat", f"You attack the {enemy['name']} for {player_damage} damage!\nThe {enemy['name']} attacks you for {enemy_damage} damage!")
            update_description()
    else:
        messagebox.showinfo("Combat", "There's no enemy to attack here.")

def flee():
    global current_room
    current_room = "Foyer"
    update_description()
    messagebox.showinfo("Flee", "You flee back to the Foyer.")

def enemy_attack():
    if current_room in enemies:
        enemy = enemies[current_room]
        enemy_damage = max(0, random.randint(1, enemy['strength']) - player['defense'])
        player['health'] -= enemy_damage
        if player['health'] <= 0:
            messagebox.showinfo("Game Over", "You have been defeated. Game over!")
            root.quit()
        else:
            messagebox.showinfo("Enemy Attack", f"The {enemy['name']} attacks you for {enemy_damage} damage!")
            update_description()

def check_inventory():
    inventory_window = Toplevel(root)
    inventory_window.title("Inventory")
    tk.Label(inventory_window, text="Your Inventory:", font=("Arial", 16)).pack()
    inventory_frame = tk.Frame(inventory_window)
    inventory_frame.pack()
    for item_name, item in player['inventory'].items():
        btn = tk.Button(inventory_frame, text=item_name, command=lambda i=item_name: use_item(i))
        btn.pack(side=tk.LEFT)

def use_item(item_name):
    item = player['inventory'][item_name]
    if item['effect'] == "heal":
        player['health'] = min(100, player['health'] + item['heal_amount'])
        del player['inventory'][item_name]
        messagebox.showinfo("Item Used", f"You used the {item_name} and restored {item['heal_amount']} health.")
    elif item['effect'] == "weapon":
        player['strength'] += item['strength']
        del player['inventory'][item_name]
        messagebox.showinfo("Item Used", f"You equipped the {item_name} and increased your strength by {item['strength']}.")
    elif item['effect'] == "defense":
        player['defense'] += item['defense']
        del player['inventory'][item_name]
        messagebox.showinfo("Item Used", f"You equipped the {item_name} and increased your defense by {item['defense']}.")
    elif item['effect'] == "map":
        show_map()
    update_description()

def show_map():
    map_window = Toplevel(root)
    map_window.title("Map")
    tk.Label(map_window, text="Map of the Haunted Mansion", font=("Arial", 16)).pack()
    tk.Label(map_window, text="Foyer - Living Room - Bathroom\nLibrary - Study - Master Bedroom\nKitchen - Pantry\nDining Room\nBackyard - Shed - Tunnel - Hidden Chamber").pack()

def update_inventory():
    for widget in inventory_frame.winfo_children():
        widget.destroy()
    for item_name, item in player['inventory'].items():
        btn = tk.Button(inventory_frame, text=item_name, command=lambda i=item_name: use_item(i))
        btn.pack(side=tk.LEFT)

def choose_class(class_name):
    player['class'] = class_name
    player['strength'] += classes[class_name]['strength']
    player['defense'] += classes[class_name]['defense']
    player['skills'] = classes[class_name]['skills']
    update_description()
    class_window.destroy()
    messagebox.showinfo("Class Chosen", f"You have chosen the {class_name} class!")

def level_up():
    if player['experience'] >= player['level'] * 10:
        player['level'] += 1
        player['strength'] += 2
        player['health'] = 100  # Restore health on level up
        messagebox.showinfo("Level Up!", f"You have reached level {player['level']}! Strength increased to {player['strength']}.")

def show_character():
    char_window = Toplevel(root)
    char_window.title("Character Stats")
    tk.Label(char_window, text="Character Stats", font=("Arial", 16)).pack()
    tk.Label(char_window, text=f"Class: {player['class']}").pack()
    tk.Label(char_window, text=f"Level: {player['level']}").pack()
    tk.Label(char_window, text=f"Strength: {player['strength']}").pack()
    tk.Label(char_window, text=f"Defense: {player['defense']}").pack()
    tk.Label(char_window, text=f"Health: {player['health']}").pack()
    tk.Label(char_window, text=f"Experience: {player['experience']}").pack()
    tk.Label(char_window, text="Skills:").pack()
    for skill in player['skills']:
        tk.Label(char_window, text=skill).pack()

def choose_class_window():
    global class_window
    class_window = Toplevel(root)
    class_window.title("Choose Class")
    tk.Label(class_window, text="Choose Your Class", font=("Arial", 16)).pack()
    for class_name in classes.keys():
        btn = tk.Button(class_window, text=class_name, command=lambda c=class_name: choose_class(c))
        btn.pack()

def end_game():
    if not enemies:
        messagebox.showinfo("Congratulations!", "You have defeated all enemies and won the game!")
        root.quit()

# Create the main window
root = tk.Tk()
root.title("Haunted Mansion RPG")

# Create the description label
description = tk.StringVar()
tk.Label(root, textvariable=description, wraplength=400).pack()

# Create the item label
item_label = tk.StringVar()
tk.Label(root, textvariable=item_label).pack()

# Create the enemy label
enemy_label = tk.StringVar()
tk.Label(root, textvariable=enemy_label).pack()

# Create the player health label
player_health_label = tk.StringVar()
tk.Label(root, textvariable=player_health_label).pack()

# Create the enemy health label
enemy_health_label = tk.StringVar()
tk.Label(root, textvariable=enemy_health_label).pack()

# Create the player stats label
player_stats_label = tk.StringVar()
tk.Label(root, textvariable=player_stats_label).pack()

# Create the action buttons
move_north_button = tk.Button(root, text="Move North", command=lambda: move("north"))
move_north_button.pack()

move_east_button = tk.Button(root, text="Move East", command=lambda: move("east"))
move_east_button.pack()

move_south_button = tk.Button(root, text="Move South", command=lambda: move("south"))
move_south_button.pack()

move_west_button = tk.Button(root, text="Move West", command=lambda: move("west"))
move_west_button.pack()

move_up_button = tk.Button(root, text="Move Up", command=lambda: move("up"))
move_up_button.pack()

move_down_button = tk.Button(root, text="Move Down", command=lambda: move("down"))
move_down_button.pack()

take_button = tk.Button(root, text="Take Item", command=take_item)
take_button.pack()

attack_button = tk.Button(root, text="Attack Enemy", command=attack_enemy)
attack_button.pack()

flee_button = tk.Button(root, text="Flee to Foyer", command=flee)
flee_button.pack()

inventory_button = tk.Button(root, text="Inventory", command=check_inventory)
inventory_button.pack()

character_button = tk.Button(root, text="Character", command=show_character)
character_button.pack()

choose_class_window()

inventory_frame = tk.Frame(root)
inventory_frame.pack()

# Initialize the game description
update_description()

# Check for end game conditions
root.after(100, end_game)  # Check every 100ms for end game conditions

# Run the main loop
root.mainloop()
