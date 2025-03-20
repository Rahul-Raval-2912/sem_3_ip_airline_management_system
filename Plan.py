from datetime import datetime

class Plan:
    def __init__(self, db, name, passenger, general, business, departure, destination, time, landing_time=None, plan_id=None):
        self.db = db
        self.name = name
        self.passenger = passenger
        self.general = general
        self.business = business
        self.departure = departure
        self.destination = destination
        self.time = self._parse_time(time)
        self.landing_time = self._parse_time(landing_time) if landing_time else None
        self.id = plan_id

    def _parse_time(self, time_str):
        try:
            if isinstance(time_str, str):
                return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            return time_str
        except ValueError:
            raise ValueError("Time must be in 'YYYY-MM-DD HH:MM:SS' format")

    def save_to_db(self):
        try:
            if self.id is None:
                query = """
                INSERT INTO plan (name, passanger, general, business, departure, destination, time, landing_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                self.db.cursor.execute(query, (self.name, self.passenger, self.general, self.business,
                                              self.departure, self.destination, self.time, self.landing_time))
                self.db.conn.commit()
                self.id = self.db.cursor.lastrowid
                return f"Flight plan '{self.name}' added successfully! ID: {self.id}"
            else:
                query = """
                UPDATE plan SET name = %s, passanger = %s, general = %s, business = %s,
                                departure = %s, destination = %s, time = %s, landing_time = %s
                WHERE id = %s
                """
                self.db.cursor.execute(query, (self.name, self.passenger, self.general, self.business,
                                              self.departure, self.destination, self.time, self.landing_time, self.id))
                self.db.conn.commit()
                return f"Flight plan '{self.name}' (ID: {self.id}) updated successfully!"
        except Exception as e:
            return f"Error saving flight plan: {e}"

    def delete_from_db(self):
        if not self.id:
            return "Error: No plan ID set."
        try:
            query_check = "SELECT user_id FROM tickets WHERE plan_id = %s AND status = 'Booked'"
            self.db.cursor.execute(query_check, (self.id,))
            booked_passengers = self.db.cursor.fetchall()
            if booked_passengers:
                for user_id in booked_passengers:
                    self._process_refund(user_id[0])
            self.db.cursor.execute("DELETE FROM plan WHERE id = %s", (self.id,))
            self.db.conn.commit()
            return f"Flight plan '{self.name}' (ID: {self.id}) deleted successfully!"
        except Exception as e:
            return f"Error deleting flight plan: {e}"

    def _process_refund(self, user_id):
        try:
            query_ticket = "SELECT price FROM tickets WHERE user_id = %s AND plan_id = %s AND status = 'Booked'"
            self.db.cursor.execute(query_ticket, (user_id, self.id))
            ticket = self.db.cursor.fetchone()
            if ticket:
                refund_amount = ticket[0] * 0.8
                query_update = "UPDATE tickets SET status = 'Canceled', refund_status = 'Refunded' WHERE user_id = %s AND plan_id = %s"
                self.db.cursor.execute(query_update, (user_id, self.id))
                query_wallet = "UPDATE user SET wallet_balance = wallet_balance + %s WHERE id = %s"
                self.db.cursor.execute(query_wallet, (refund_amount, user_id))
                self.db.conn.commit()
        except Exception as e:
            print(f"Error processing refund for user {user_id}: {e}")

    @staticmethod
    def get_all_plans(db):
        query = "SELECT * FROM plan"
        db.cursor.execute(query)
        plans = db.cursor.fetchall()
        if not plans:
            return "No flight plans available."
        output = "\n=== Flight Plans ===\n"
        for p in plans:
            output += f"ID: {p[0]}, {p[1]}, {p[5]} → {p[6]}, Dep: {p[7]}\n"
        return output

    @classmethod
    def load_from_db(cls, db, plan_id):
        query = "SELECT name, passanger, general, business, departure, destination, time, landing_time FROM plan WHERE id = %s"
        db.cursor.execute(query, (plan_id,))
        plan_data = db.cursor.fetchone()
        if not plan_data:
            return None
        return cls(db, name=plan_data[0], passenger=plan_data[1], general=plan_data[2], business=plan_data[3],
                   departure=plan_data[4], destination=plan_data[5], time=plan_data[6], landing_time=plan_data[7], plan_id=plan_id)

    def get_status(self):
        now = datetime.now()
        if now < self.time:
            return "Scheduled"
        elif now >= self.time and now <= self.landing_time:
            return "In Flight"
        else:
            return "Completed"

    def get_available_seats(self, seat_type):
        count = self.general if seat_type == "General" else self.business
        booked_query = "SELECT seat_type FROM tickets WHERE plan_id = %s AND status = 'Booked'"
        self.db.cursor.execute(booked_query, (self.id,))
        booked_tickets = self.db.cursor.fetchall()
        booked_seats = []
        for ticket in booked_tickets:
            if seat_type in ticket[0]:
                try:
                    seats_str = ticket[0].split('(')[1].rstrip(')').split(', ')
                    booked_seats.extend(seats_str)
                except IndexError:
                    # Handle cases where seat_type might not have labels
                    booked_seats.append(f"{seat_type} seat")

        # Generate seats up to the full count
        all_seats = []
        rows = "ABCDEFGHIJ"  # Extended rows to accommodate larger counts
        seats_per_row = 10  # Increased to allow more seats per row
        total_seats_needed = count
        row_idx = 0
        seat_idx = 1

        while len(all_seats) < total_seats_needed and row_idx < len(rows):
            seat_label = f"{rows[row_idx]}{seat_idx}"
            all_seats.append(seat_label)
            seat_idx += 1
            if seat_idx > seats_per_row:
                seat_idx = 1
                row_idx += 1

        return [seat for seat in all_seats if seat not in booked_seats]

    def update_status(self, new_status):
        valid_statuses = ["Scheduled", "In Flight", "Completed", "Delayed", "Cancelled"]
        if new_status not in valid_statuses:
            return f"Error: Invalid status. Use one of {', '.join(valid_statuses)}."
        return f"Flight {self.name} status updated to {new_status}."