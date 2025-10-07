from main_program.main import main

def ticketing_clerk_menu():
    user_name = login()
    while True:
        print(
            '\n--- Ticketing Clerk Menu ---\n'
            '1. Book Ticket\n'
            '2. Cancel Booking\n'
            '3. View Seating\n'
            '4. Back to Main Menu'
              )
        options = input('Select an option (1 ~ 4): ')
        print()

        if  options == '1':
            booking(user_name)
        elif options == '2':
            cancelling(user_name)
        elif options == '3':
            seating()
        elif options == '4':
            previous_page()
        else:
            print('Invalid choice. Please enter again.')

import re
def customized(movie):
    movie = re.sub(r"\s+", "", movie)
    movie = movie.strip()
    return movie.lower()

import random
def generate_numeric_code(length = 4):
    code = ''.join(str(random.randint(0,9)) for _ in range(length))
    return code

def read_users():
    users = []
    with open('data/ticketing_clerk_menu/user_details.csv', 'r', encoding = 'utf-8') as f:
        header = f.readline()
        for line in f:
            users.append(line.strip().split(','))
    return users

def register(user_name, password):
    with open('data/ticketing_clerk_menu/user_details.csv', 'a', encoding = 'utf-8') as f:
        f.write(f"{user_name},{password}\n")
    print('User',user_name,'registered successfully')

def login():
    while True:
        print('\nWelcome! Please choose:\n1. Log in (If you already have an account)\n2. Register (If you are a new user)\n3. exit (If you select the wrong role)\n* Enter the number or the word')
        selection = input('Your selection: ')
        selection = ''.join(selection.split()).strip().lower()
        if selection == 'login' or selection == 'log in' or selection == '1':
            while True:
                users = read_users()
                user_name = input('\nEnter your name: ')
                password = input('Enter your password: ')
                if [user_name, password] not in users:
                    print('Invalid input, please re-enter.')
                    print('* Please register first if you don\'t have an account')
                    new_input = input('Enter 1 to continue, enter 2 to make a registration: ')
                    if new_input == '1':
                        continue
                    else:
                        while True:
                            user_name = input('\nEnter your name: ')
                            password = input('Enter your password: ')
                            print('Confirm again your name and password')
                            confirmation = input('Enter 1 to confirm, enter 2 to re-enter: ')
                            if confirmation == '1':
                                register(user_name, password)
                                return user_name
                            elif confirmation == '2':
                                continue
                            else:
                                print('Invalid input, please re-enter.')

                while True:
                    verification_code = generate_numeric_code()
                    print('Verification code: ', verification_code)
                    user_input = input('Enter the verification code: ')
                    if user_input != verification_code or user_input == '':
                        print('Wrong input, please re-enter again')
                        continue
                    else:
                        print('Login successful!')
                        return user_name

        elif selection == 'register' or selection == '2':
            while True:
                user_name = input('\nEnter your name: ')
                password = input('Enter your password: ')
                print('Confirm again your name and password')
                confirmation = input('Enter 1 to confirm, enter 2 to re-enter: ')
                if confirmation == '1':
                    register(user_name, password)
                    return user_name
                elif confirmation == '2':
                    continue
                else:
                    print('Invalid input, please re-enter.')

        elif selection == '3' or selection == 'exit':
            print()
            main()

        else:
            print('Invalid input, please re-enter.')

def generate_booking_id(user_name, movie: str, seat: list):
    booking_list = []
    with open('data/ticketing_clerk_menu/customer_bookingID_details.csv', 'r', encoding='utf-8') as f:
        header = f.readline()
        lines = f.read().strip().split('\n')
        for i in lines:
             booking_list.append(i.strip().split(","))

    max_num = 0
    new_id = ""
    for i in booking_list:
        if i[0] == "":
            new_id = 'B01'
        else:
            booking_id_included_b = i[0]
            booking_id = int(booking_id_included_b[1:])
            if booking_id > max_num:
                max_num = booking_id
            new_id = f'B{max_num +1 :02d}'

    row = seat[0]
    column = seat[1]
    with open('data/ticketing_clerk_menu/customer_bookingID_details.csv', 'a', encoding = 'utf-8') as f:
        f.write(f"{new_id},{user_name},{movie},{row},{column}\n")

    return new_id

def cancel_by_booking_id(user_name):
    while True:
        bookings = []
        with open('data/ticketing_clerk_menu/customer_bookingID_details.csv', 'r', encoding = 'utf-8') as f:
            header = f.readline()
            lines = f.read().strip().split('\n')
            for line in lines:
                bookings.append(line.strip().split(','))

        print('* Enter \'exit\' if you choose the wrong option.')
        booking_id_input = input('Enter your booking ID: ')
        if booking_id_input == 'exit':
            return
        else:
            movie_name = ''
            row = -1
            column = -1
            found = False

            # 3. 查找 booking
            for i in range(len(bookings)):
                if bookings[i][0] == booking_id_input and bookings[i][1] == user_name:
                    movie_name = bookings[i][2]
                    row = int(bookings[i][3])
                    column = int(bookings[i][4])
                    found = True
                    bookings.pop(i)  # 删除这条 booking
                    break

            if not found:
                print('Booking ID not found. Please check and try again.')
                continue  # 返回函数

            # 4. 打开对应电影座位表
            seat_file = movie_name.replace(' ', '_') + '_seat.csv'
            with open(f'data/ticketing_clerk_menu/{seat_file}', 'r', encoding = 'utf-8') as f:
                seats = []
                lines = f.read().strip().split('\n')
                for line in lines:
                    seats.append(line.strip().split(','))

            # 5. 取消座位
            seats[row][column] = "0"
            print(f'Seat ({row + 1}, {column + 1}) of {movie_name} has been cancelled successfully.')

            # 6. 写回座位表
            with open(f'data/ticketing_clerk_menu/{seat_file}', 'w', encoding = 'utf-8') as f:
                for seat_row in seats:
                    f.write(','.join(seat_row) + '\n')

            # 7. 写回 bookingID 文件
            with open('data/ticketing_clerk_menu/customer_bookingID_details.csv', 'w', encoding = 'utf-8') as f:
                f.write("BookingID,UserName,MovieName,Row,Column\n")
                for b in bookings:
                    f.write(','.join(b) + '\n')

def input_seat(seats, movie_name: str, user_name: str, price):
    axis_list = []
    while True:
        row = int(input('Please enter the row: ')) - 1
        if row < 0 or row > 6:
            print('Invalid input. Please enter again.')
        else:
            break

    while True:
        column = int(input('Please enter the column: ')) - 1
        if column < 0 or column > 9:
            print('Invalid input. Please enter again.')
        else:
            break

    # 检查是否已被占用

    if seats[row][column] == "X":
        print('This seat is already taken. Please choose another one.')
        return input_seat(seats, movie_name, user_name, price)

    # 修改座位为 "X"
    seats[row][column] = "X"
    axis_list.append(str(row))
    axis_list.append(str(column))
    booking_id = generate_booking_id(user_name, movie_name, axis_list)
    method = payment(user_name, movie_name, row, column, price)
    print(f'Booking complete! Seat ({row + 1}, {column + 1}) of {movie_name} has been reserved successfully.')
    receipt(booking_id, user_name, movie_name, row, column, price, method)

    return seats

def cancel_seat(seats):
    while True:
        row = int(input('Please enter the row: ')) - 1
        if row < 0 or row > 6:
            print('Invalid input. Please enter again.')
        else:
            break

    while True:
        column = int(input('Please enter the column: ')) - 1
        if column < 0 or column > 9:
            print('Invalid input. Please enter again.')
        else:
            break

    # 检查是否已被占用
    if seats[row][column] == "0":
        print("This seat has not been taken yet. Please choose another one.")
        return cancel_seat(seats)
    # 修改座位为 "0"
    seats[row][column] = "0"
    print(f"\nCancelling complete! Seat ({row}, {column}) has been cancelled successfully.")

    return seats

def payment(user_name, movie, row, column, price):
    print("\n--- Payment Section ---")
    print(f"Movie: {movie}")
    print(f"Seat: [{row + 1}, {column + 1}]")
    print(f"Price: RM {price}")

    while True:
        method = input("Enter payment method (cash/card): ").lower().strip()
        if method == "cash":
            while True:
                try:
                    amount = float(input("Enter cash amount: RM "))
                    if amount < price:
                        print("Not enough money, please try again.")
                    else:
                        change = amount - price
                        print(f"\nPayment successful! Change: RM {change:.2f}")
                        return method
                except ValueError:
                    print("Invalid amount, please enter a number.")
        elif method == "card":
            print("Processing payment via card...")
            print("Payment successful!")
            return method
        else:
            print("Invalid method, please enter 'cash' or 'card'.")

def receipt(booking_id, user_name, movie, row, column, price, method):
    print("\n--- Receipt ---")
    print(f"Booking ID : {booking_id}")
    print(f"User       : {user_name}")
    print(f"Movie      : {movie}")
    print(f"Seat       : 【{row + 1},{column + 1}】")
    print(f"Price      : RM {price}")
    print(f"Payment    : {method}")
    print("Thank you for your purchase!\n")

def booking(user_name):
    while True:
        with open('data/ticketing_clerk_menu/movie_details.csv', 'r', encoding = 'utf-8') as f:
            header = f.readline()
            lst = f.read().strip().split("\n")
            data_list = [i.split(',') for i in lst]

        print("--- Available movies ---")
        for movie_info in data_list:
            print(movie_info[0])

        print('* Enter \'exit\' if you select the wrong options')
        movie = input('Select your movie (enter movie\'s name): ')
        movie_customized = customized(movie)
        if movie_customized == 'exit':
            return
        else:
            for movie_info in data_list:
                movie_name = movie_info[0]
                if movie_customized == customized(movie_name):
                    seat_file = movie_name.replace(' ', '_') + '_seat.csv'

                    # 读取 CSV 文件
                    with open(f'data/ticketing_clerk_menu/{seat_file}', 'r', encoding = 'utf-8') as f:
                        lines = f.read().strip().split('\n')

                    # 把每一行转成列表
                    seats = [line.split(",") for line in lines]

                    # 打印当前位置
                    print(f'\nSeating for {movie_name}:')
                    for row in seats:
                        print(' '.join(row))

                    # 调用 input_seat
                    raw_price = movie_info[4]
                    price_str = raw_price.split("RM")[-1].strip()
                    price = float(price_str)
                    seats = input_seat(seats, movie_name, user_name, price)
                    print(f'Updated seating for {movie_name}:')
                    for row in seats:
                        print(' '.join(row))

                    # 把二维列表转回字符串
                    new_lines = [",".join(row_data) for row_data in seats]

                    # 写回文件
                    with open(f'data/ticketing_clerk_menu/{seat_file}', 'w', encoding = 'utf-8') as f:
                        f.write("\n".join(new_lines))
                    return
            else:
                print("Invalid choice. Please enter again.\n")

def cancelling(user_name):
    while True:
        with open('data/ticketing_clerk_menu/movie_details.csv', 'r', encoding='utf-8') as f:
            header = f.readline()
            lst = f.read().strip().split("\n")
            data_list = [i.split(',') for i in lst]

        print("--- Available movies ---")
        for movie_info in data_list:
            print(movie_info[0])

        print('* Enter \'exit\' if you select the wrong options')
        movie = input('Select your movie (enter movie\'s name): ')
        movie_customized = customized(movie)
        if movie == 'exit':
            return
        else:
            valid_movie = False
            for movie_info in data_list:
                movie_name = movie_info[0]
                if movie_customized == customized(movie_name):
                    valid_movie = True
                    cancel_by_booking_id(user_name)
                    return
            if not valid_movie:
                print("Invalid choice. Please enter again.\n")
                return

def seating():
    with open('data/ticketing_clerk_menu/movie_details.csv', 'r', encoding = 'utf-8') as f:
        header = f.readline()
        lst = f.read().strip().split("\n")
        data_list = [i.split(',') for i in lst]

    print("--- Available movies ---")
    for movie_info in data_list:
        print(movie_info[0])

    print('* Enter \'exit\' if you select the wrong options')
    movie = input('Select your movie (enter movie\'s name): ')
    movie_customized = customized(movie)
    if movie == 'exit':
        return
    else:
        for movie_info in data_list:
            movie_name = movie_info[0]
            if movie_customized == customized(movie_name):
                seat_file = movie_name.replace(' ', '_') + '_seat.csv'

                with open(f'data/ticketing_clerk_menu/{seat_file}', 'r', encoding = 'utf-8') as f:
                    lines = f.read().strip().split('\n')

                seats = [line.split(",") for line in lines]

                print(f"\nSeating for {movie_name}:")
                for row in seats:
                    print(" ".join(row))
                return
        else:
            print("Invalid choice. Please enter again.\n")

def previous_page():
    main()