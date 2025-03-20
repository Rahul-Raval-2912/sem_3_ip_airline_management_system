from datetime import datetime
import random
import string
from Plan import Plan  # Added import to fix "Plan" not defined error

class User:
    def __init__(self, db, name=None, location=None, birthday=None, password=None, email=None, bonus_count=0, wallet_balance=0.00, user_id=None):
        self.db = db
        self.name = name
        self.location = location
        self.birthday = birthday
        self.password = password
        self.email = email
        self.bonus_count = bonus_count
        self.wallet_balance = wallet_balance
        self.id = user_id

    def generate_user_id(self):
        first_name = self.name.split()[0]
        random_number = ''.join(random.choices(string.digits, k=6))
        return f"{first_name}@{random_number}"

    def calculate_age(self, birthday):
        try:
            birth_date = datetime.strptime(birthday, "%Y-%m-%d")
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        except ValueError:
            return -1

    def sign_up(self):
        print("\n=== User Registration ===")
        self.name = input("Full Name: ").strip()
        self.email = input("Email Address: ").strip()
        
        check_email_query = "SELECT email FROM user WHERE email = %s"
        self.db.cursor.execute(check_email_query, (self.email,))
        if self.db.cursor.fetchone():
            print("Error: This email is already registered.")
            return False
        
        self.location = input("Home Address: ").strip()
        self.birthday = input("Birthday (YYYY-MM-DD): ").strip()
        
        age = self.calculate_age(self.birthday)
        if age < 0:
            print("Error: Invalid date format. Use YYYY-MM-DD.")
            return False
        if age < 18:
            print("Error: You must be at least 18 years old.")
            return False
        
        self.password = input("Create Password: ").strip()
        self.id = self.generate_user_id()
        
        check_query = "SELECT id FROM user WHERE id = %s"
        self.db.cursor.execute(check_query, (self.id,))
        if self.db.cursor.fetchone():
            print("Error: User ID conflict. Please try again.")
            return False
        
        try:
            insert_query = """
            INSERT INTO user (id, name, email, location, birthday, password, bonus_count, wallet_balance)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.db.cursor.execute(insert_query, (self.id, self.name, self.email, self.location, self.birthday, self.password, 0, 0.00))
            self.db.conn.commit()
            print(f"Registration successful! Your User ID is: {self.id}")
            return True
        except Exception as e:
            print(f"Error during sign-up: {e}")
            return False

    def log_in(self, user_id, password):
        query = "SELECT id, name, location, birthday, password, bonus_count, email, wallet_balance FROM user WHERE id = %s AND password = %s"
        try:
            self.db.cursor.execute(query, (user_id, password))
            user_data = self.db.cursor.fetchone()
            if not user_data:
                return "Error: Invalid credentials."
            self.id, self.name, self.location, self.birthday, self.password, self.bonus_count, self.email, self.wallet_balance = user_data
            return f"Login successful! Welcome, {self.name} (ID: {self.id})"
        except Exception as e:
            return f"Error during login: {e}"

    def delete_account(self, email, password):
        query_check = "SELECT id, password FROM user WHERE email = %s"
        try:
            self.db.cursor.execute(query_check, (email,))
            user_data = self.db.cursor.fetchone()
            if not user_data:
                return "Error: User not found."
            if user_data[1] != password:
                return "Error: Incorrect password."
            query_delete = "DELETE FROM user WHERE email = %s"
            self.db.cursor.execute(query_delete, (email,))
            self.db.conn.commit()
            self.id = None
            return "Account deleted successfully!"
        except Exception as e:
            return f"Error during account deletion: {e}"

    def update_profile(self, new_name=None, new_location=None, new_password=None):
        print("\n=== Update Profile ===")
        updates = {}
        if new_name:
            updates["name"] = new_name
        if new_location:
            updates["location"] = new_location
        if new_password:
            updates["password"] = new_password
        
        if not updates:
            print("No changes provided.")
            return
        
        query_parts = [f"{key} = %s" for key in updates.keys()]
        query = f"UPDATE user SET {', '.join(query_parts)} WHERE id = %s"
        params = list(updates.values()) + [self.id]
        try:
            self.db.cursor.execute(query, params)
            self.db.conn.commit()
            self.db.cursor.execute("SELECT id, name, location, birthday, password, bonus_count, email, wallet_balance FROM user WHERE id = %s", (self.id,))
            user_data = self.db.cursor.fetchone()
            self.name, self.location, self.password = user_data[1], user_data[2], user_data[4]
            self.bonus_count, self.email, self.wallet_balance = user_data[5], user_data[6], user_data[7]
            print("Profile updated successfully!")
        except Exception as e:
            print(f"Error updating profile: {e}")

    def get_booking_history(self):
        query = "SELECT pnr, plan_id, seat_type, price, status FROM tickets WHERE user_id = %s ORDER BY pnr DESC"
        self.db.cursor.execute(query, (self.id,))
        tickets = self.db.cursor.fetchall()
        if not tickets:
            return "No booking history."
        output = "\n=== Booking History ===\n"
        for ticket in tickets:
            pnr, plan_id, seat_type, price, status = ticket
            output += f"PNR: {pnr}, Flight ID: {plan_id}, Seats: {seat_type}, Price: ${float(price):.2f}, Status: {status}\n"
        return output

    def request_flight_status(self, plan_id):
        plan = Plan.load_from_db(self.db, plan_id)
        if not plan:
            return "Error: Flight not found."
        status = plan.get_status()
        return f"Flight {plan.name} (ID: {plan_id}) Status: {status}"