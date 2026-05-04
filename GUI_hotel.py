import tkinter as tk
from tkinter import messagebox
import DBbase as db
from datetime import datetime
from datetime import date
from datetime import timedelta


#window creation
window = tk.Tk()
window.title("Hotel Reservation System")
window.geometry("700x600")

# SETUP FRAMES FIRST
home_frame = tk.Frame(window)
details_frame = tk.Frame(window) #will be created in System class, click_btn method
booking_frame= tk.Frame(window)

# Define the frame switching function
def show_page(frame):
    home_frame.pack_forget()
    details_frame.pack_forget()
    booking_frame.pack_forget()
    frame.pack(fill="both", expand=True)
    # The following line is to fix the bug of my back button
    # This forces Tkinter to recalculate the layout immediately
    window.update_idletasks() 

# This function is called in System class, make_booking method
def validate_reservation_dates(in_date, out_date):
    try:
        # Convert strings from the GUI inputs to date objects
        check_in = datetime.strptime(in_date, "%Y-%m-%d").date()
        check_out = datetime.strptime(out_date, "%Y-%m-%d").date()
        today = date.today()

        if check_in < today:
            return False, "Check-in date cannot be in the past."
        
        if check_out <= check_in:
            return False, "Check-out date must be after the check-in date."
        
        return True, "Dates are valid."
    except ValueError:
        return False, "Please enter dates in YYYY-MM-DD format."

class System(db.DBbase):
    def __init__(self):
        # Connect to the hotel_reservation database created in hotel_project.py file
        super().__init__("hotel_reservation.sqlite") 
    
    def show_error(self, message):
        messagebox.showerror("Error", message)
    
    def add_reservation(self, customer_id, room_quantity, a_date):
        try:
            # Convert date object (a_date) to string "YYYY-MM-DD"
            date_str = a_date.isoformat() 
            super().get_cursor.execute("INSERT INTO reservations (customer_id, room_id, room_quantity, hotel_id, dates) VALUES (?, ?, ?, ?, ?);",
                                        (customer_id, self.room_id, room_quantity, self.hotel, date_str))
            super().get_connection.commit()
        except Exception as e:
            messagebox.showerror("An error adding reservation.", e)

    # This method verifies that the customer is not entering a false id.
    def validate_customer(self, ID):
        # This query returns 1 if the ID is found, 0 if not
        query= """
                    SELECT EXISTS(SELECT 1 FROM customers WHERE customer_id= ? LIMIT 1)
                 """
        super().get_cursor.execute(query, (ID,))
        result = super().get_cursor.fetchone() # The result will be a tuple: either (1,) or (0,)
        # result[0] gets the value from the tuple (1 or 0)
        return result[0] == 1 # It returns True if ID found or False if not 

    def make_booking(self):
        # fetching data from entry boxes
        check_in_date = self.ent_in.get().strip()
        check_out_date= self.ent_out.get().strip()
        # validating the user entry for dates
        is_valid, message = validate_reservation_dates(check_in_date, check_out_date)
        
        if not is_valid:
            self.show_error(message)
            return

        try:
            room_quantity = int(self.ent_quant.get().strip())
            customer_id = int(self.ent_cusID.get().strip())
            if room_quantity <= 0:
                raise ValueError("Quantity must be positive.")
        except ValueError:
            self.show_error("Room quantity and Customer ID must be valid numbers.")
            return
        
        # If the customer id is not found in the database, the booking will not proceed
        if not self.validate_customer(customer_id):
            messagebox.showerror("Invalid ID", "The Customer ID entered does not exist.")
            return

        try:
            # get occupancy
            check_res = """
                SELECT dates, SUM(room_quantity) 
                FROM reservations
                WHERE room_id = ? 
                AND dates >= ? 
                AND dates < ?
                GROUP BY dates
                ORDER BY dates ASC
                """
            super().get_cursor.execute(check_res, (self.room_id, check_in_date, check_out_date))
            results = super().get_cursor.fetchall()
            #saving the results in a dictionary
            availability_dict = dict(results)

            #sql_totalRooms is going to find out total number of rooms for the room_id
            sql_totalRooms= """
                        SELECT count FROM rooms
                        WHERE room_id = ?
                        """
            super().get_cursor.execute(sql_totalRooms, (self.room_id, ))
            total_room = super().get_cursor.fetchone()    #for one room_id there is only one count value

            # Convert the main boundary strings to date objects, including the date strings saved in dictionary
            # We need to convert all date strings to date objects; otherwise timedelta to increament date in the while loop won't work
            # since comparison of a date object to a string won't work, we are converting the date strings of the dictionary too
            check_in_dt = date.fromisoformat(check_in_date)
            check_out_dt = date.fromisoformat(check_out_date)
            clean_avail_dict = {date.fromisoformat(k): v for k, v in availability_dict.items()}
            

            #logic to check if a room is available for each date the customer wants to reserve.
            can_book = True
            temp_date = check_in_dt 

            while temp_date < check_out_dt:
                if temp_date in clean_avail_dict:
                    available = total_room[0] - clean_avail_dict[temp_date]
                    if room_quantity > available:
                        can_book = False
                        break  # Stop checking, we already found a conflict
    
                # Check next day
                temp_date += timedelta(days=1)

            # COMMIT PHASE: Only add to database if the check for all dates passed
            if can_book:
                current_date = check_in_dt
                while current_date < check_out_dt:
                    self.add_reservation(customer_id, room_quantity, current_date)
                    current_date += timedelta(days=1)
    
                messagebox.showinfo("Success", "Reservation completed!")
            else:
                messagebox.showerror("Error", f"One or more dates are full for {room_quantity} rooms.")

        except Exception as e:
            self.show_error(f"A database error occurred: {e}")

    def create_booking_frame(self):
        # 'booking_frame' is found in the global scope
        for widget in booking_frame.winfo_children(): 
            widget.destroy()

        #label and entry box for customer id input
        tk.Label(booking_frame, text="Enter Customer ID or Sign up to get one", font= ("", 16)).pack(pady=50)
        tk.Label(booking_frame, text="Customer ID:").pack()
        self.ent_cusID = tk.Entry(booking_frame)
        self.ent_cusID.pack()

        # button to finalize the reservation
        tk.Button(booking_frame, text="Confirm Booking", font= ("", 16), command= self.make_booking).pack(pady=20)

        # Sign up button
        tk.Label(booking_frame, text="-----or-----", font= ("", 16)).pack(pady=10)
        btn_signup= tk.Button(booking_frame, text="Sign up", font= ("", 16))
        btn_signup.pack(pady=5)

        # back button
        btn_back_booking = tk.Button(booking_frame, text="Back", command=lambda: show_page(details_frame))
        btn_back_booking.pack(pady=100)

        # make the switch
        show_page(booking_frame)


    def final_selection(self, room_data):
        #creating a class variable with room_data's room id
        self.room_id = room_data[0]

        #the empty label gets filled with text
        self.lbl_room_selection.config(text=f"You selected {room_data[1]}")
        #deleting old data
        self.ent_quant.delete(0, tk.END) 


    def click_btn(self, hotel_id):
        # Saving the hotel_id in a class variable
        self.hotel = hotel_id

        #CLEAR the details_frame so old hotel rooms disappear
        for widget in details_frame.winfo_children():
            widget.destroy()

        #fetch the rooms for this hotel
        sql= """
            SELECT room_id, room_type, price 
            FROM rooms
            WHERE hotel_id = ?
            """
        super().get_cursor.execute(sql, (hotel_id, ))
        cursor = super().get_cursor
        rooms= cursor.fetchall()
        
        #create a header
        lbl_details = tk.Label(details_frame, text="Select Room, Quantity & Date", font=("", 16))
        lbl_details.pack(pady=10)

        #create a button for each room
        for room in rooms:
            room_btn= tk.Button(
            details_frame,
            text=f"{room[1]} - ${room[2]}/night",
            font= ("", 16),
            width=40,
            height=1,
            #calling final_selection with room_id and room_name
            command =lambda r=room: self.final_selection(r) 
            )
            room_btn.pack(pady=5)

        #create an empty label using self. so we can configure it in another method
        self.lbl_room_selection= tk.Label(details_frame, text="", font= ("", 16))
        self.lbl_room_selection.pack(pady=10)

        #create a quantity label
        tk.Label(details_frame, text= "Quantity", font= ("", 16)).pack()
       
        #create an entry box using self
        self.ent_quant = tk.Entry(details_frame)
        self.ent_quant.pack(pady=5)

        #create a check in label
        tk.Label(details_frame, text= "Check in date: (YYYY-MM-DD)", font= ("", 16)).pack()

        #create a check in entry box using self
        self.ent_in = tk.Entry(details_frame)
        self.ent_in.pack(pady=5)

        #create a check out label
        tk.Label(details_frame, text= "Check out date: (YYYY-MM-DD)", font= ("", 16)).pack()

        #create a check out entry box using self
        self.ent_out = tk.Entry(details_frame)
        self.ent_out.pack(pady=5)

        # Create a container frame for the Next & Back buttons
        button_container = tk.Frame(details_frame)
        button_container.pack(pady=10)

        #create a back button
        btn_back = tk.Button(button_container, text="Back", command=lambda: show_page(home_frame))
        btn_back.pack(side="left", padx=5)
        tk.Label(button_container, text="|").pack(side="left", padx=5)

        #create a submit button
        btn_next= tk.Button(button_container, text="Next", command= self.create_booking_frame)
        btn_next.pack(side="left", padx=5)

        #switch to the details page
        show_page(details_frame)   

       
system= System()

#create home page widgets
welcome_msg = tk.Label(home_frame, text="Welcome Guest", font=("", 32))
welcome_msg.pack(pady= 50)
select_msg= tk.Label(home_frame, text="Select a hotel", font= ("", 16))
select_msg.pack(pady=5)

btn1= tk.Button(
    home_frame,
    text="Py Charming Resort",
    font= ("", 16),
    width=20,
    height=2,
    command= lambda: system.click_btn(1)
)
btn2= tk.Button(
    home_frame,
    text="Pylance Inn",
    font= ("", 16),
    width=20,
    height=2,
    command= lambda: system.click_btn(2)
)
btn3= tk.Button(
    home_frame,
    text="Residence Inn",
    font= ("", 16),
    width=20,
    height=2,
    command= lambda: system.click_btn(3)
)

btn1.pack(pady=10)
btn2.pack(pady=10)
btn3.pack(pady=10)


# INITIALIZE THE STARTING VIEW
home_frame.pack(fill="both", expand=True)

window.mainloop()

