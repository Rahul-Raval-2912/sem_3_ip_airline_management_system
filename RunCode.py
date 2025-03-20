import os
from Database import DBMS_Connection
from Main import Main 
from User import User
from Admin import Admin
from Plan import Plan
import random
import time
import string

class RunCode:
    def __init__(self, db, main):
        self.db = db
        self.main = main
        self.current_user = None
        self.current_admin = None

    def menu(self):
        while True:
            print("\n=== Welcome to xAIrline Booking System ===")
            print("1. Sign Up")
            print("2. Log In")
            print("3. Admin Login")
            print("4. Exit")
            choice = input("Please enter your choice (1-4): ")
            if choice == "1":
                self.sign_up()
            elif choice == "2":
                if self.log_in():
                    self.user_menu()
            elif choice == "3":
                self.admin_login()
            elif choice == "4":
                print("\nThank you for using xAIrline. Goodbye!")
                break
            else:
                print("Invalid choice! Please select a valid option.")

    def sign_up(self):
        user = User(self.db)
        if user.sign_up():
            self.current_user = user
            self.user_menu()

    def log_in(self):
        print("\n=== User Login ===")
        user = User(self.db)
        user_id = input("User ID: ")
        password = input("Password: ")
        result = user.log_in(user_id, password)
        print(result)
        if "successful" in result.lower():
            self.current_user = user
            return True
        return False

    def admin_login(self):
        print("\n=== Admin Login ===")
        email = input("Admin Email: ")
        password = input("Admin Password: ")
        admin = Admin(self.db)
        result = admin.log_in(email, password)
        print(result)
        if "successful" in result.lower():
            self.current_admin = admin
            self.admin_menu()

    def user_menu(self):
        while True:
            print("\n=== User Dashboard ===")
            print("1. Book Ticket")
            print("2. Cancel Ticket")
            print("3. View Upcoming Flights")
            print("4. Submit Feedback")
            print("5. View Booked Tickets")
            print("6. Check Wallet Balance")
            print("7. Redeem Bonus Points")
            print("8. View Flight Details")
            print("9. Update Profile")
            print("10. View Booking History")
            print("11. Log Out")
            choice = input("Please enter your choice (1-11): ")
            if choice == "1":
                self.book_ticket()
            elif choice == "2":
                self.cancel_ticket()
            elif choice == "3":
                print(self.main.upcoming_flights(self.db))
            elif choice == "4":
                self.give_feedback()
            elif choice == "5":
                self.view_booked_tickets()
            elif choice == "6":
                print(f"\n=== Wallet Information ===")
                print(f"Balance: ${float(self.current_user.wallet_balance):.2f}")
                print(f"Bonus Points: {self.current_user.bonus_count}")
            elif choice == "7":
                self.redeem_bonus()
            elif choice == "8":
                self.view_flight_details()
            elif choice == "9":
                self.update_profile()
            elif choice == "10":
                print(self.current_user.get_booking_history())
            elif choice == "11":
                print("\nLogged out successfully. Thank you for using xAIrline!")
                self.current_user = None
                break
            else:
                print("Invalid choice! Please select a valid option.")

    def admin_menu(self):
        while True:
            print("\n=== Admin Dashboard ===")
            print("1. Add Flight Plan")
            print("2. Remove Flight Plan")
            print("3. Update Flight Plan")
            print("4. View All Flight Plans")
            print("5. View Registered Users")
            print("6. Remove User")
            print("7. View User Feedback")
            print("8. View Booking Statistics")
            print("9. View Total Revenue")
            print("10. Send Broadcast Notification")
            print("11. Log Out")
            choice = input("Please enter your choice (1-11): ")
            if choice == "1":
                self.add_plan()
            elif choice == "2":
                self.remove_plan()
            elif choice == "3":
                self.update_plan()
            elif choice == "4":
                print(self.view_plans())
            elif choice == "5":
                print(self.view_users())
            elif choice == "6":
                user_id = input("Enter User ID to Remove: ")
                print(self.remove_user(user_id))
            elif choice == "7":
                print(self.view_feedback())
            elif choice == "8":
                print(self.current_admin.view_booking_stats())
            elif choice == "9":
                print(self.current_admin.view_revenue())
            elif choice == "10":
                message = input("Enter broadcast message: ")
                print(self.current_admin.broadcast_notification(message))
            elif choice == "11":
                print("\nAdmin logged out successfully.")
                self.current_admin = None
                break
            else:
                print("Invalid choice! Please select a valid option.")

    def book_ticket(self):
        print("\n=== Book a Flight ===")
        plan_id = input("Enter Flight ID: ")

        plan = Plan.load_from_db(self.db, plan_id)
        if not plan:
            print("Error: Invalid Flight ID!")
            return

        print(f"\nFlight: {plan.name} | {plan.departure} → {plan.destination}")
        print(f"Available Seats - General: {plan.general}, Business: {plan.business}")

        seat_type = input("Choose seat type (General/Business): ").capitalize()
        if seat_type not in ["General", "Business"]:
            print("Error: Invalid seat type! Please choose General or Business.")
            return

        available_seat_count = plan.general if seat_type == "General" else plan.business
        if available_seat_count <= 0:
            print(f"Error: No {seat_type.lower()} seats available!")
            return

        num_seats = input(f"How many {seat_type.lower()} seats would you like to book (1-{available_seat_count})? ")
        try:
            num_seats = int(num_seats)
            if num_seats <= 0 or num_seats > available_seat_count:
                print(f"Error: Please enter a number between 1 and {available_seat_count}!")
                return
        except ValueError:
            print("Error: Please enter a valid number!")
            return

        available_seats = plan.get_available_seats(seat_type)
        if len(available_seats) < num_seats:
            print(f"Error: Only {len(available_seats)} {seat_type.lower()} seats available!")
            return

        # Display all available seats
        print(f"\n=== Available {seat_type} Seats ===")
        for i, seat in enumerate(available_seats, 1):
            print(f"{i}. {seat}")
        
        print(f"\nEnter the seat numbers you want to book (e.g., 1, 2, 3, 4 for {num_seats} seats):")
        while True:
            seat_input = input("Your selection: ").strip()
            try:
                seat_choices = [int(x.strip()) - 1 for x in seat_input.split(',')]
                if len(seat_choices) != num_seats:
                    print(f"Error: Please select exactly {num_seats} seats!")
                    continue
                if any(choice < 0 or choice >= len(available_seats) for choice in seat_choices):
                    print("Error: One or more seat numbers are out of range!")
                    continue
                if len(set(seat_choices)) != len(seat_choices):
                    print("Error: Duplicate seat selections are not allowed!")
                    continue
                selected_seats = [available_seats[i] for i in seat_choices]
                break
            except ValueError:
                print("Error: Please enter valid numbers separated by commas (e.g., 1, 2, 3)!")

        base_price = 200 if seat_type == "General" else 400
        total_base_price = base_price * num_seats
        bonus_count = int(self.current_user.bonus_count)
        discount = 0.5 if bonus_count == 10 else 1.0
        final_price = total_base_price * discount
        thank_you = " Thank you for your loyalty and choosing xAIrline!" if bonus_count == 10 else ""

        print(f"\n=== Booking Summary ===")
        print(f"Flight: {plan.name}")
        print(f"Departure: {plan.departure}")
        print(f"Destination: {plan.destination}")
        print(f"Seats: {', '.join(selected_seats)} ({seat_type})")
        print(f"Total Amount: ${final_price:.2f}{' (50% off applied)' if bonus_count == 10 else ''}")

        print("\n=== Select Payment Method ===")
        print("1. Credit Card")
        print("2. Debit Card")
        print("3. UPI")
        payment_choice = input("Enter your payment method (1-3): ")

        if payment_choice == "1":
            payment_mode = "Credit Card"
            card_number = input("Enter 16-digit Credit Card Number: ")
            if len(card_number) != 16 or not card_number.isdigit():
                print("Error: Invalid credit card number! Must be 16 digits.")
                return
            card_expiry = input("Enter Expiry Date (MM/YY): ")
            card_cvv = input("Enter CVV (3 digits): ")
            if len(card_cvv) != 3 or not card_cvv.isdigit():
                print("Error: Invalid CVV! Must be 3 digits.")
                return
        elif payment_choice == "2":
            payment_mode = "Debit Card"
            card_number = input("Enter 16-digit Debit Card Number: ")
            if len(card_number) != 16 or not card_number.isdigit():
                print("Error: Invalid debit card number! Must be 16 digits.")
                return
            card_expiry = input("Enter Expiry Date (MM/YY): ")
            card_cvv = input("Enter CVV (3 digits): ")
            if len(card_cvv) != 3 or not card_cvv.isdigit():
                print("Error: Invalid CVV! Must be 3 digits.")
                return
        elif payment_choice == "3":
            payment_mode = "UPI"
            upi_id = input("Enter UPI ID (e.g., user@bank): ")
            if "@" not in upi_id:
                print("Error: Invalid UPI ID! Must include '@'.")
                return
        else:
            print("Error: Invalid payment method! Please choose 1, 2, or 3.")
            return

        pnr = self.main.generate_pnr()
        ticket_query = """
        INSERT INTO tickets (pnr, user_id, plan_id, seat_type, price, status, refund_status)
        VALUES (%s, %s, %s, %s, %s, 'Booked', 'Pending')
        """
        seat_type_with_seats = f"{seat_type} ({', '.join(selected_seats)})"
        try:
            self.db.cursor.execute(ticket_query, (pnr, self.current_user.id, plan_id, seat_type_with_seats, final_price))
            update_seat_query = f"UPDATE plan SET {seat_type.lower()} = {seat_type.lower()} - %s WHERE id = %s"
            self.db.cursor.execute(update_seat_query, (num_seats, plan_id))
            self.db.conn.commit()
        except Exception as e:
            print(f"Error: Failed to book ticket - {e}")
            return

        transaction_id = f"TXN{random.randint(100000, 999999)}"
        payment_query = """
        INSERT INTO payments (user_id, pnr, amount, payment_mode, transaction_id, status)
        VALUES (%s, %s, %s, %s, %s, 'Success')
        """
        try:
            self.db.cursor.execute(payment_query, (self.current_user.id, pnr, final_price, payment_mode, transaction_id))
            self.db.conn.commit()
        except Exception as e:
            print(f"Error: Payment failed - {e}")
            self.db.cursor.execute("DELETE FROM tickets WHERE pnr = %s", (pnr,))
            self.db.cursor.execute(f"UPDATE plan SET {seat_type.lower()} = {seat_type.lower()} + %s WHERE id = %s", (num_seats, plan_id))
            self.db.conn.commit()
            return

        new_bonus_count = bonus_count + 1
        update_bonus_query = "UPDATE user SET bonus_count = %s WHERE id = %s"
        self.db.cursor.execute(update_bonus_query, (new_bonus_count, self.current_user.id))
        self.db.conn.commit()

        self.db.cursor.execute("SELECT id, name, location, birthday, password, bonus_count, email, wallet_balance FROM user WHERE id = %s", (self.current_user.id,))
        user_data = self.db.cursor.fetchone()
        self.current_user = User(self.db, user_data[1], user_data[2], user_data[3], user_data[4], user_data[6], user_data[5], user_data[7])
        self.current_user.id = user_data[0]

        print(self.main.generate_ticket(self.db, self.current_user.id, plan_id, pnr))
        print(f"\n=== Booking Confirmation ===")
        print(f"PNR: {pnr}")
        print(f"Flight: {plan.name}")
        print(f"Seats: {', '.join(selected_seats)} ({seat_type})")
        print(f"Payment Method: {payment_mode}")
        print(f"Transaction ID: {transaction_id}")
        print(f"Total Charged: ${final_price:.2f}")
        print(f"New Bonus Count: {self.current_user.bonus_count}{thank_you}")
        self.main.send_notification(self.current_user.id, f"Your booking for {plan.name} (PNR: {pnr}) is confirmed!")

    def cancel_ticket(self):
        print("\n=== Cancel Ticket ===")
        pnr = input("Enter PNR to cancel: ")
        self.db.cursor.execute("SELECT user_id, plan_id, price, seat_type FROM tickets WHERE pnr = %s AND user_id = %s", (pnr, self.current_user.id))
        ticket = self.db.cursor.fetchone()
        if not ticket:
            print("Error: Invalid PNR or ticket not found.")
            return
        
        user_id, plan_id, ticket_price, seat_type = ticket
        if '(' in seat_type:
            seat_count = len(seat_type.split('(')[1].rstrip(')').split(', '))
            seat_category = seat_type.split('(')[0].strip().lower()
        else:
            seat_count = 1
            seat_category = seat_type.lower()

        refund_amount = 0.8 * ticket_price
        update_query = "UPDATE user SET wallet_balance = wallet_balance + %s WHERE id = %s"
        self.db.cursor.execute(update_query, (refund_amount, user_id))
        self.db.cursor.execute("UPDATE tickets SET status = 'Canceled', refund_status = 'Refunded' WHERE pnr = %s", (pnr,))
        self.db.cursor.execute(f"UPDATE plan SET {seat_category} = {seat_category} + %s WHERE id = %s", (seat_count, plan_id))
        self.db.conn.commit()
        
        self.db.cursor.execute("SELECT id, name, location, birthday, password, bonus_count, email, wallet_balance FROM user WHERE id = %s", (self.current_user.id,))
        user_data = self.db.cursor.fetchone()
        self.current_user = User(self.db, user_data[1], user_data[2], user_data[3], user_data[4], user_data[6], user_data[5], user_data[7])
        self.current_user.id = user_data[0]
        
        print(f"Ticket {pnr} cancelled successfully. Refunded ${refund_amount:.2f} to your wallet.")
        self.main.send_notification(self.current_user.id, f"Your cancellation for PNR {pnr} has been processed. Refund: ${refund_amount:.2f}")

    def view_booked_tickets(self):
        print("\n=== Your Booked Tickets ===")
        query = "SELECT pnr, plan_id, seat_type, price, status FROM tickets WHERE user_id = %s AND status = 'Booked'"
        self.db.cursor.execute(query, (self.current_user.id,))
        tickets = self.db.cursor.fetchall()
        if not tickets:
            print("No booked tickets found.")
            return
        for ticket in tickets:
            pnr, plan_id, seat_type, price, status = ticket
            flight_details = self.db.get_flight_details(plan_id)
            if flight_details:
                flight_name = flight_details[0]
                print(f"PNR: {pnr}, Flight: {flight_name}, Seats: {seat_type}, Price: ${float(price):.2f}, Status: {status}")
            else:
                print(f"PNR: {pnr}, Flight ID: {plan_id} (Details unavailable), Seats: {seat_type}, Price: ${float(price):.2f}, Status: {status}")

    def give_feedback(self):
        print("\n=== Submit Feedback ===")
        feedback = input("Please enter your feedback: ")
        query = "INSERT INTO feedback (name, email, feedback) VALUES (%s, %s, %s)"
        self.db.cursor.execute(query, (self.current_user.name, self.current_user.email, feedback))
        self.db.conn.commit()
        print("Feedback submitted successfully. Thank you!")

    def add_plan(self):
        print("\n=== Add Flight Plan ===")
        name = input("Flight Name: ")
        departure = input("Departure Location: ")
        destination = input("Destination: ")
        time = input("Departure Time (YYYY-MM-DD HH:MM:SS): ")
        general = input("General Seat Count: ")
        business = input("Business Seat Count: ")
        try:
            passenger = int(general) + int(business)
        except ValueError:
            print("Error: Seat counts must be numbers!")
            return
        landing_time = input("Landing Time (YYYY-MM-DD HH:MM:SS): ")
        plan = Plan(self.db, name, passenger, general, business, departure, destination, time, landing_time)
        print(plan.save_to_db())

    def remove_plan(self):
        print("\n=== Remove Flight Plan ===")
        plan_id = input("Enter Flight ID to Remove: ")
        plan = Plan.load_from_db(self.db, plan_id)
        if plan:
            print(plan.delete_from_db())
        else:
            print("Error: Flight not found.")

    def update_plan(self):
        print("\n=== Update Flight Plan ===")
        plan_id = input("Enter Flight ID to Update: ")
        plan = Plan.load_from_db(self.db, plan_id)
        if not plan:
            print("Error: Flight not found!")
            return
        time = input("Enter New Departure Time (YYYY-MM-DD HH:MM:SS, press Enter to skip): ")
        if time:
            plan.time = time
        print(plan.save_to_db())

    def view_plans(self):
        return Plan.get_all_plans(self.db)

    def view_users(self):
        return self.current_admin.view_users()

    def remove_user(self, user_id):
        return self.current_admin.remove_user(user_id)

    def view_feedback(self):
        return self.current_admin.view_feedback()

    def redeem_bonus(self):
        print("\n=== Redeem Bonus Points ===")
        bonus_count = int(self.current_user.bonus_count)
        if bonus_count < 10:
            print(f"Insufficient points! Current: {bonus_count}, Required: 10")
            return

        reward_amount = 50
        new_bonus_count = bonus_count - 10
        new_wallet_balance = float(self.current_user.wallet_balance) + reward_amount
        
        query = "UPDATE user SET bonus_count = %s, wallet_balance = %s WHERE id = %s"
        try:
            self.db.cursor.execute(query, (new_bonus_count, new_wallet_balance, self.current_user.id))
            self.db.conn.commit()
            self.db.cursor.execute("SELECT id, name, location, birthday, password, bonus_count, email, wallet_balance FROM user WHERE id = %s", (self.current_user.id,))
            user_data = self.db.cursor.fetchone()
            self.current_user = User(self.db, user_data[1], user_data[2], user_data[3], user_data[4], user_data[6], user_data[5], user_data[7])
            self.current_user.id = user_data[0]
            print(f"Success: Redeemed 10 bonus points for ${reward_amount}. New Balance: ${self.current_user.wallet_balance:.2f}")
        except Exception as e:
            print(f"Error: Failed to redeem bonus - {e}")

    def view_flight_details(self):
        print("\n=== View Flight Details ===")
        plan_id = input("Enter Flight ID: ")
        plan = Plan.load_from_db(self.db, plan_id)
        if not plan:
            print("Error: Flight not found!")
            return
        print(f"Flight ID: {plan.id}")
        print(f"Flight Name: {plan.name}")
        print(f"Capacity: {plan.passenger} passengers")
        print(f"General Seats Available: {plan.general}")
        print(f"Business Seats Available: {plan.business}")
        print(f"Departure: {plan.departure}")
        print(f"Destination: {plan.destination}")
        print(f"Departure Time: {plan.time}")
        print(f"Arrival Time: {plan.landing_time}")
        print(f"Status: {plan.get_status()}")

if __name__ == "__main__":
    db = DBMS_Connection()
    main = Main()
    run = RunCode(db, main)
    run.menu()