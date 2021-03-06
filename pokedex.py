# This program mimics a pokedex. 
# Search for a gen 1 or 2 pokemon and see what they look like along with their base stats.
# This program will take statistics from a file and convert them into a pokedex.

from tkinter import *
from PIL import Image ,ImageTk
from pygame import mixer
import os
import pdb

IMAGEROOT = 'images'

def main():
    # creating a GUI
    window = Tk()
    window.title('Pokedex')
    window.geometry('700x700')
    window.configure(bg='#f25f5f')
    window.resizable(False, False)
    img = ImageTk.PhotoImage(Image.open(os.path.join(IMAGEROOT, 'pokedex.png')))

    # adding a banner to the pokedex for title
    banner = Label(window, image=img, bg='#f25f5f', padx = 20)
    banner.image = img
    banner.pack()
    
    # opening and reading a file
    infile = open('pokestats.txt', 'r')

    # creating a label
    my_label = Label(window, text="Search for a Generation 1 or 2 Pokemon",
    font=("Times New Roman", 18), fg="black", bg='#f25f5f')
    my_label.pack(pady=20)

    # creating an entry box
    poke_input = Entry(window, font =('Times New Roman', 20))
    poke_input.pack(pady=20)               
    
    # creating the search button and adding a binding functon
    button = Button(window, bd='4', text='Search', fg='black', bg='white', font=("Times New Roman", 14),
    command=lambda: filescanner(pokemon_image, poke_input, ndex, poke_type, poke_hp, 
    poke_atk, poke_def, poke_sp_atk, poke_sp_def, poke_speed))
    button.pack()

    # creating a list box
    my_list = Listbox(window, width=30, height=5, )
    my_list.pack(pady=30, padx=30)

    # create a label for an image
    pokemon_image = Label(window, bg='#f25f5f')
    pokemon_image.pack(side='left', padx=50)
    
      # creating a label for the pokemons speed
    poke_speed = Label(window, bg='#f25f5f')
    poke_speed.pack(side=BOTTOM, pady=5)

    # creating a label for the pokemons special defense 
    poke_sp_def = Label(window,bg='#f25f5f')
    poke_sp_def.pack(side=BOTTOM, pady=5)

    # creating a label for the pokemons special attack
    poke_sp_atk = Label(window,bg='#f25f5f')
    poke_sp_atk.pack(side=BOTTOM, pady=5)

    # creating a label for the pokemons defense 
    poke_def = Label(window,bg='#f25f5f')
    poke_def.pack(side=BOTTOM, pady=5)

    # creating a label for the pokemons attack
    poke_atk = Label(window, bg='#f25f5f')
    poke_atk.pack(side=BOTTOM, pady=5)

    # creating a label for the pokemons HP
    poke_hp = Label(window, bg='#f25f5f')
    poke_hp.pack(side=BOTTOM, pady=5)

    # creating a label for the pokemons type
    poke_type = Label(window, bg='#f25f5f')
    poke_type.pack(side=BOTTOM, pady=5)

    # creating a label for the pokemons pokedex number
    ndex = Label(window, bg='#f25f5f')
    ndex.pack(side=BOTTOM, pady=5)


    # selecting a line in the file
    pokemonlst = []  # create a list of pokemon 
    for line in infile:
        line = line.strip()  # stripping the new line character from the last index
        pokemon = line.split(" ")  # splitting the words in the line
        pokemonlst.append(pokemon[0])  # appending the pokemon name to pokemon list

    # add the pokemon to our list
    update(pokemonlst, my_list)

    # add events
    my_list.bind("<<ListboxSelect>>", lambda evt: fillout(evt, poke_input, my_list))  #create a binding on the listbox onclick
    poke_input.bind("<KeyRelease>", lambda evt: check(evt, poke_input, pokemonlst, my_list))  # create a binding on the enrty box
    window.bind("<Return>", lambda: filescanner(pokemon_image, poke_input, ndex, poke_type, poke_hp, 
    poke_atk, poke_def, poke_sp_atk, poke_sp_def, poke_speed))


    # adding music
    mixer.init()

    # creating 2 music channels
    mixer.set_num_channels(2)
    
    # setting channel 0 to play the lake them
    # channel 1 will be used for a sound effect
    mixer.Channel(0).play(mixer.Sound('laketheme.mp3'), loops = -1)

    # setting the volume of the background music to 40%
    mixer.Channel(0).set_volume(.4)

    # run the main loop
    window.mainloop()

#Function to update the listbox
def update(data, my_list):
    # clear the list box
    my_list.delete(0, END)

    # add pokemon to list box
    for item in data:
        my_list.insert(END, item)

#Function to update the entry box with listbox clicked
def fillout(evt, poke_input, my_list):
    # delete whatever is in the entry box
    poke_input.delete(0, END)

    # add clicked list item to entry box
    poke_input.insert(0, my_list.get(ACTIVE))

#Function to check entry vs listbox
def check(evt, poke_input, pokemonlst, my_list):
    # grab what was typed
    typed = poke_input.get()

    if typed == '':
        data = pokemonlst
    else:
        data = []
        for item in pokemonlst:
            if typed.lower() in item.lower():
                data.append(item)

    # update listbox with selected items
    update(data, my_list)

# file scanner is a function that takes a pokemon name from the user input
# if the user input matches a pokemon it then pulls the information from the txt file
# it updates the image and the stats to match the desired pokemon.
# Function that runs when the button is pressed
def filescanner(pokemon_image, poke_input, ndex, poke_type, poke_hp, 
poke_atk, poke_def, poke_sp_atk, poke_sp_def, poke_speed):

    # plays the select sound effect when search is pressed
    mixer.Channel(1).play(mixer.Sound('selecteffect.mp3'))
    
    # open the file in the function
    file = open('pokestats.txt', 'r')

    # take the user input from the field
    user_input = poke_input.get()
    
    # Loop over the file
    for line in file:

        # stripping the new line character from the last index
        line = line.strip()

        # splitting the words in the line
        pokemon = line.split(" ")

        # If the user input matches the pokemon name update the data
        if pokemon[0].lower() == user_input.lower():

            # creating an empty label field which will display the pokemons image
            png = pokemon[1] + user_input.lower().capitalize() + ".png"
            img = ImageTk.PhotoImage(Image.open(os.path.join(IMAGEROOT, png)).resize((200, 200)))
            pokemon_image.config(image=img)
            pokemon_image.image = img
            ndex.config(text="Pokedex #: " + pokemon[1])
            poke_type.config(text="Primary Type: " + pokemon[2])
            poke_hp.config(text="HP: " + pokemon[3])
            poke_atk.config(text="Attack: " + pokemon[4])
            poke_def.config(text="Defense: " + pokemon[5])
            poke_sp_atk.config(text="Special Attack: " + pokemon[6])
            poke_sp_def.config(text="Special Defense: " + pokemon[7])
            poke_speed.config(text="Speed: " + pokemon[8])

            # changing the font of the stats displayed
            ndex.config(font=("Times New Roman", 10))
            poke_type.config(font=("Times New Roman", 10))
            poke_hp.config(font=("Times New Roman", 10))
            poke_atk.config(font=("Times New Roman", 10))
            poke_def.config(font=("Times New Roman", 10))
            poke_sp_atk.config(font=("Times New Roman", 10))
            poke_sp_def.config(font=("Times New Roman", 10))
            poke_speed.config(font=("Times New Roman", 10))
if __name__ == "__main__":
    main()