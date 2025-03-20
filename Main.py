import os
import random
import string
import io
from datetime import datetime

class Main:
    def generate_pnr(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def book_ticket(self, db, user, plan_id, seat_type):
        return "Booking handled in RunCode."

    def cancel_ticket(self, db, user, pnr):
        return "Cancellation handled in RunCode."

    def show_available_seat(self, db, plan_id):
        query = "SELECT general, business FROM plan WHERE id = %s"
        db.cursor.execute(query, (plan_id,))
        result = db.cursor.fetchone()
        if result:
            general, business = result
            return f"Available Seats - General: {general}, Business: {business}"
        return "Invalid plan ID or no seats available."

    def check_ticket_status(self, db, pnr):
        query = "SELECT status FROM tickets WHERE pnr = %s"
        db.cursor.execute(query, (pnr,))
        result = db.cursor.fetchone()
        if result:
            return f"Ticket Status: {result[0]}"
        return "Invalid PNR! Ticket not found."

    def feedback(self, db, name, email, message):
        return "Feedback handled in RunCode."

    def upcoming_flights(self, db):
        query = """
        SELECT id, name, departure, destination, time, landing_time 
        FROM plan 
        WHERE time > NOW()
        ORDER BY time ASC
        """
        db.cursor.execute(query)
        flights = db.cursor.fetchall()
        if not flights:
            return "No upcoming flights available."
        output = "\n=== Upcoming Flights ===\n"
        for flight in flights:
            output += f"ID: {flight[0]}, {flight[1]}, {flight[2]} → {flight[3]}, Dep: {flight[4]}, Arr: {flight[5]}\n"
        return output

    def payment(self, db, user_id, amount, payment_mode, card_number=None, upi_id=None):
        return "Payment handled in RunCode."

    def refund_to_wallet(self, db, user_id, plan_id):
        return "Refund handled in RunCode."

    def generate_ticket(self, db, user_id, plan_id, pnr):
        user_query = "SELECT name, email FROM user WHERE id = %s"
        db.cursor.execute(user_query, (user_id,))
        user = db.cursor.fetchone()
        if not user:
            return "Error: User not found!"
        user_name, user_email = user

        plan_query = "SELECT name, departure, destination, time FROM plan WHERE id = %s"
        db.cursor.execute(plan_query, (plan_id,))
        plan = db.cursor.fetchone()
        if not plan:
            return "Error: Flight plan not found!"
        flight_name, flight_from, flight_to, flight_time = plan

        ticket_query = "SELECT seat_type FROM tickets WHERE pnr = %s"
        db.cursor.execute(ticket_query, (pnr,))
        seat_type = db.cursor.fetchone()[0]

        ticket_content = f"""
        === xAIrline Boarding Pass ===
        Passenger Name: {user_name}
        Email: {user_email}
        Flight: {flight_name}
        From: {flight_from}
        To: {flight_to}
        Departure: {flight_time}
        Seats: {seat_type}
        PNR: {pnr}
        Issued: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        =============================
        """
        ticket_filename = f"ticket_{user_id}_{pnr}.txt"
        file_path = os.path.join(os.getcwd(), ticket_filename)
        with open(file_path, "w") as file:
            file.write(ticket_content)
        return f"Ticket generated successfully! Saved at: {file_path}"

    def flight_occupancy(self, db, plan_id):
        query = "SELECT passanger, general, business FROM plan WHERE id = %s"
        db.cursor.execute(query, (plan_id,))
        plan = db.cursor.fetchone()
        if not plan:
            return "Error: Flight not found."
        total_capacity, general, business = plan
        booked_query = "SELECT COUNT(*) FROM tickets WHERE plan_id = %s AND status = 'Booked'"
        db.cursor.execute(booked_query, (plan_id,))
        booked = db.cursor.fetchone()[0]
        occupancy_rate = (booked / total_capacity) * 100 if total_capacity > 0 else 0
        return f"Flight ID: {plan_id}, Occupancy Rate: {occupancy_rate:.2f}% (Booked: {booked}/{total_capacity})"

    def send_notification(self, user_id, message):
        print(f"\n[Notification to {user_id}]: {message}")
        return f"Notification sent to {user_id}: {message}"