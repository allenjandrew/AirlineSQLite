import datetime
import random
import string
import csv
import sqlite3

DATABASE_FILE = "air_travel.db"
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M"

SETUP = False


def generate_unique_id(existing_ids, length=6):
    while True:
        new_id = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=length)
        )
        if new_id not in existing_ids:
            return new_id


def convert_s_to_hm(s):
    hours = s // 3600
    minutes = (s % 3600) // 60
    return f"{hours:02}:{minutes:02}"


def create_customers_list():

    # ("customer_id", first_name, last_name, email, phone, id_num, dob, address)

    customers = [
        (
            "Andrew",
            "Allen",
            "allenjandrew@gmail.com",
            "7632921848",
            "FVU321",
            "2000-12-23",
            "185 N 4032 E Rigby, ID 83442",
        ),
        (
            "Jamie",
            "Allen",
            "jamielnallen@gmail.com",
            "8019177733",
            "1J85008",
            "2004-04-02",
            "185 N 4032 E Rigby, ID 83442",
        ),
        (
            "John",
            "Doe",
            "johndoe@example.com",
            "5551234567",
            "7Y6G88KP",
            "1990-05-15",
            "123 Main St, Anytown, USA",
        ),
        (
            "Jane",
            "Smith",
            "janesmith@example.com",
            "5559876543",
            "IMBN324",
            "1985-08-30",
            "456 Elm St, Othertown, USA",
        ),
        (
            "Alice",
            "Johnson",
            "alicejohnson@example.com",
            "5557654321",
            "FVU39I5",
            "1995-03-10",
            "789 Oak St, Sometown, USA",
        ),
        (
            "Bob",
            "Brown",
            "bobbrown@example.com",
            "5558765432",
            "F99326",
            "1998-11-20",
            "101 Pine St, Anycity, USA",
        ),
        (
            "Charlie",
            "Davis",
            "charliedavis@example.com",
            "5556543210",
            "T7U327",
            "1992-07-25",
            "202 Maple St, Anyville, USA",
        ),
        (
            "Diana",
            "Evans",
            "dianaevans@example.com",
            "5554321098",
            "FV9990GH28",
            "1983-02-05",
            "303 Birch St, Anyburg, USA",
        ),
        (
            "Eve",
            "Foster",
            "evefoster@example.com",
            "5553210987",
            "88JJ8UI",
            "1999-09-09",
            "404 Cedar St, Anyplace, USA",
        ),
        (
            "Frank",
            "Green",
            "frankgreen@example.com",
            "5552109876",
            "123FREFJ",
            "1975-04-18",
            "505 Spruce St, Anyspot, USA",
        ),
    ]

    existing_ids = {customer[4] for customer in customers}

    for i in range(10, 1024):
        first_name = f"FirstName{i}"
        last_name = f"LastName{i}"
        email = f"email{i}@example.com"
        phone = f"555{i:07d}"
        id_num = generate_unique_id(existing_ids, random.randint(6, 12))
        existing_ids.add(id_num)
        dob = datetime.date(1980 + i % 40, (i % 12) + 1, (i % 28) + 1).strftime(
            DATE_FORMAT
        )
        address = f"{i} Random St, Randomtown, USA"
        customers.append((first_name, last_name, email, phone, id_num, dob, address))

    return customers


def create_airlines_list():
    airlines = [
        ("American Airlines", "USA"),
        ("Delta Air Lines", "USA"),
        ("United Airlines", "USA"),
        ("Southwest Airlines", "USA"),
        ("Air Canada", "Canada"),
        ("British Airways", "United Kingdom"),
        ("Lufthansa", "Germany"),
        ("Air France", "France"),
        ("Emirates", "United Arab Emirates"),
        ("Qatar Airways", "Qatar"),
        ("Singapore Airlines", "Singapore"),
        ("Cathay Pacific", "Hong Kong"),
        ("Qantas", "Australia"),
        ("Japan Airlines", "Japan"),
        ("Korean Air", "South Korea"),
        ("Turkish Airlines", "Turkey"),
    ]
    return airlines


def create_airports_list():
    airports = []
    with open("airports.csv") as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for row in csv_reader:
            airports.append((row[0], row[1], row[2], row[3]))
    return airports


def create_aircraft_list(airlines_list):
    # ("aircraft_id", airline_id, model, capacity, first_class_capacity, business_class_capacity, economy_class_capacity, tail_num)
    aircrafts = []
    existing_ids = set()

    for i in range(len(airlines_list) * 100):

        capacity = random.randint(100, 500)
        model = f"{'Boeing' if i % 2 else 'Airbus'} {capacity}"

        first_class_capacity = random.randint(10, 50)
        business_class_capacity = random.randint(20, 100)
        economy_class_capacity = (
            capacity - first_class_capacity - business_class_capacity
        )

        while economy_class_capacity <= 10:
            if first_class_capacity > random.randint(10, 20):
                first_class_capacity -= 2
                economy_class_capacity += 2
            else:
                business_class_capacity -= 5
                economy_class_capacity += 5

        assert economy_class_capacity >= 0
        assert first_class_capacity >= 0
        assert business_class_capacity >= 0
        assert (
            first_class_capacity + business_class_capacity + economy_class_capacity
            == capacity
        )

        tail_num = generate_unique_id(existing_ids, length=random.randint(8, 12))
        existing_ids.add(tail_num)

        aircrafts.append(
            (
                (i % len(airlines_list)) + 1,
                model,
                capacity,
                first_class_capacity,
                business_class_capacity,
                economy_class_capacity,
                "TAIL-" + tail_num,
            )
        )

    return aircrafts


def create_flights_list(airlines_list, airports_list, aircrafts_list):
    # ("flight_id", flight_num, airline_id, origin_airport_id, dest_airport_id, aircraft_id, depart_datetime, arrival_datetime, duration, status)

    flights = []
    existing_ids = set()

    for i in range(len(aircrafts_list)):
        flight_num = generate_unique_id(existing_ids, length=random.randint(5, 7))
        existing_ids.add(flight_num)

        airline_id = aircrafts_list[i][0]

        airports = random.sample(range(1, len(airports_list) + 1), 4)

        aircraft_id = i + 1

        departs = []
        arrives = []
        durations = []
        waiting = datetime.timedelta(minutes=47)

        depart_datetime = datetime.datetime(2025, 1, 1) + datetime.timedelta(
            days=random.randint(0, 364),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )
        departs.append(depart_datetime)

        for j in range(3):
            duration = datetime.timedelta(
                hours=random.randint(1, 24), minutes=random.randint(0, 59)
            )
            durations.append(duration)

            arrive_datetime = depart_datetime + duration
            arrives.append(arrive_datetime)

            if j < 2:
                depart_datetime = arrive_datetime + waiting
                departs.append(depart_datetime)

        status = random.choices(["On Time", "Delayed", "Cancelled"], [0.7, 0.2, 0.1])[0]

        for j in range(3):
            flights.append(
                (
                    airlines_list[airline_id - 1][0][:1] + flight_num + str(j),
                    airline_id,
                    airports[j],
                    airports[j + 1],
                    aircraft_id,
                    departs[j].strftime(DATETIME_FORMAT),
                    arrives[j].strftime(DATETIME_FORMAT),
                    durations[j].seconds // 60,
                    status,
                )
            )

    return flights


def create_trips_list(customers_list, flights_list, aircrafts_list):
    # ("trip_id", customer_id, flight_id, seat_num, seat_class, price)
    trips = []
    for i in range(len(customers_list) * 3):
        customer_id = (
            i + 1 if i < len(customers_list) else random.randint(1, len(customers_list))
        )
        flight_id = random.randint(1, len(flights_list))

        seat_num = random.randint(
            1, aircrafts_list[flights_list[flight_id - 1][4] - 1][2]
        )
        seat_class = random.choice(["First", "Business", "Economy"])
        price = random.randint(100, 1000)

        trips.append((customer_id, flight_id, seat_num, seat_class, price))

    return trips


def main():

    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    if SETUP:

        # customers
        customers_list = create_customers_list()
        cursor.execute(
            "create table if not exists customers (id integer primary key, first_name string, last_name string, email string, phone string, id_num string, dob string, address string)"
        )
        cursor.executemany(
            "insert into customers (first_name, last_name, email, phone, id_num, dob, address) values (?, ?, ?, ?, ?, ?, ?)",
            customers_list,
        )

        # airlines
        airlines_list = create_airlines_list()
        cursor.execute(
            "create table if not exists airlines (id integer primary key, name string, country string)"
        )
        cursor.executemany(
            "insert into airlines (name, country) values (?, ?)", airlines_list
        )

        # airports
        airports_list = create_airports_list()
        cursor.execute(
            "create table if not exists airports (id integer primary key, name string, iata string, city string, state string)"
        )
        cursor.executemany(
            "insert into airports (name, iata, city, state) values (?, ?, ?, ?)",
            airports_list,
        )

        # aircrafts
        aircrafts_list = create_aircraft_list(airlines_list)
        cursor.execute(
            "create table if not exists aircrafts (id integer primary key, airline_id integer, model string, capacity integer, first_class_capacity integer, business_class_capacity integer, economy_class_capacity integer, tail_num string)"
        )
        cursor.executemany(
            "insert into aircrafts (airline_id, model, capacity, first_class_capacity, business_class_capacity, economy_class_capacity, tail_num) values (?, ?, ?, ?, ?, ?, ?)",
            aircrafts_list,
        )

        # flights
        flights_list = create_flights_list(airlines_list, airports_list, aircrafts_list)
        cursor.execute(
            "create table if not exists flights (id integer primary key, flight_num string, airline_id integer, origin_airport_id integer, dest_airport_id integer, aircraft_id integer, depart_datetime string, arrival_datetime string, duration int, status string)"
        )
        cursor.executemany(
            "insert into flights (flight_num, airline_id, origin_airport_id, dest_airport_id, aircraft_id, depart_datetime, arrival_datetime, duration, status) values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            flights_list,
        )

        # trips
        trips_list = create_trips_list(customers_list, flights_list, aircrafts_list)
        cursor.execute(
            "create table if not exists trips (id integer primary key, customer_id integer, flight_id integer, seat_num integer, seat_class string, price integer)"
        )
        cursor.executemany(
            "insert into trips (customer_id, flight_id, seat_num, seat_class, price) values (?, ?, ?, ?, ?)",
            trips_list,
        )

        connection.commit()

    connection.close()


if __name__ == "__main__":
    main()
