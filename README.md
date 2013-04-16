MoodMusic
=========

Playlist generator in Python as part of an Artificial Intelligence class at Northeastern University.

##What is MoodMusic?

We set out to create a playlist-generation application that doesn't rely on meta-data (song, artist, genre), and only uses your own library (unlike Pandora, Last.fm, etc. that are all about music discovery). Genius is one of the only options that uses only your library, but we don't like that it only uses meta-data. We've created an application in which you can create moods ('happy', 'sad', or whatever you'd like) and generates playlists based on the seed songs you add to the mood. 

##How does it work?

It uses [EchoNest](http://echonest.com/)'s API to get numerical representations for songs (such as <em>danceability</em>, <em>loudness</em>, etc.) and populates the DB with your library (which is a very time-consuming process, but worth it in the end!). After adding songs to user-specified moods, you can generate playlists based on a mood, which uses label-spreading machine learning.

##Contributors:
* Tom Weaver
* Behrooz Afghahi
* William Johnston
* Ari Entlich
* Brian Kracoff

##Installation

###1. Install dependencies (if you don't already have them installed)

####a. Python 2.7 (does not work on Python 3)

####b. NumPy and SciPy

Go to the following website for instructions: http://www.scipy.org/Installing_SciPy

####c. SciKit-Learn

    easy_install -U scikit-learn
    
####d. VLC

Install VLC media player at the following website: http://www.videolan.org/vlc/

####e. PyEchoNest

        easy_install -U pyechonest

####f. Marsyas

        See README.marsyas.

###2. Clone repo (or download as a zip)

###3. Run moodmusic.py

Follow setup instructions. Enter your EchoNest API key (or the default one that is given) as well as the full path to your music library xml file or folder.

##Usage (Professors)

###1. Run the following from the moodmusic directory

        ./moodmusic.py --test
        
This will run our test scrip using our test database. There is normally a large startup time since you need to generate a significany DB of songs which takes days depending on your library size. The DB importer runs in the background when you are running the application normally (without the --test argument).

###2. Generate some playlists based on our moods

###3. To test the UI, follow the instructions for "Usage (Anyone)"

##Usage (Anyone)

###1. Run moodmusic.py

        ./moodmusic.py
        
Keep the program running as long as possible because there is a background process that begins adding songs to the DB (which is a VERY time-consuming process). While in the player (options 'a' or 'b') you can type 'd' to see how many songs the importer has added.

###2. Choose an option. We recommend using option 'd' in the beginning to add songs to moods so that you can start generating playlists based on moods.
        
###3. Enjoy!
