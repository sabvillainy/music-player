from tkinter import filedialog, Tk, Menu, Listbox, PhotoImage, Button, Frame, END, messagebox, simpledialog
from tkinter import *
from PIL import Image, ImageTk
import pygame
import sqlite3
import os

root = Tk()
root.title("Sab's Music Player")
root.geometry("660x350+{}+{}".format((root.winfo_screenwidth() - 660) // 2, (root.winfo_screenheight() - 350) // 2))
root.iconbitmap("images/icon.ico")
root.resizable(False,False)

pygame.mixer.init()

DB_NAME = 'music-player.db'

def get_db_connection():
    return sqlite3.connect(DB_NAME)

# Şarkılar listesi ve oynatma durumu değişkenleri
songs = []
currentSong = ""
paused = False

current_user_id = int(os.getenv('USER_ID', -1))  # Giriş yapmış kullanıcı ID'si
if current_user_id == -1:
    messagebox.showerror("Error", "User not logged in!")
    root.destroy()


def add_to_favorites():
    global currentSong, current_user_id
    if not current_user_id:
        messagebox.showerror("Error", "No user is logged in.")
        return

    if not currentSong:
        messagebox.showerror("Error", "No song is currently playing.")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # şarkının ID'sini al
        cursor.execute("SELECT SongID FROM Songs WHERE Path = ?", (currentSong,))
        song = cursor.fetchone()

        if song:
            song_id = song[0]
            cursor.execute("SELECT * FROM Favorites WHERE SongID = ? AND UserID = ?", (song_id, current_user_id))
            already_favorite = cursor.fetchone()

            if not already_favorite:
                cursor.execute("INSERT INTO Favorites (SongID, UserID) VALUES (?, ?)", (song_id, current_user_id))
                conn.commit()
                messagebox.showinfo("Success", "Song added to your favorites!")
            else:
                messagebox.showwarning("Warning", "Song is already in your favorites.")
        else:
            messagebox.showerror("Error", "Current song is not in the database.")


    except Exception as e:
        print("Error adding to favorites:", e)
    finally:
        conn.close()


def load_favorites():
    global current_user_id
    if not current_user_id:
        print("No user is logged in.")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT Songs.Title, Songs.Path
            FROM Favorites
            INNER JOIN Songs ON Favorites.SongID = Songs.SongID
            WHERE Favorites.UserID = ?
        """, (current_user_id,))
        rows = cursor.fetchall()

        songlist.delete(0, END)
        songs.clear()

        for title, path in rows:
            songlist.insert(END, title)
            songs.append(path)

        print("Favorites loaded successfully.")
    except Exception as e:
        print("Error loading favorites:", e)
    finally:
        conn.close()


def update_album_cover(song_path):
    """Albüm kapağını gösterir veya default resim kullanır."""
    try:
        cover_path = os.path.join(os.path.dirname(song_path), "cover.jpg")
        if os.path.exists(cover_path):
            image = Image.open(cover_path).resize((243, 243))
        else:
            image = Image.open("images/default_cover.jpg").resize((243, 243))

        album_cover = ImageTk.PhotoImage(image)
        cover_label.config(image=album_cover)
        cover_label.image = album_cover
    except Exception as e:
        print("Error loading album cover:", e)


# Şarkı oynatma fonksiyonu
def playMusic():
    global currentSong, paused
    try:
        if not paused:
            selected_index = songlist.curselection() #mevcut seçili şarkıyı bulur
            if selected_index:
                currentSong = songs[selected_index[0]]
                pygame.mixer.music.load(currentSong)
                pygame.mixer.music.play()
                update_album_cover(currentSong)
        else:
            pygame.mixer.music.unpause()
            paused = False
    except Exception as e:
        print("Error playing music:", e)


def pauseMusic():
    global paused
    try:
        pygame.mixer.music.pause()
        paused = True
    except Exception as e:
        print("Error pausing music:", e)


def nextMusic():
    try:
        index = songlist.curselection()[0]
        songlist.selection_clear(index)
        songlist.selection_set(index + 1)
        playMusic()
    except IndexError:
        print("Reached end of playlist.")


def prevMusic():
    try:
        index = songlist.curselection()[0]
        songlist.selection_clear(index)
        songlist.selection_set(index - 1)
        playMusic()
    except IndexError:
        print("Reached start of playlist.")


def loadMusic():
    global currentSong
    directory = filedialog.askdirectory()
    if not directory:
        return

    songlist.delete(0, END)  # Listeyi temizle
    songs.clear()

    for song in os.listdir(directory):
        name, ext = os.path.splitext(song)
        if ext == '.mp3':
            song_path = os.path.join(directory, song)
            songs.append(song_path)
            songlist.insert(END, name)

    if songs:
        songlist.selection_set(0)
        currentSong = songs[0]


def add_song():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        song_path = filedialog.askopenfilename(initialdir="C:/", title="Choose a Song",
                                               filetypes=[("MP3 Files", "*.mp3")])
        if not song_path:
            return

        album_path = os.path.dirname(song_path)
        album_name = os.path.basename(album_path)
        song_title = os.path.splitext(os.path.basename(song_path))[0]
        cover_path = os.path.join(album_path, "cover.jpg")

        cursor.execute("SELECT AlbumID FROM Albums WHERE AlbumName = ?", (album_name,))
        album = cursor.fetchone()

        if album:
            album_id = album[0]
        else:
            cursor.execute("INSERT INTO Albums (AlbumName, Path, Cover) VALUES (?, ?, ?)",
                           (album_name, album_path, cover_path))
            album_id = cursor.lastrowid

        cursor.execute("INSERT INTO Songs (Title, Path, AlbumID) VALUES (?, ?, ?)", (song_title, song_path, album_id))
        conn.commit()

        songlist.insert(END, song_title)
        songs.append(song_path)
    except Exception as e:
        print("Error adding song:", e)
    finally:
        conn.close()


def load_songs_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Songs.Title, Songs.Path FROM Songs")
        rows = cursor.fetchall()

        songlist.delete(0, END)
        songs.clear()

        for title, path in rows:
            songlist.insert(END, title)
            songs.append(path)
    except Exception as e:
        print("Error loading songs:", e)
    finally:
        conn.close()


cover_label = Label(root)
cover_label.place(x=400, y=8)

songlist = Listbox(root, bg="black", fg="white", width=62, height=15, selectbackground="gray", selectforeground="black")
songlist.place(x=10, y=10)

controlFrame = Frame(root)
controlFrame.place(x=230, y=265)

playButtonImg = PhotoImage(file='images/play.png')
pauseButtonImg = PhotoImage(file='images/pause.png')
nextButtonImg = PhotoImage(file='images/next.png')
prevButtonImg = PhotoImage(file='images/previous.png')
favoriteButtonImg = PhotoImage(file='images/favorite.png')

playButton = Button(controlFrame, image=playButtonImg, borderwidth=0, command=playMusic)
pauseButton = Button(controlFrame, image=pauseButtonImg, borderwidth=0, command=pauseMusic)
nextButton = Button(controlFrame, image=nextButtonImg, borderwidth=0, command=nextMusic)
prevButton = Button(controlFrame, image=prevButtonImg, borderwidth=0, command=prevMusic)
favoriteButton = Button(controlFrame, image=favoriteButtonImg, borderwidth=0,command=add_to_favorites)

playButton.grid(row=0, column=2, padx=7, pady=10)
pauseButton.grid(row=0, column=1, padx=7, pady=10)
nextButton.grid(row=0, column=3, padx=7, pady=10)
prevButton.grid(row=0, column=0, padx=7, pady=10)
favoriteButton.grid(row=0,column=4,padx=7,pady=10)

menubar = Menu(root)
root.config(menu=menubar)

organiseMenu = Menu(menubar, tearoff=False)
organiseMenu.add_command(label='Select Folder', command=loadMusic)
menubar.add_cascade(label='Local Actions', menu=organiseMenu)

dbMenu = Menu(menubar, tearoff=False)
dbMenu.add_command(label="My Favorites", command=load_favorites)
dbMenu.add_command(label="Add Song", command=add_song)
dbMenu.add_command(label="Load Songs", command=load_songs_from_db)
menubar.add_cascade(label="Database Actions", menu=dbMenu)


root.mainloop()