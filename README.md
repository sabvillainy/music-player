# ![sabs-music-player-high-resolution-logo-transparent](https://github.com/user-attachments/assets/fde8bd53-63a5-4b96-bef6-def0d292692f)


Sab's Music Player is a comprehensive music application built with Python. It features a user-friendly interface for managing playlists, favorites, and albums, along with seamless playback functionality. This app leverages Tkinter for the UI and SQLite for database management, offering a robust solution for music lovers.

---

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Panels](#panels)  
   - [Login & Registration Panel](#1-login--registration-panel)
   - [Main Panel](#2-main-panel)
   - [Favorites](#3-favorites)
   - [Album Cover Display](#4-album-cover-display)
5. [Database Structure](#database-structure)  
6. [Setup and Installation](#setup-and-installation)  
7. [Future Enhancements](#future-enhancements)
8. [Contributing](#contributing)

---

## Overview

Sab's Music Player is designed to provide a smooth experience for managing and playing your favorite songs. With intuitive controls and database-backed functionality, the app ensures your music library and preferences are always accessible.

---

## Features

- User authentication with **Login and Registration**.
- **Playlist Management**: Load songs from directories or the database.
- **Favorites**: Save and manage favorite songs.
- **Album Covers**: Dynamic display of album covers or a default image.
- **Seamless Playback**: Play, pause, skip, and rewind tracks.
- **SQLite Database Integration**: Manage users, songs, and favorites efficiently.

---

## Technologies Used

- **Python**
- **Tkinter**: GUI development.
- **Pygame**: Music playback.
- **SQLite3**: Database integration.
- **Pillow**: Image handling for album covers.

---

## Panels

### 1. **Login & Registration Panel**

- The entry point to the application.
- Features:
  - **Login Form**: Users can log in with their credentials.
  - **Registration Form**: New users can create an account.
- Database interaction ensures secure storage and validation of user credentials.

![image](https://github.com/user-attachments/assets/0866f6ba-e0c3-48c0-bc12-1141ed06c855)
![image](https://github.com/user-attachments/assets/415c622c-69f5-4e91-9b6f-19db2942dedd)



### 2. **Main Panel**

- The central hub of the application.
- Features:
  - **Playlist**: Displays the loaded songs with titles.
  - **Control Buttons**:
    - **Play**: Start playing the selected song.
    - **Pause**: Pause the current song.
    - **Next**: Skip to the next track.
    - **Previous**: Return to the previous track.
    - **Favorite**: Save the current song to favorites.
  - **Menu Bar**:
    - **Local Actions**: Load songs from a directory.
    - **Database Actions**: Add songs, load songs, or view favorites from the database.

![image](https://github.com/user-attachments/assets/ae613f48-d0d9-4c8b-84b0-822d0fa28a59)



### 3. **Favorites**

- Manage your favorite songs.
- Features:
  - Displays all saved favorite songs for the logged-in user.
  - Allows playing directly from the favorites list.
  
_Here is UserID = 1's favorite songs:_
  
![image](https://github.com/user-attachments/assets/91936a0a-fe89-4386-a759-1eea288188fb)



### 4. **Album Cover Display**

- Located on the right side of the main panel.
- Dynamically displays:
  - The album cover from the song's folder (`cover.jpg`).
  - A default image if no album cover is found.
  
---

## Database Structure

I used SQLite3 for database integration. Here is my tables:

![image](https://github.com/user-attachments/assets/3f161871-294f-45df-b038-6539a5fef122)

- **Users Table**:
  - Stores user credentials.
  - Fields: `UserID`, `Username`, `Password`.

- **Songs Table**:
  - Tracks information about songs.
  - Fields: `SongID`, `Title`, `Path`, `AlbumID`.

- **Albums Table**:
  - Contains album details.
  - Fields: `AlbumID`, `AlbumName`, `Path`, `Cover`.

- **Favorites Table**:
  - Manages user favorites.
  - Fields: `ID`, `UserID`, `SongID`.

---

## Setup and Installation

### Clone the Repository

```bash
git clone https://github.com/sabvillainy/music-player.git
cd music-player
```

### Install Dependencies 
```bash
pip install pygame pillow
```

**Note:** You need to login first to run the app. So firstly, you need to run login.py and login with a user information that exists in the database. Although, you can register with the "Register from here" button on the panel. And then, you'll be directed to the main app.

---

## Future Enhancements
- Add advanced playlist management features.
- Improve UI/UX with a modern framework like PyQt5.
- Expand the database functionality for better analytics.
- Integrate with online music libraries or APIs (e.g., Spotify API).

---

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.
