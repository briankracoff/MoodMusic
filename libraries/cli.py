#! /usr/bin/python

from vlc import *
import ctypes
from ctypes.util import find_library
import os
import sys
from collections import OrderedDict

# Used by EventManager in override.py
from inspect import getargspec

try:
    from msvcrt import getch
except ImportError:
    import termios
    import tty

echo_position = False

def getch():  # getchar(), getc(stdin)  #PYCHOK flake
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch

def end_callback(event):
    print('End of media stream (event %s)\n' % event.type)
    sys.exit(0)

def pos_callback(event, player):
    if echo_position:
        sys.stdout.write('\rPosition in song: %.2f%%' % (player.get_position() * 100))
        sys.stdout.flush()

def print_version():
    """Print libvlc version"""
    try:
        print('Build date: %s (%#x)' % (build_date, hex_version()))
        print('LibVLC version: %s (%#x)' % (bytes_to_str(libvlc_get_version()), libvlc_hex_version()))
        print('LibVLC compiler: %s' % bytes_to_str(libvlc_get_compiler()))
        if plugin_path:
            print('Plugin path: %s' % plugin_path)
    except:
        print('Error: %s' % sys.exc_info()[1])

def print_info():
    """Print information about the media"""
    try:
        print_version()
        media = player.get_media()
        print('State: %s' % player.get_state())
        print('Media: %s' % bytes_to_str(media.get_mrl()))
        print('Current time: %s/%s' % (player.get_time(), media.get_duration()))
        print('Position: %s' % player.get_position())
       #print('Window:' % player.get_hwnd()
    except Exception:
        print('Error: %s' % sys.exc_info()[1])

def print_menu():
    """Print menu"""
    print('Single-character commands:')
    for k, m in keybindings.items():
        if(k != '?'):
            m = (m.__doc__ or m.__name__).splitlines()[0]
            print('  %s: %s.' % (k, m.rstrip('.')))
    print('0-9: go to that fraction of the movie')

def quit_app():
    """Stop and exit"""
    sys.exit(0)

#Toggles whether the current position of the song should be shown
def toggle_echo_position():
    """Toggle echoing of media position"""
    global echo_position
    echo_position = not echo_position

#Navigates to the portion of the song desired
#portion - must be a single digit, 0 through 9
def jump_to_position(portion):
    if k.isdigit():
        player.set_position(float('0.'+portion))

#Go to next track in playlist
def next_track():
    """Go to next track in playlist"""

#Open a new track to play
def play_different_track():
    """Play a different track"""
    
#Add the current track to a user-inputted mood
def add_to_mood():
    """Add track to one of your moods"""

if sys.argv[1:] and sys.argv[1] not in ('-h', '--help'):

    song = os.path.expanduser(sys.argv[1])
    if not os.access(song, os.R_OK):
        print('Error: %s file not readable' % movie)
        sys.exit(1)

    instance = Instance("--sub-source marq")
    try:
        media = instance.media_new(song)
    except NameError:
        print('NameError: %s (%s vs LibVLC %s)' % (sys.exc_info()[1], __version__, libvlc_get_version()))
        sys.exit(1)
    player = instance.media_player_new()
    player.set_media(media)
    player.play()

    # Some event manager examples.  Note, the callback can be any Python
    # callable and does not need to be decorated.  Optionally, specify
    # any number of positional and/or keyword arguments to be passed
    # to the callback (in addition to the first one, an Event instance).
    event_manager = player.event_manager()
    event_manager.event_attach(EventType.MediaPlayerEndReached,      end_callback)
    event_manager.event_attach(EventType.MediaPlayerPositionChanged, pos_callback, player)

    #Constant keybindings for menu
    keybindings = OrderedDict()
    keybindings.setdefault(' ', player.pause)
    keybindings.setdefault('m', add_to_mood)
    keybindings.setdefault('i', print_info)
    keybindings.setdefault('p', toggle_echo_position)
    keybindings.setdefault('n', play_different_track)
    keybindings.setdefault('>', next_track)
    keybindings.setdefault('q', quit_app)
    keybindings.setdefault('?', print_menu)

    print('Press q to quit, ? to see menu.%s' % os.linesep)
    while True:
        k = getch()
        print('> %s' % k)
        if k in keybindings:
            keybindings[k]()
        elif k.isdigit():
            # jump to fraction of the song.
            jump_to_position(k)

else:
    print('Usage: %s <movie_filename>' % sys.argv[0])
    print('Once launched, type ? for the menu.')
    print('')
    print_version()