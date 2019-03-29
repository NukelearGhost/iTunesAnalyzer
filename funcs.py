import plistlib
import os
import re
import logging
import matplotlib.pyplot as plt
import numpy as np
from iTunes_Analyzer import main


def loadplist():
    """

        Loads the plist file into memory

    """

    clear()

    # Find iTunes file(s) if in same directory as iTunes_Analyzer.py
    foundfiles = []  # List to store the names of found .xml files.

    logging.debug("Searching current directory for .xml files.")
    for file in os.listdir('./'):
        # If the file ends with .xml add the filename to the foundfiles list.
        if re.search('(?:xml)', file):
            logging.debug("Found {}".format(file))
            foundfiles.append(file)

    # If there is one or more item in found files, display a list of files to the user and allow them to select a file
    # or leave blank to specify a file.
    if len(foundfiles) > 0:
        print("Found the following .xml files: \n")
        for file in foundfiles:
            # Add 1 to the actual index to make the list begin at 1
            print("{}) {}".format(foundfiles.index(file)+1, file))

        selection = input("\n Select the number corresponding to the file you would like to analyze, or leave blank "
                          "to specify a different file: ")

        # If selection is blank, prompt for path to specified playlist file.
        if not selection:
            filepath = input("\nEnter the path to your playlist file: ")

            # Check if the specified file actually exists.
            while not os.path.isfile(filepath):
                filepath = input("\n[FILE NOT FOUND] Enter the path to your playlist file: ")

            try:
                # Load the file
                logging.debug("Attempting to load playlist file {}".format(filepath))
                pl = open(filepath, 'br')
                playlist = plistlib.load(pl)
                logging.debug("Playlist loaded successfully!")
                # Return playlist to caller
                return playlist
            except Exception as E:
                print("Error loading file, try again.")
                logging.warning("Error loading playlist file. ERROR INFO: {}".format(E))

        else:
            # Subtract 1 from the selection so it matches the actual index of the selected item.
            selection = int(selection) - 1

            try:
                # Load the file
                logging.debug("Attempting to load playlist file ./{}".format(foundfiles[selection]))
                pl = open(foundfiles[selection], 'br')
                playlist = plistlib.load(pl)
                logging.debug("Playlist loaded successfully!")
                # Return playlist to caller
                return playlist
            except Exception as E:
                print("Error loading file, try again.")
                logging.warning("Error loading playlist file. ERROR INFO: {}".format(E))

    clear()


def tracksbyyear(plist):
    '''

    Counts the number of tracks by year
    plots to a graph and outputs the
    graph (matplotlib) and table (stdout)

    '''

    clear()
    # Pull track info from plist file
    tracks = plist['Tracks']

    # Store track years in a set and list to be used later.
    yearsx = set()
    yearsy = []
    for trackId, track in tracks.items():
        yearsx.add(track['Year'])
        yearsy.append(track['Year'])

    # Generate a list of years and a list of counts
    years = []
    counts = []

    for yearx in yearsx:
        years.append(yearx)
        counts.append(yearsy.count(yearx))

    # Plot data to graph

    # Plot config
    plt.title("Tracks by Year")
    plt.xlabel("Count of Tracks", fontsize=10)
    plt.ylabel("Years", fontsize=10)
    x_pos = np.arange(len(years))

    # Bar Graph
    plt.bar(x_pos, counts, align='center')
    plt.xticks(x_pos, years)
    plt.tick_params(labelsize=8, axis='both')
    plt.xticks(rotation=90)

    # Table
    yeardata = zip(years, counts)
    print("\n      Raw Data        \n")
    print("    Years    Count   ")
    for y, c in yeardata:
        print("    {}       {}    ".format(y, c))

    plt.show()

    input("Press any key to continue...")
    main(plist)

def toptwenty(plist):
    '''

    Print a list of the top 20 most played songs in the library

    '''

    clear()

    # Pull track info from plist file
    tracks = plist['Tracks']

    # Store track name and number of plays in dictionary
    trackinfo = {}
    for trackId, track in tracks.items():
        try:
            if track.get('Play Count'):
                trackinfo[track['Name']] = track['Play Count']

        except:
            logging.warning("Could not find play count for {}".format(track['Name']))
            pass

    x = 0

    print("\nYour top 20 played songs are: \n")

    # Print the name and number of plays of 20 most played songs.
    while x < 20:

        # Pull the name of the longest from from trackinfo{}
        toptrack = max(trackinfo, key=trackinfo.get)

        # Print the number of the song (1 = most played), name, and number of plays
        print("{}) {} {}".format(x+1, toptrack, trackinfo.get(toptrack)))

        # Remove the most played track from trackinfo{}
        del trackinfo[toptrack]

        x += 1

    input("Press any key to continue...")
    main(plist)

def lonshort(plist):
    '''

    Print top 25 longest tracks from longest song to shortest song

    '''

    clear()

    # Pull track info from plist file
    tracks = plist['Tracks']

    # Store track name and total time in dictionary
    trackinfo = {}
    for trackId, track in tracks.items():
        try:
            if track.get('Total Time'):
                trackinfo[track['Name']] = track['Total Time']

        except Exception as E:
            logging.warning("Could not find track length for {}. ERROR DETAILS: {}".format(track['Name'], E))
            pass

    x = 0
    # Print the top 100 longest songs from longest to shortest
    while x < 25:
        # Grab the name of the longest track from trackinfo{}
        lontrack = max(trackinfo, key=trackinfo.get)

        # Grab the time of the longest track from trackinfo{} and format to minutes:seconds
        time = trackinfo.get(lontrack) / 1000
        time = round(time, 2)
        minutes = int(time / 60)
        seconds = int(time - (minutes * 60))
        time = "{}:{}".format(minutes, seconds)

        # Pad ones place with zero if nothing else present
        if len(time) <= 3:
            time = time + "0"

        # Print the number of the song (1 = longest), name, and number of plays
        print("{}) {} {}".format(x+1, lontrack, time))

        # Delete track from trackinfo{}
        del trackinfo[lontrack]

        x += 1

    input("Press any key to continue...")
    main(plist)

def mostskipped(plist):
    '''

    Print top 25 most skipped songs.

    '''

    clear()

    # Pull track info from plist file
    tracks = plist['Tracks']

    # Store track name and number of skips in dictionary
    trackinfo = {}
    for trackId, track in tracks.items():
        try:
            if track.get('Skip Count'):
                trackinfo[track['Name']] = track['Skip Count']

        except Exception as E:
            logging.warning("Could get skip count for {}. ERROR DETAILS: {}".format(track['Name'], E))
            pass

    x = 0

    while x < 25:
        # Grab the most skipped song from trackinfo{}
        topskip = max(trackinfo, key=trackinfo.get)

        # Print the number of the song (1 = most skipped), name, and number of plays
        print("{}) {} {}".format(x + 1, topskip, trackinfo.get(topskip)))

        # Delete longest song from trackinfo{}
        del trackinfo[topskip]

        x += 1

    input("Press any key to continue...")
    main(plist)


def countgenre(plist):
    '''

    Counts the number of tracks by year
    plots to a graph and outputs the
    graph (matplotlib) and table (stdout)

    '''

    clear()

    # Pull track info from plist file
    tracks = plist['Tracks']

    # Store track genre in a set.
    genresx = set()
    genresy = []

    for trackId, track in tracks.items():
        genresx.add(track['Genre'])
        genresy.append(track['Genre'])

    genres = []
    counts = []

    for genrex in genresx:
        genres.append(genrex)
        counts.append(genresy.count(genrex))

    # Plot data to graph

    # Plot config
    plt.title("Tracks by Genre")
    plt.xlabel("Genres", fontsize=10)
    plt.ylabel("Years", fontsize=10)
    x_pos = np.arange(len(genres))

    # Bar Graph
    plt.bar(x_pos, counts, align='center')
    plt.xticks(x_pos, genres)
    plt.tick_params(labelsize=8, axis='both')
    plt.xticks(rotation=90)

    # Table
    genredata = zip(genres, counts)
    print("\n      Raw Data        \n")
    print("    Years    Count   ")
    for g, c in genredata:
        print("    {}       {}    ".format(g, c))

    plt.show()

    input("Press any key to continue...")
    main(plist)


def counttracks(plist):
    '''

    Counts the number of tracks in
    the given plist

    '''

    clear()

    # Pull track info from plist file
    tracks = plist['Tracks']

    # Store track genre in a set.

    x = 0

    for trackId, track in tracks.items():
        x += 1

    return x


def songsbylength(plist):
    '''

    Plots the length of all tracks.

    '''

    clear()

    # Pull track info from plist file
    tracks = plist['Tracks']

    # Store track lengths
    tracklengths = []
    unqtracklengths = set()

    for trackId, track in tracks.items():
        time = track['Total Time']
        if time:
            time = time / 1000
            time = round(time, 2)
            minutes = int(time / 60)
            tracklengths.append(minutes)
            unqtracklengths.add(minutes)

    n = max(unqtracklengths)
    unqtracklengths = []

    for num in range(0, n+1):
        unqtracklengths.append(num)

    counts = []

    for unqlength in unqtracklengths:
        counts.append(tracklengths.count(unqlength))

    # Plot data to graph

    # Plot data to graph

    # Plot config
    plt.title("Tracks by Length")
    plt.xlabel("Length of Tracks (mins)", fontsize=10)
    plt.ylabel("Count of Tracks", fontsize=10)
    x_pos = np.arange(len(unqtracklengths))

    # Bar Graph
    plt.bar(x_pos, counts, align='center')
    plt.xticks(x_pos, unqtracklengths)
    plt.tick_params(labelsize=8, axis='both')

    # Table
    lendata = zip(unqtracklengths, counts)
    print("\n      Raw Data        \n")
    print("    Length    Count   ")
    for l, c in lendata:
        print("      {}         {}    ".format(l, c))

    plt.show()

    input("Press any key to continue...")
    main(plist)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
