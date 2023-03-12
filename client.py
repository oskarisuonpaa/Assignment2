import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:5000/")

def main():
    while(1):
        print("What would you like to do?")
        print("1) Add a new note")
        print("2) Fetch notes by topic")
        print("3) Query Wikipedia")
        print("0) Quit")
        selection = input("Enter your choice: ")

        match selection:
            case "1":
                topicHeading = input("Give the topic heading: ")
                noteHeading = input("Give the note heading: ")
                text = input("Give the note text content: ")

                proxy.addNote(topicHeading, noteHeading, text)
            case "2":
                topicHeading = input("Give the topic heading: ")
                print(f"\n{proxy.fetchByTopic(topicHeading)}")
            case "3":
                searchTerm = input("Give the Wikipedia query search term: ")
                topicHeading = input("Give the topic heading: ")
                result = proxy.queryWikipedia(searchTerm, topicHeading)
                
                if result: print(result)
            case "0":
                print("Thank you for using the program")
                exit(0)
            case _:
                print("Unknown entry, try again")
        print()

main()