### customers

    id integer primary key,
    first_name string,
    last_name string,
    email string,
    phone string,
    id_num string,
    dob string,
    address string

### airlines

    id integer primary key,
    name string,
    country string

### airports

    id integer primary key,
    name string,
    iata string,
    city string,
    state string

### aircrafts

    id integer primary key,
    airline_id integer (foreign: airlines.id),
    model string,
    capacity integer,
    first_class_capacity integer,
    business_class_capacity integer,
    economy_class_capacity integer,
    tail_num string

### flights

    id integer primary key,
    flight_num string,
    airline_id integer (foreign: airlines.id),
    origin_airport_id integer (foreign: airports.id),
    dest_airport_id integer (foreign: airports.id),
    aircraft_id integer (foreign: aircrafts.id),
    depart_datetime string,
    arrival_datetime string,
    duration string,
    status string

### trips

    id integer primary key,
    customer_id integer (foreign: customers.id),
    flight_id integer (foreign: flights.id),
    seat_num integer,
    seat_class string,
    price integer
