# Airline travel agency system

### Description

Create a database to manage trips, customers, airlines, airplanes, airports, bookings, dates, times, fares
Implement CRUD operations for trips and bookings
Write queries to find popular destinations, booking history, etc.

### Plan

1. Write docstrings explaining the purpose, parameters, and return value for every function.

2. Make a schedule outlining what days and times I will work on this sprint. If I miss an hour, find somewhere else in my schedule to place it.
3. Make a schedule for when I will work on this project (as well as the team project).
4. Watch videos, read tutorials on sql for beginners.
5. Set up my development environment, if needed. I expect to use Python in VS Code with SQLite.
6. Make practice databases, if needed.
7. Build the project.

### Resources

https://www.youtube.com/watch?v=Ohj-CqALrwk&pp=ygUGc3FsaXRl
https://www.youtube.com/watch?v=jH39c5-y6kg

## Functionality

| Functionality                                  |   CRUD    | Implemented? |
| ---------------------------------------------- | :-------: | :----------: |
| Search existing flights by day, origin, destin |   read    |              |
| Search existing trips by customer              |   read    |              |
| Cancel trip                                    |  delete   |              |
| Create trip                                    |  create   |              |
| Create customer                                |  create   |              |
| Update customer details                        |  update   |              |
| Update flight times                            |  update   |              |
| Get customer's total flight time               | aggregate |              |
| Get customer's total cost                      | aggregate |              |

## Necessary tables

1. Customers

This table stores information about the customers who book flights.

    •	customer_id (Primary Key, Integer)
    •	first_name (Text)
    •	last_name (Text)
    •	email (Text)
    •	phone_number (Text)
    •	passport_number (Text, unique for each customer)
    •	date_of_birth (Date)
    •	address (Text)

2. Airlines

This table stores information about airlines operating in the system.

    •	airline_id (Primary Key, Integer)
    •	name (Text)
    •	country (Text)

3. Airports

This table stores information about airports.

    •	airport_id (Primary Key, Integer)
    •	name (Text)
    •	city (Text)
    •	country (Text)
    •	iata_code (Text, 3-letter code for the airport)

4. Flights

This table stores information about individual flights offered by airlines.

    •	flight_id (Primary Key, Integer)
    •	flight_number (Text, unique)
    •	airline_id (Foreign Key to Airlines.airline_id)
    •	origin_airport_id (Foreign Key to Airports.airport_id)
    •	destination_airport_id (Foreign Key to Airports.airport_id)
    •	departure_time (DateTime)
    •	arrival_time (DateTime)
    •	duration (Time)
    •	status (Text, e.g., scheduled, delayed, cancelled)

5. Trips

This table keeps track of individual bookings or trips customers make.

    •	trip_id (Primary Key, Integer)
    •	customer_id (Foreign Key to Customers.customer_id)
    •	flight_id (Foreign Key to Flights.flight_id)
    •	booking_date (DateTime)
    •	seat_number (Text)
    •	price (Decimal)

6. Baggage

This table stores information about the baggage associated with trips.

    •	baggage_id (Primary Key, Integer)
    •	trip_id (Foreign Key to Trips.trip_id)
    •	weight (Decimal)
    •	dimensions (Text, e.g., “22x14x9”)
    •	type (Text, e.g., carry-on, checked)

7. Payments

This table stores information about payments for bookings.

    •	payment_id (Primary Key, Integer)
    •	trip_id (Foreign Key to Trips.trip_id)
    •	amount (Decimal)
    •	payment_date (DateTime)
    •	payment_method (Text, e.g., credit card, PayPal)
    •	status (Text, e.g., paid, refunded)

8. Aircrafts

This table stores information about the aircraft used for flights.

    •	aircraft_id (Primary Key, Integer)
    •	airline_id (Foreign Key to Airlines.airline_id)
    •	model (Text, e.g., “Boeing 737”)
    •	capacity (Integer, total seats available)
    •	tail_number (Text, unique identifier for the aircraft)

9. Crew

This table stores information about the crew members assigned to flights.

    •	crew_id (Primary Key, Integer)
    •	first_name (Text)
    •	last_name (Text)
    •	role (Text, e.g., pilot, flight attendant)
    •	flight_id (Foreign Key to Flights.flight_id)

Relationships:

    •	Customers and Trips: A customer can have multiple trips, but each trip is linked to one customer (Customers ↔ Trips).
    •	Trips and Flights: A trip is linked to a specific flight, but a flight can have multiple trips associated with it (Trips ↔ Flights).
    •	Flights and Airlines: Each flight is operated by an airline, but an airline can have many flights (Flights ↔ Airlines).
    •	Airports and Flights: Each flight has an origin and a destination airport (Flights ↔ Airports).
    •	Trips and Baggage: A trip can have multiple pieces of baggage, but each piece of baggage belongs to one trip (Trips ↔ Baggage).
    •	Aircrafts and Flights: Each flight uses a specific aircraft, and each aircraft can be used for multiple flights (Flights ↔ Aircrafts).
