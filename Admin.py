import random
import string

class Admin:
    def __init__(self, db, name=None, location=None, email=None, phone_number=None, password=None):
        self.db = db
        self.name = name
        self.location = location
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.id = None

    def log_in(self, email, password):
        query = "SELECT id, name, password FROM admin WHERE email = %s"
        try:
            self.db.cursor.execute(query, (email,))
            admin_data = self.db.cursor.fetchone()
            if not admin_data:
                return "Error: Admin email not found."
            if admin_data[2] != password:
                return "Error: Incorrect password."
            self.id = admin_data[0]
            self.name = admin_data[1]
            self.email = email
            self.password = password
            return f"Admin login successful! Welcome, {self.name} (ID: {self.id})"
        except Exception as e:
            return f"Error during login: {e}"

    def log_out(self):
        self.id = None
        self.name = None
        self.email = None
        self.password = None
        return "Admin logged out successfully."

    def add_plan(self, name, passenger_capacity, general_seats, business_seats, origin, destination, time, landing_time):
        query = """
        INSERT INTO plan (name, passanger, general, business, departure, destination, time, landing_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            self.db.cursor.execute(query, (name, passenger_capacity, general_seats, business_seats, origin, destination, time, landing_time))
            self.db.conn.commit()
            plan_id = self.db.cursor.lastrowid
            return f"Flight plan '{name}' added successfully! ID: {plan_id}"
        except Exception as e:
            return f"Error adding flight plan: {e}"

    def remove_plan(self, plan_id):
        query_check = "SELECT name FROM plan WHERE id = %s"
        self.db.cursor.execute(query_check, (plan_id,))
        plan_data = self.db.cursor.fetchone()
        if not plan_data:
            return "Error: Plan not found."
        plan_name = plan_data[0]

        query_notify = "SELECT user_id FROM tickets WHERE plan_id = %s AND status = 'Booked'"
        self.db.cursor.execute(query_notify, (plan_id,))
        booked_passengers = self.db.cursor.fetchall()

        if booked_passengers:
            for user_id in booked_passengers:
                self.process_refund(user_id[0], plan_id)

        self.db.cursor.execute("DELETE FROM plan WHERE id = %s", (plan_id,))
        self.db.conn.commit()
        return f"Flight plan '{plan_name}' removed successfully!"

    def process_refund(self, user_id, plan_id):
        try:
            query_ticket = "SELECT price FROM tickets WHERE user_id = %s AND plan_id = %s AND status = 'Booked'"
            self.db.cursor.execute(query_ticket, (user_id, plan_id))
            ticket = self.db.cursor.fetchone()
            if ticket:
                refund_amount = ticket[0] * 0.8
                query_update = "UPDATE tickets SET status = 'Canceled', refund_status = 'Refunded' WHERE user_id = %s AND plan_id = %s"
                self.db.cursor.execute(query_update, (user_id, plan_id))
                query_wallet = "UPDATE user SET wallet_balance = wallet_balance + %s WHERE id = %s"
                self.db.cursor.execute(query_wallet, (refund_amount, user_id))
                self.db.conn.commit()
        except Exception as e:
            print(f"Error processing refund for user {user_id}: {e}")

    def update_plan_details(self, plan_id, name=None, passenger=None, general=None, business=None, departure=None, destination=None, time=None, landing_time=None):
        try:
            query = "UPDATE plan SET "
            values = []
            if name:
                query += "name = %s, "
                values.append(name)
            if passenger is not None:
                query += "passanger = %s, "
                values.append(passenger)
            if general is not None:
                query += "general = %s, "
                values.append(general)
            if business is not None:
                query += "business = %s, "
                values.append(business)
            if departure:
                query += "departure = %s, "
                values.append(departure)
            if destination:
                query += "destination = %s, "
                values.append(destination)
            if time:
                query += "time = %s, "
                values.append(time)
            if landing_time:
                query += "landing_time = %s, "
                values.append(landing_time)
            if not values:
                return "Error: No updates provided!"
            query = query.rstrip(", ") + " WHERE id = %s"
            values.append(plan_id)
            self.db.cursor.execute(query, tuple(values))
            self.db.conn.commit()
            return f"Flight plan ID {plan_id} updated successfully!"
        except Exception as e:
            return f"Error updating plan: {e}"

    def view_plans(self):
        query = "SELECT * FROM plan"
        self.db.cursor.execute(query)
        plans = self.db.cursor.fetchall()
        if not plans:
            return "No flight plans available."
        output = "\n=== Flight Plans ===\n"
        for p in plans:
            output += f"ID: {p[0]}, {p[1]}, {p[5]} → {p[6]}, Dep: {p[7]}, Arr: {p[8]}\n"
        return output

    def view_users(self):
        query = "SELECT id, name, email, location FROM user"
        self.db.cursor.execute(query)
        users = self.db.cursor.fetchall()
        if not users:
            return "No users registered."
        output = "\n=== Registered Users ===\n"
        for u in users:
            output += f"ID: {u[0]}, Name: {u[1]}, Email: {u[2]}, Location: {u[3]}\n"
        return output

    def remove_user(self, user_id):
        query = "DELETE FROM user WHERE id = %s"
        self.db.cursor.execute(query, (user_id,))
        self.db.conn.commit()
        return f"User {user_id} removed successfully!"

    def view_feedback(self):
        query = "SELECT name, email, feedback FROM feedback"
        self.db.cursor.execute(query)
        feedbacks = self.db.cursor.fetchall()
        if not feedbacks:
            return "No feedback available."
        output = "\n=== User Feedback ===\n"
        for f in feedbacks:
            output += f"Name: {f[0]}, Email: {f[1]}, Feedback: {f[2]}\n"
        return output

    def view_booking_stats(self):
        query = "SELECT plan_id, COUNT(*) as bookings FROM tickets WHERE status = 'Booked' GROUP BY plan_id"
        self.db.cursor.execute(query)
        stats = self.db.cursor.fetchall()
        if not stats:
            return "No bookings recorded."
        output = "\n=== Booking Statistics ===\n"
        for stat in stats:
            plan_id, bookings = stat
            self.db.cursor.execute("SELECT name FROM plan WHERE id = %s", (plan_id,))
            plan_name = self.db.cursor.fetchone()[0]
            output += f"Flight ID: {plan_id}, {plan_name}, Bookings: {bookings}\n"
        return output

    def view_revenue(self):
        query = "SELECT SUM(amount) FROM payments WHERE status = 'Success'"
        self.db.cursor.execute(query)
        total = self.db.cursor.fetchone()[0] or 0
        return f"Total Revenue: ${total:.2f}"

    def broadcast_notification(self, message):
        query = "SELECT id FROM user"
        self.db.cursor.execute(query)
        users = self.db.cursor.fetchall()
        for user in users:
            print(f"[Broadcast to {user[0]}]: {message}")
        return "Broadcast sent to all users."