import funcs as f
import logging

logging.basicConfig(filename="iTunes_Analyzer.log",
                    filemode='a',
                    format='%(asctime)s (%(levelname)s):  %(message)s',
                    datefmt='%d %b %y %H:%M:%S',
                    level=logging.DEBUG)


def main(playlist):

    if not playlist:
        print("///////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
        print("|       iTunes Analyzer     |")
        print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\//////////////")

        print("\nLet's load in an iTunes playlist file!\n")

        playlist = f.loadplist()

    f.clear()
    print("///////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
    print("|       iTunes Analyzer     |")
    print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\//////////////")

    print("\nYour playlist includes {} songs.\n".format(f.counttracks(playlist)))

    print("1) Tracks by year released               5) Count of songs by genre")
    print("2) Top twenty most played tracks         6) Count of songs by length")
    print("3) Top 25 longest songs by length        7) Load different playlist file")
    print("4) Top 25 most skipped songs             8) Exit\n\n")

    selection = input("Type your selection and press enter: ")

    while True:
        if selection == "1":
            f.tracksbyyear(playlist)
        elif selection == "2":
            f.toptwenty(playlist)
        elif selection == "3":
            f.lonshort(playlist)
        elif selection == "4":
            f.mostskipped(playlist)
        elif selection == "5":
            f.countgenre(playlist)
        elif selection == "6":
            f.songsbylength(playlist)
        elif selection == "7":
            playlist = []
            main(playlist)
        elif selection == "8":
            exit(0)
        else:
            selection = input("[INVALID INPUT] Type your selection and press enter: ")


if __name__ == '__main__':
    main("")
