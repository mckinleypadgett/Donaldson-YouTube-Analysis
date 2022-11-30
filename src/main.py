#from data_collection import youtube_data
from data_collection import selection

def main():
    choice = -1

    while (choice != 0):
        MainMenu()
        
        choice = input("What would you like to do? ")

        if choice == "1":
           print("You have chosen to gather data")
           selection.main()
        elif choice == "2":
           print("You have chosen to run sentiment analyzer")
        elif choice == "3":
           print("You have chosen to view results")
        elif choice == "0":
            break

    
    return

def MainMenu():
    print("Main Menu:")
    print("1. Gather Data")
    print("2. Run Sentiment Analysis")
    print("3. View Results")
    print("0. Exit")

    return

if __name__ == '__main__':
    main()
