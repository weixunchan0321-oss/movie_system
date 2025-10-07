import re

def customized(text):
    text = re.sub(r"\s+", "", text)
    text = text.strip()
    return text.lower()

def main():
    from main_program.role.clerk import ticketing_clerk_menu
    while True:
        choice = input(
            '--- Main Menu ---\n'
            '1. Ticketing Clerk\n'
            '2. Cinema Manager\n'
            '3. Technician\n'
            '4. Customer\n'
            'Select your role (select via number or roles): '
        )

        choice_customized = customized(choice)

        if choice_customized == '1' or choice_customized == customized('Ticketing Clerk'):
            ticketing_clerk_menu()
        elif choice_customized == '2' or choice_customized == customized('Cinema Manager'):

            pass
        elif choice_customized == '3' or choice_customized == customized('Technician'):

            pass
        elif choice_customized == '4' or choice_customized == customized('Customer'):

            pass
        else:
            print('\nInvalid choice. Please enter again.\n')

if __name__ == '__main__':
    main()