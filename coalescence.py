import sqlite3
import shutil
import os
import time
import sys

# Setup File Picker
import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()

# Initial flags
skip_fileSelect = False
skip_Overwrite = False

base_path = None
update_path = None
skip = None
overwrite = None

# Get arguments
arg_amount = len(sys.argv)
   
if arg_amount > 2:
    base_path = sys.argv[1]
    update_path = sys.argv[2]
if arg_amount > 3:
    skip = True if sys.argv[3] == 'skip' else False
if arg_amount > 4:
    overwrite = True if sys.argv[4] == 'overwrite' else False


if arg_amount != 1:
    print("/n---[Arguments Passed]---")

    # Print based on arguments passed
    if update_path is not None:
        print("Base path: " + base_path)
        print("Update path: " + update_path)
        print("Path initialized.")
        skip_fileSelect = True
    
    if skip != None:
        print("Skip confirmations: " + str(skip))
    else:
        skip = False

    if overwrite != None:
        print("Overwrite: " + str(overwrite))


    if skip is not True:
        correct = input("Is the above information correct? y/n   ")
        correct = True if correct.lower()[0] == 'y' else False
        if correct is not True:
            quit()         

# Get the file
if skip_fileSelect is not True:
    input("Press enter key to select your base file.")
    base_path = filedialog.askopenfilename()

    input("Press enter key to select your update file.")
    update_path = filedialog.askopenfilename()

    print("Base file: " + base_path)
    print("Update file: " + update_path)

    if skip is not True:
        wrong = input("All good? y/n   ")
        wrong = wrong.lower()[0]
        print(wrong)
        wrong = False if wrong == 'y' else True

        if wrong:
            # Get the file
            input("Press enter key to select your base file.")
            base_path = filedialog.askopenfilename()

            input("Press enter key to select your update file.")
            update_path = filedialog.askopenfilename()

            wrong = input("All good? y/n   ")
            wrong = wrong.lower()[0]
            print(wrong)
            wrong = False if wrong == 'y' else True

            if wrong:
                print("Quitting program. Figure out what files you want!")
                input()
                quit()



EMPTY = []

# Set up our directory
try:
    print("cleaning dir")
    os.remove("new.sqlite")
except:
    print("dir is already sqeaky clean :D")

# Make our new playsets file
shutil.copyfile(base_path, "new.sqlite")
new_path = "new.sqlite"

# Show that we have connected
print("\n---[Connections]---")
baseconn = sqlite3.connect(base_path)
print("We have connected to base file properly.")
updateconn = sqlite3.connect(update_path)
print("We have connected to update file properly.")



print("\n---[Info]---")

# Save the base playsets
print("Here is the base playsets.")
base_result = baseconn.execute("SELECT * FROM PLAYSETS")
base_names = []
SAVED_base_result = []
for row in base_result:
    SAVED_base_result.append(row)
    name = row[1]
    base_names.append(name)
    print(name)
baseconn.close() # Close to save memory


# Print the update
print("\nHere is the update playsets.")
update_result = updateconn.execute("SELECT * FROM PLAYSETS")
update_names = []
SAVED_update_result = []
for row in update_result:
    SAVED_update_result.append(row)
    name = row[1]
    update_names.append(name)
    print(name)
updateconn.close() # Close to save memory

# Find dupe playsets
dupe_names = []
for update_name in update_names:
    for base_name in base_names:
        if update_name == base_name:
            dupe_names.append(base_name)
            

# Duplicates?
if dupe_names != EMPTY:
    
    print("\n---[Overwrite]---")

    for name in dupe_names:
        print("Duplicate Playset! " + name)
    
    # Ask if they wish to overwrite
    if overwrite is None:
        overwrite = input("Do you wish to overwrite playsets with same name? y/n   ")
        overwrite = overwrite.lower()[0]
        overwrite = True if overwrite == 'y' else False
        print("Overwrite: " + str(overwrite))


    # Dealing with overwrite
    if overwrite:
        print("\n---[overwriting...]---")
        
        while dupe_names != EMPTY:
            for name in dupe_names:

                # Grab our data
                for row in SAVED_update_result:
                    if name in row:
                        data_id = row[0]
                        data_isActive = row[2]
                        data_loadOrder = row[3]

                newconn = sqlite3.connect(new_path)
                    
                updated = newconn.execute(f"UPDATE playsets SET id = '{data_id}', isActive = '{data_isActive}', loadOrder = '{data_loadOrder}' WHERE name = '{name}'")

                newconn.commit()
                    
                newconn.close()

                # Delete the old
                dupe_names.remove(name)
                for row in SAVED_update_result:
                    if name in row:
                        SAVED_update_result.remove(row)

    # Not overwrite
    else:
        print("\n---[skipping...]---")
        for name in dupe_names:
            for row in SAVED_update_result:
                if name in row:
                    SAVED_update_result.remove(row)

# Print current new file
newconn = sqlite3.connect(new_path)
newcon_result = newconn.execute("SELECT * FROM PLAYSETS")
print("\n---[AFTER DEALING WITH SOME DUPLICATION]---")
for row in newcon_result:
    print(row)
newconn.close()

if SAVED_update_result != EMPTY:
    print("\n---[Current Updating File]---")
    for row in SAVED_update_result:
        print(row)
        
else:
    print("\nThe files were the same! Ending program.")
        

# Now to deal with the remaining update_results
# Grab our data
for row in SAVED_update_result:
    data_id = row[0]
    data_name = row[1]
    data_isActive = row[2]
    data_loadOrder = row[3]

    newconn = sqlite3.connect(new_path)
        
    updated = newconn.execute(f"INSERT INTO playsets (id, name, isActive, loadOrder) VALUES ('{data_id}', '{data_name}', '{data_isActive}', '{data_loadOrder}')")

    newconn.commit()
        
    newconn.close()

    SAVED_update_result.remove(row)

        
# Print current new file
newconn = sqlite3.connect(new_path)
newcon_result = newconn.execute("SELECT * FROM PLAYSETS")
print("\n---[AFTER DEALING WITH UPDATE]---")
for row in newcon_result:
    print(row[0])
newconn.close()

# grab base playset mods
print("\n---[Playset Mod Base]---")
baseconn = sqlite3.connect(base_path)
base_playset_mods_result = baseconn.execute("SELECT * FROM playsets_mods")
SAVED_base_playset_mods_result = []
for row in base_playset_mods_result:
    SAVED_base_playset_mods_result.append(row)
baseconn.close() # Close to save memory

# Print the update
print("\n---[Playset Mod Update]---")
updateconn = sqlite3.connect(update_path)
update_result = updateconn.execute("SELECT * FROM playsets_mods")
SAVED_update_playset_mods_result = []
for row in update_result:
    SAVED_update_playset_mods_result.append(row)
updateconn.close() # Close to save memory


# Now lets make sure we have all the playset mods
newconn = sqlite3.connect(new_path)
for row in SAVED_update_playset_mods_result:
    if row not in SAVED_base_playset_mods_result:
        print("new mod")
        print(row)

        playsetid = row[0]
        modid = row[1]
        position = row[2]
        enabled = row[3]

        
        
        updated = newconn.execute(f"INSERT INTO playsets_mods (playsetid, modid, position, enabled) VALUES ('{playsetid}', '{modid}', '{position}', '{enabled}')")

newconn.commit()
newconn.close()                   
                

print("\n DONE ")
