import DBbase as db
import csv

class Hotel(db.DBbase):
    #This class is going to hold basic info of a hotel- name and location
    def __init__(self):
        super().__init__("hotel_reservation.sqlite")

    #this method is going to create the hotels table
    def reset_database(self):
        try:
            sql = """
                DROP TABLE IF EXISTS hotels;
                    CREATE TABLE "hotels" (
                        "ID"	INTEGER NOT NULL UNIQUE,
                        "name"	TEXT NOT NULL UNIQUE,
                        "location"	TEXT,
                        PRIMARY KEY("ID" AUTOINCREMENT)              
                    );
                """
            super().execute_script(sql)

        except Exception as e:
            print("An error occured!", e)

        finally:
            super().close_db()

    # add_hotel will insert data into hotels table   
    def add_hotel(self, name, location):
        try:
            super().get_cursor.execute("INSERT OR IGNORE INTO hotels (name, location) VALUES (?, ?);", (name,location))
            super().get_connection.commit()
            print(f"{name} added successfully.")
        except Exception as e:
            print("An error has occured.", e)
    


#following code will create the database, make hotels table and insert data

#hotel = Hotel()
#hotel.reset_database()
#hotel.add_hotel("Py Charming Resort", "abc street")
#hotel.add_hotel("Pylance Inn", "def street")
#hotel.add_hotel("Residence Inn", "123 street")


#The Room class will create rooms table in the hotel_reservation database.
#rooms table will hold info about room types in each hotel.
class Room(db.DBbase):
    def __init__(self):
        super().__init__("hotel_reservation.sqlite")   #connecting to the hotel_reservation database
    
    def reset_database(self):
        try:
            #sql to create rooms table
            #hotel_id is the foreign key that will point to a hotel in hotels table
            sql = """
            DROP TABLE IF EXISTS rooms;
                CREATE TABLE "rooms" (
                    "room_id" INTEGER NOT NULL UNIQUE,
                    "hotel_id" INTEGER NOT NULL, 
                    "room_type" TEXT NOT NULL,
                    "count" INTEGER NOT NULL,
                    "price" REAL,                    
                    PRIMARY KEY("room_id" AUTOINCREMENT),
                    FOREIGN KEY("hotel_id") REFERENCES "hotels"("ID") 
                        ON DELETE CASCADE             -- If a hotel is deleted, its rooms are too!
                );
                """
            super().execute_script(sql)

        except Exception as e:
            print("An error occured!", e)

        finally:
            super().close_db()

    #hotel_id is ID from the hotels table for the hotel we are adding rooms.
    #room_type is king/queen etc. count is the number of rooms for that type. price is the cost per night
    def add_room(self, hotel_id, room_type, count, price):
        try:
            super().get_cursor.execute("INSERT INTO rooms (hotel_id, room_type, count, price) VALUES (?, ?, ?, ?);", (hotel_id, room_type, count, price))
            super().get_connection.commit()
            print(f"{room_type} added to {hotel_id}")
        except Exception as e:
            print("An error adding room.", e)

#room = Room()
#room.reset_database()

#The following code will add three types of rooms for the 1st hotel named Py Charming Resort(hotel_id 1)
#room.add_room(1, "2 Queen Beds", 20, 289)
#room.add_room(1, "1 King Bed", 20, 297)
#room.add_room(1, "1 King Bed- Executive Lounge Access", 10, 333)

#The following code will add two types of rooms for the 2nd hotel named Pylance Inn (hotel_id 2)
#room.add_room(2, "Queen Room with Two Queen Beds", 30, 279)
#room.add_room(2, "Studio King Suite", 15, 350)


#The following code will add three types of rooms for the 3rd hotel named Residence Inn (hotel_id 3)
#room.add_room(3, "Standard King", 28, 429)
#room.add_room(3, "Standard Queen", 32, 419)
#room.add_room(3, "Suite", 10, 505)


#this Customer class will create a customers table and hold customer info
class Customer(db.DBbase):
    def __init__(self):
        super().__init__("hotel_reservation.sqlite")   # connecting to the same database

    def reset_database(self):
        try:
            sql = """
                DROP TABLE IF EXISTS customers;
                    CREATE TABLE "customers" (
                        "customer_id"	INTEGER NOT NULL UNIQUE,
                        "customer_name"	TEXT NOT NULL,
                        "email"	TEXT,
                        PRIMARY KEY("customer_id" AUTOINCREMENT)              
                    );
                """
            super().execute_script(sql)

        except Exception as e:
            print("An error occured in customer table.", e)

        finally:
            super().close_db()

    #To add a customer we need customer's name. email is optional
    def add_customer(self, customer_name, email= " "):
        try:
            super().get_cursor.execute("INSERT INTO customers (customer_name, email) VALUES (?, ?);", (customer_name, email))
            super().get_connection.commit()
            print(f"{customer_name} added successfully!")
            return super().get_cursor.lastrowid
        except Exception as e:
            print("An error adding customer.", e)

    #reading from a csv file and adding it to the database
    def add_customer_from_file(self, file_name):
        with open (file_name, "r") as records:
               csv_reader = csv.reader(records)
               next(records) # skips the header
               number_of_rows = 0
               for row in csv_reader:
                    number_of_rows += 1
                    try:
                         super().get_cursor.execute("INSERT INTO customers (customer_name, email) VALUES (?, ?);",
                             (row[1], row[2])
                         )
                         super().get_connection.commit()

                    except Exception as ex:
                         print(ex)
               print(f"{number_of_rows} customers added successfully")

#customer = Customer()
#customer.reset_database()

#Adding the following customers to the 'customers' table-
#customer.add_customer("John Doe", "john@somewhere.com")
#customer.add_customer("Liam Smith", "Liam@somewhere.com")
#customer.add_customer("Mia Johnson")
#customer.add_customer("Emily Harris", "emily@somewhere.com")

#Adding customer from a file
#customer.add_customer_from_file("customers.csv")



#The Reservation class is going to create a reservations table in the same database.
class Reservation(db.DBbase):
    def __init__(self):
        super().__init__("hotel_reservation.sqlite") #connecting to the same database
    
    def reset_database(self):
        try:
            sql = """
                DROP TABLE IF EXISTS reservations;
                    CREATE TABLE "reservations" (
                        "reservation_id" INTEGER NOT NULL UNIQUE,
                        "customer_id" INTEGER NOT NULL,
                        "room_id" INTEGER NOT NULL,
                        "room_quantity" INTEGER NOT NULL,
                        "hotel_id" INTEGER NOT NULL,
                        "dates" TEXT NOT NULL,
                        PRIMARY KEY("reservation_id" AUTOINCREMENT),
                        FOREIGN KEY("hotel_id") REFERENCES "hotels"("ID"),
                        FOREIGN KEY("customer_id") REFERENCES "customers"("customer_id"),
                        FOREIGN KEY("room_id") REFERENCES "rooms"("room_id")            
                    );
                """
            super().execute_script(sql)

        except Exception as e:
            print("An error occured in reservation table.", e)

        finally:
            super().close_db()


reservation = Reservation()
#reservation.reset_database()

#The logic for checking availability and creating reservation will be handled by a separate class in a separate file
#add_reservation was not tested here!

