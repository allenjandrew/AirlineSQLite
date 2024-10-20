import sqlite3

DATABASE_FILE = "air_travel.db"


def main():

    print("\nWelcome to the Air Travel Database!")

    logged_in = False
    while not logged_in:
        print("\nOptions: 1. Log in, 2. Create a new account, 3. Exit")
        choice = input("What would you like to do? ")
        if choice == "1":
            cust_id = log_in()
            logged_in = True
        elif choice == "2":
            cust_id = create_customer()
            logged_in = True
        elif choice == "3":
            quit()

    # Options: book a flight, search for flights, view your trips (get total flight time; get total cost), cancel trip, change active customer, update customer details, create a new customer, exit

    show_options()

    while True:
        choice = input("\nWhat would you like to do? (Enter 0 to view options): ")
        if choice == "0":
            show_options()
        elif choice == "1":
            # book_flight()
            not_implemented()
        elif choice == "2":
            # search_flights()
            not_implemented()
        elif choice == "3":
            view_my_trips(cust_id)
        elif choice == "4":
            cancel_trip(cust_id)
        elif choice == "5":
            cust_id = log_in()
        elif choice == "6":
            update_customer(cust_id)
        elif choice == "7":
            cust_id = create_customer()
        elif choice == "8":
            break


def log_in():
    """
    Log in to the database. Takes no arguments; all input comes directly from the user. Makes its own connection to the database. Returns the unique primary key id of the customer as an int.
    """
    while True:
        (first_name, last_name) = get_first_last_names()

        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()
        cursor.execute(
            "select id from customers where first_name =:c and last_name =:d",
            {"c": first_name, "d": last_name},
        )
        searcher = cursor.fetchall()

        if len(searcher) == 1:
            return searcher[0][0]

        elif len(searcher) > 1:
            id_num = input("Enter your ID number (letters and digits only): ").upper()
            cursor.execute(
                "select id from customers where first_name =:c and last_name =:d and id_num =:e",
                {"c": first_name, "d": last_name, "e": id_num},
            )
            return cursor.fetchone()[0]

        else:
            print("No customer found with that name")


def create_customer():
    """
    Create a new customer in the database. Takes no arguments; all input comes directly from the user. Makes its own connection to the database. Returns the unique primary key id of the new customer as an int.
    """
    first_name, last_name = get_first_last_names()

    email = get_email()

    phone = get_phone()

    id_num = get_id_num()

    dob = get_dob()

    address = input("Enter your address: ")

    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    cursor.execute(
        "insert into customers (first_name, last_name, email, phone, id_num, dob, address) values (?, ?, ?, ?, ?, ?, ?)",
        (first_name, last_name, email, phone, id_num, dob, address),
    )
    cursor.execute(
        "select id from customers where first_name =:c and last_name =:d and dob =:e and id_num =:f",
        {"c": first_name, "d": last_name, "e": dob, "f": id_num},
    )
    custid = cursor.fetchone()[0]

    connection.commit()
    connection.close()

    return custid


def show_options():
    """
    Prints the main menu options. Nothing more.
    """
    print(
        "\nOptions: 1. book a flight, 2. search for flights, 3. view your trips, 4. cancel trip, 5. change active customer, 6. update customer details, 7. create a new customer, 8. exit"
    )


def view_my_trips(cust_id):
    """
    View a customer's trips in the database. Takes the unique primary key id of the customer as an int. Makes its own connection to the database. Uses the sum() SQLite aggregate function. Does not return anything.
    """

    print()
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    cursor.execute(
        "select * from trips where customer_id =:c",
        {"c": cust_id},
    )
    trip_searcher = cursor.fetchall()

    if len(trip_searcher) == 0:
        print("\nYou have no trips booked.\n")
        connection.close()
        return

    cursor.execute(
        "select sum(duration) from flights where id in (select flight_id from trips where customer_id =:c)",
        {"c": cust_id},
    )
    total_time = convert_mins_to_hhmm(cursor.fetchone()[0])

    cursor.execute(
        "select sum(price) from trips where customer_id =:c",
        {"c": cust_id},
    )
    total_cost = cursor.fetchone()[0]

    connection.close()

    trips = []

    for trip in trip_searcher:

        flight = fetch_one("flights", trip[2])

        airline = fetch_one("airlines", flight[2])[1]

        origin_airport = fetch_one("airports", flight[3])[2]

        dest_airport = fetch_one("airports", flight[4])[2]

        aircraft = fetch_one("aircrafts", flight[5])[2]

        trips.append(
            (
                trip[0],  # trip.id
                origin_airport,  # flight.origin_airport.iata
                flight[6],  # flight.depart_time
                dest_airport,  # flight.dest_airport.iata
                flight[7],  # flight.arrive_time
                convert_mins_to_hhmm(flight[8]),  # flight.duration
                trip[3],  # trip.seat_num
                trip[4],  # trip.seat_class
                airline,  # airline.name
                flight[1],  # flight.flight_num
                aircraft,  # aircraft.model
                trip[5],  # trip.price
            )
        )

    trips.sort(key=lambda x: x[2])  # sort by departure datetime

    for trip in trips:
        print()
        print(f"\nTrip ID: {trip[0]}")
        print(f"Depart from {trip[1]} on {trip[2]}")
        print(f"Arrive at {trip[3]} on {trip[4]}")
        print(f"Flight time: {trip[5]}")
        print(f"Seat number: {trip[6]} {trip[7]} class")
        print(f"{trip[8]} flight number {trip[9]}")
        print(f"Aircraft model: {trip[10]}")
        print(f"Price: ${trip[11]}")
        print()

    print()
    print(f"Total flight time: {total_time}")
    print(f"Total cost: ${total_cost}")
    print()


def fetch_one(table, unique_id):
    """
    Fetch one row from a table in the database. Takes the table name as a string and the unique primary key id as an int. Makes its own connection to the database. Returns the row as a tuple.
    """
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    cursor.execute(
        f"select * from {table} where id =:c",
        {"c": unique_id},
    )
    row = cursor.fetchone()

    connection.close()

    return row


def cancel_trip(cust_id):
    """
    Cancel a trip in the database. Takes the unique primary key id of the customer as an int. Makes its own connection to the database. Does not return anything.
    """

    done = False
    while not done:
        choice = input(
            "\nEnter the ID of the trip you would like to cancel (enter 'trips' to view trips): "
        ).strip()

        if choice == "trips":
            view_my_trips(cust_id)
            continue

        if not choice.isdigit():
            print("Invalid trip ID. Please try again.")
            continue

        choice = int(choice)

        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        cursor.execute(
            "select * from trips where customer_id =:c and id =:d",
            {"c": cust_id, "d": choice},
        )
        trip_searcher = cursor.fetchall()

        if len(trip_searcher) == 1:
            cursor.execute(
                "delete from trips where id =:d",
                {"d": choice},
            )
            connection.commit()
            connection.close()
            done = True
            print("Trip successfully cancelled.")

        else:
            print("Invalid trip ID. Please try again.")
            connection.close()


def update_customer(cust_id):
    """
    Update a customer's details in the database. Takes the unique primary key id of the customer as an int. Does not return anything.
    """

    print(
        "Available fields: 1. first name, 2. last name, 3. email, 4. phone, 5. ID number, 6. date of birth, 7. address"
    )
    choice = input("What field would you like to update? ")

    if choice == "1" or choice == "2":
        first_name, last_name = get_first_last_names()
        update_field("customers", "first_name", first_name, cust_id)
        update_field("customers", "last_name", last_name, cust_id)

    elif choice == "3":
        email = get_email()
        update_field("customers", "email", email, cust_id)

    elif choice == "4":
        phone = get_phone()
        update_field("customers", "phone", phone, cust_id)

    elif choice == "5":
        id_num = get_id_num()
        update_field("customers", "id_num", id_num, cust_id)

    elif choice == "6":
        dob = get_dob()
        update_field("customers", "dob", dob, cust_id)

    elif choice == "7":
        address = input("Enter your address: ")
        update_field("customers", "address", address, cust_id)


def update_field(table, field, value, unique_id):
    """
    Update a `field` in a `table`. Takes the table name as a string, the field name as a string, the new value as a string, and the unique primary key id as an int. Makes its own connection to the database. Does not return anything.
    """
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    cursor.execute(
        f"update {table} set {field} =:c where id =:d",
        {"c": value, "d": unique_id},
    )

    connection.commit()
    connection.close()


def get_first_last_names():
    """
    Get first and last names from user, with validity checks. Returns the first and last names as a tuple of strings.
    """
    names_okay = False
    while not names_okay:
        names = input("Enter your first and last name: ").strip()
        names = [x.capitalize() for x in names.split()]

        names_okay = True
        if len(names) == 2:
            (first_name, last_name) = names
        elif len(names) == 3:
            (given_name, middle_name, last_name) = names
            first_name = f"{given_name} {middle_name}"
        elif len(names) == 4:
            (given_name, middle_name, surname_1, surname_2) = names
            first_name = f"{given_name} {middle_name}"
            last_name = f"{surname_1} {surname_2}"
        else:
            names_okay = False

    return (first_name, last_name)


def get_email():
    """
    Get email from user, with validity checks. Returns the email as a string.
    """
    email_okay = False
    while not email_okay:
        email = input("Enter your email address: ")
        if email.count("@") == 1 and "." in email.split("@")[1]:
            email_okay = True
        else:
            print("Invalid email address")

    return email


def get_phone():
    """
    Get phone number from user, with validity checks. Returns the phone number as a 10-digit string.
    """
    phone_okay = False
    while not phone_okay:
        phone = input("Enter your phone number (digits only): ")
        if phone.isdigit() and len(phone) == 10:
            phone_okay = True
        else:
            print("Invalid phone number")

    return phone


def get_id_num():
    """
    Get ID number from user, with validity checks. Returns the ID number as a string.
    """
    id_okay = False
    while not id_okay:
        id_num = input("Enter your ID number (letters and digits only): ").upper()
        id_okay = True
        for char in id_num:
            if not (char.isalpha() or char.isdigit()):
                id_okay = False
                print("Invalid ID number")

    return id_num


def get_dob():
    """
    Get date of birth from user, with validity checks. Returns the date of birth as a string of format 'YYYY-MM-DD'.
    """
    dob_okay = False
    while not dob_okay:
        dob = input("Enter your date of birth (YYYY-MM-DD): ")
        dobber = dob.split("-")
        if len(dobber) == 3:
            if dobber[0].isdigit() and len(dobber[0]) == 4:
                if dobber[1].isdigit() and len(dobber[1]) == 2:
                    if dobber[2].isdigit() and len(dobber[2]) == 2:
                        dob_okay = True
        if not dob_okay:
            print("Invalid date of birth")

    return dob


def convert_hhmm_to_hours(hhmm):
    """
    Convert a string in 'HH:MM' format to a float representing hours.
    """
    hh, mm = [int(x) for x in hhmm.split(":")]
    return hh + mm / 60


def convert_mins_to_hhmm(mins):
    """
    Convert an int representing minutes to a string in 'HH:MM' format.
    """
    hh = mins // 60
    mm = mins % 60
    return f"{hh:02d}:{mm:02d}"


def not_implemented():
    """
    Print a message indicating that a feature has not been implemented yet.
    """
    print("\nThis feature has not been implemented yet. Please continue.\n")


def extra():
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    cursor.execute(
        "select * from flights where airline_id =:d",
        {"c": 10, "d": 10},
    )
    searcher = cursor.fetchall()
    for line in searcher:
        print(line)
        print()
    # print(searcher)

    cursor.execute(
        "select * from customers where first_name =:c and last_name =:d",
        {"c": "Andrew", "d": "Allen"},
    )
    searcher = cursor.fetchall()
    for line in searcher:
        print(line)
        print()

    cursor.execute(
        "select id from customers where first_name =:c and last_name =:d",
        {"c": "Andrew", "d": "Allen"},
    )
    searcher = cursor.fetchone()
    print(searcher)
    custid = searcher[0]
    print(custid)

    cursor.execute("select * from trips where customer_id =:c", {"c": custid})
    searcher = cursor.fetchall()
    for line in searcher:
        print(line)
        print()

    connection.close()


if __name__ == "__main__":
    main()
