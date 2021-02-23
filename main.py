from bs4 import BeautifulSoup
import requests
from tkinter import *
from tkinter import scrolledtext

FONT=("Courier", 10)

######## Scraping ####################################

response = requests.get("https://www.billboard.com/charts/hot-100/2002-01-05")
billboard = response.text

soup = BeautifulSoup(billboard, "html.parser")
song_tags = soup.find_all(name="span", class_="chart-element__information__song")
artist_tags = soup.find_all(name="span", class_="chart-element__information__artist")

song_list_2002 = []
with open("top_100_list.csv", mode="w", encoding="utf-8")as songs:
    for index, song in enumerate(song_tags, start=1):
        song_name = song.getText()
        song_list_2002.append(song_name)
        songs.write(f"{index}: {song_name}\n")

artist_list_2002 = []
for artist in artist_tags:
    artist_name = artist.getText()
    artist_list_2002.append(artist_name)

song_artist_dict = {song_list_2002[i]: artist_list_2002[i] for i in range(len(song_list_2002))}


######## Function #####################################


def selected():

    selected_song = song_choice.get()
    canvas.itemconfig(canvas_text, text=selected_song)
    chosen_artist = song_artist_dict[song_choice.get()]
    canvas.itemconfig(canvas_artist_text, text=chosen_artist)
    LYRICS_END_POINT = "https://api.musixmatch.com/ws/1.1/matcher.lyrics.get"
    LYRICS_API_KEY = "608c60387aa9cc1a76817cafbea5d2c1"
    parameters = {
        "apikey": LYRICS_API_KEY,
        "q_track": song_choice.get(),
        "q_artist": song_artist_dict[song_choice.get()]

    }

    response = requests.get(url=LYRICS_END_POINT, params=parameters)
    response.raise_for_status()
    data = response.json()

    song_lyrics = data["message"]["body"]["lyrics"]["lyrics_body"]
    lyric_box.insert(END, song_lyrics)


def cleared():
    lyric_box.delete("1.0", END)


###############################################################
############ User Interface ###################################
###############################################################

root = Tk()
root.title("Top music in 2002")

root.config(padx=20, pady=50)

########## Frame ##############################################
left_frame = Frame(root)
left_frame.grid(row=0, column=0, padx=20)
right_frame = Frame(root)
right_frame.grid(row=0, column=1)

################## Widget ######################################

canvas = Canvas(left_frame, width=284, height=512)
ipod_img = PhotoImage(file="ipod.png")
canvas.create_image(142, 256, image=ipod_img)
canvas_text = canvas.create_text(142, 110, text="Song", width=230)
canvas_artist_text = canvas.create_text(142, 140, text="Artist", width=230)
canvas.pack()

song_choice = StringVar()
song_choice.set(song_list_2002[0])
drop_menu = OptionMenu(right_frame, song_choice, *song_list_2002)
drop_menu.config(width=40)
drop_menu.grid(row=0, column=0)

select_button = Button(right_frame, text="Select", command=selected)
select_button.grid(row=1, column=0, ipadx=138, pady=10)

lyric_box = scrolledtext.ScrolledText(right_frame,font=FONT, width=40)
lyric_box.grid(row=2, column=0)

button_frame = Frame(right_frame)
button_frame.grid(row=3, column=0)

clear_button = Button(button_frame, text="Clear", command=cleared)
clear_button.grid(row=0, column=0, ipadx=50, padx=(0,30))

close_button = Button(button_frame, text="Close", command=root.destroy)
close_button.grid(row=0, column=1, ipadx=50, pady=10)


root.mainloop()
