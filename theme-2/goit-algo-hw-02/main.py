
def main():
    while True:
        print("\n************ MENU ************")
        print("1. Message Broker")
        print("2. Palindrome checker")
        print("3. Delimiters checker")
        print('0. Exit')
        print("******************************")
        choice = input("Select an option: ")
        if choice == "1":
            from sources.messages_broker import MessageBroker

            broker = MessageBroker()
            broker.start()

            print("Press Any Key to Stop...")
            input()

            broker.stop()
        elif choice == "2":
            from sources.palindrome import is_palindrome

            user_string = input("Enter a string: ")
            if is_palindrome(user_string):
                print("The string is a palindrome.")
            else:
                print("The string is not a palindrome.")
        elif choice == "3":
            from sources.delimiters_checker import check_delimiters

            user_sequence = input("Enter a sequence with delimiters: ")
            result = check_delimiters(user_sequence)
            print(f"Delimiter check result: {result}")
        elif choice == "0":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

        input("Press any key to continue...")


if __name__ == "__main__":
    main()
