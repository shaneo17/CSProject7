import json
import random
import time
import os


def main():
    
    n=0
    l=[]
    print("Which game do you want?")
    for i in os.listdir(): 
        if '.json' in i:
            print("  {}. {}".format(n + 1, i))
            n += 1
            l.append(i)
        else:
            pass
    choice= input("> ").lower().strip()
    num = int(choice)-1
    chosengame = l[num]
    with open(str(chosengame)) as fp:
        game = json.load(fp)
    if chosengame == "spooky_mansion.json":
        print_instructions()
        print("Booo! You are about to play '{}'! Good luck, May the odds be ever in your favor!".format(game['__metadata__']['title']))
        print(no_bridges(game))
        print("")
        play(game)
    elif chosengame == "adventure.json":
        print_instructions()
        print("You are about to play '{}'! Good luck, May the odds be ever in your favor!".format(game['__metadata__']['title']))
        print(no_bridges(game))
        print("")
        play(game)
    
def find_non_win_rooms(game):
    keep = []
    for room_name in game.keys():
        # skip if it is the "fake" metadata room that has title & start
        if room_name == '__metadata__':
            continue
        # skip if it ends the game
        if game[room_name].get('ends_game', False):
            continue
        # keep everything else:
        keep.append(room_name)
    return keep

def no_bridges(game):
    for room_name in game:
        if room_name == '__metadata__':
            continue
        room = game[room_name]
        for i in room['exits']:
            e = i['destination']
            #change variable i
            if e in game:
                pass
            if e not in game:
                return False
    return True

        
def play(rooms):
    start = time.perf_counter()
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start']
    # The things the player has collected.
    stuff = ['Cell Phone; no signal or battery...']
    
    
    cat_place = random.choice(find_non_win_rooms(rooms))


    while True:
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        # Print the description.
        print(here["description"])
        
        print("Items for the taking:", here["items"])
        
       
        
        
      
            
        #black cat
        cat_room = rooms[cat_place]
        cat_exit = random.choice(find_non_win_rooms(rooms))
        cat_place = cat_exit
          
        if current_place == cat_place:
            print("There's a black cat in here.")
            cat_place = cat_exit
        
        
       

        # TODO: print any available items in the room...
        
        # e.g., There is a Mansion Key.
        

        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Allow the user to choose an exit:
        usable_exits = find_usable_exits(here, stuff)
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))

        # See what they typed:
        action = input("> ").lower().strip()

        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break
        
        if action == "help":
            print_instructions()
            continue
    

        # TODO: if they type "stuff", print any items they have (check the stuff list!)
        if action == "stuff":
            if len(stuff) > 0:
              print(stuff)
              
            else:
                print("You have no items")
            continue
                
        # TODO: if they type "take", grab any items in the room.
        
        if action == 'take':
            if len(here['items']) == 0:
                print("No items available")
            for i in here['items']:
                stuff.append(i)
                print(stuff)
                here['items'].clear()
            continue
        
        if action == 'drop':
            n = 0
            print("what do you want to drop?")
            for i in range(len(stuff)):
                print("  {}. {}".format(i+1, stuff[n]))
                n += 1
            choice = input("> ").lower().strip()
            num = int(choice) - 1
            selected = stuff[num]
            print("Dropped Item:",selected)
            stuff.pop(num)
            print("Current Items:",stuff)
            here['items'].append(selected)
            continue
                
                
                   
        
        # TODO: if they type "search", or "find", look through any exits in the room that might be hidden, and make them not hidden anymore!
        
        # Try to turn their action into an exit, by number.
        try:
            num = int(action) - 1
            selected = usable_exits[num]
            current_place = selected['destination']
            print("...")
        except:
            print("I don't understand '{}'...".format(action))
        
    print("")
    print("")
    print("=== GAME OVER ===")
    end = time.perf_counter()
    print("you played the game for", end - start, "seconds")
   

def find_usable_exits(room, stuff):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.

    RETURNS
     - a list of exits that are visible (not hidden) and don't require a key!
    """
    usable = []
    for exit in room['exits']:
        if exit.get("hidden", False):
            continue
        if "required_key" in exit:
            if exit["required_key"] in stuff:
                usable.append(exit)
            else:
                print('exit')
            continue
        usable.append(exit)
    return usable

def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print("=== Instructions ===")
    print("")

if __name__ == '__main__':
    main()