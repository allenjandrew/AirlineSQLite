## Overview

**Project Title**: AirlineSQLite

**Project Description**:

Introduction to SQLite and working with databases. The program involves an air travel agency database that maintains 6 tables for customers, trips, flights, airlines, airports, and aircraft.

**Project Goals**:

My simple goal was to learn SQLite. Therefore, this program centers around the basic CRUD operations - create, read, update, and delete. The program fulfills this by allowing the user to create customers, update customer information, read current trips, and delete trips. Additional functionality exists, however, like using aggregate functions to find total flight time and total cost.

## Instructions for Build and Use

Steps to build and/or run the software:

1. Run setup.py if air_travel.db isn't already built out. Make sure to change `SETUP = False` on line 11 to `True`.
2. Run main.py. You can use "Andrew Allen" as a default user. You can create your own user, but it won't have trips associated with it yet.
3. Enjoy.

Instructions for using the software:

1. The functionality of this database requires you to always be logged in as a customer. This is because the program keeps track of your unique customer ID. It's easy to switch between customers, though.
2. The options menu makes it easy to update your customer info, create a new user, view your trips, cancel a trip, and more. The menu is operated by simple numerical input.
3. Some features may not be built out yet.

## Development Environment

To recreate the development environment, you need the following software and/or libraries with the specified versions:

- Running Python 3.10.1 on VS Code.
- You may need to import the following libraries:
  - `datetime`
  - `random`
  - `string`
  - `csv`
  - `sqlite3`

## Useful Websites to Learn More

I found these websites useful in developing this software:

- [SQLite Backend for Beginners](https://www.youtube.com/watch?v=Ohj-CqALrwk)
  - Simple tutorial by Python Simplified
- [SQLite Aggregate Functions](https://www.sqlitetutorial.net/sqlite-aggregate-functions/)
  - Guide to using aggregate functions in SQLite
- [SQLite Docs - Date & Time](https://www.sqlite.org/lang_datefunc.html)
- Helpful troubleshooting websites:
  - [Geeks for Geeks](geeksforgeeks.org)
  - [W3Schools](w3schools.com)
  - [Stack Overflow](stackoverflow.com)
- AI helpers:
  - ChatGPT
  - Github Copilot

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

- [ ] Allow user to search flights
- [ ] Allow user to book trips
- [ ] Allow user to view their own customer info (right now they can change it but not yet see it lol)
