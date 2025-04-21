from datetime import datetime
from collections import deque
import hashlib
import csv
import os
import random
import time

def hash_password(password):
    #Hash a password using SHA-256
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_hash, provided_password):
    #Verify a password against its hash
    return stored_hash == hash_password(provided_password)

class User():
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.tickets = {
            "VIP": 0,
            "Regular": 0
        }

class TicketRequest():
    def __init__(self, user_id, ticket_type):
        self.user_id = user_id
        self.ticket_type = ticket_type
        self.time_of_request = datetime.now()


class TicketSystem():
    def __init__(self):
        self.users = dict()
        self.ticket_types = ["VIP", "Regular"]
        self.max_tickets = 10
        self.ticket_availability = {
            "VIP": 30,
            "Regular": 200
        }
        self.ticket_requests = {
            "VIP": deque(),
            "Regular": deque()
        }
        self.load_users()
        self.load_availability()

    def add_user(self, name, password):
        if name in self.users:
            return False
        else:
            user = User(name, password)
            self.users[name] = user
        self.save_users()
        return True
    

    def authenticate_user(self, name, password):
        if name in self.users and verify_password(self.users[name].password, password):
            return True
        else:
            return False

    def request_ticket(self, user_id, requested_tickets):
        ticket_count =  (self.users[user_id].tickets["VIP"] + self.users[user_id].tickets["Regular"])
        if ticket_count >= self.max_tickets:
            print(f"{user_id}, you have reached the max tickets limit.\n")
            self.log_transaction(user_id, "VIP/Regular", "Max limit reached")
            return False
        
        while requested_tickets["VIP"] > 0 and ticket_count < self.max_tickets:
            if self.ticket_availability["VIP"] == 0:
                print(f"{user_id}, no VIP tickets available.")
                self.log_transaction(user_id, "VIP", "denied")
                break
            ticket_type = "VIP"
            ticket_request = TicketRequest(user_id, ticket_type)
            self.ticket_requests["VIP"].append(ticket_request)
            requested_tickets["VIP"] -= 1
            ticket_count += 1

        while requested_tickets["Regular"] > 0 and ticket_count < self.max_tickets:
            if self.ticket_availability["Regular"] == 0:
                print(f"{user_id}, no Regular tickets available.")
                self.log_transaction(user_id, "Regular", "denied")
                break
            ticket_type = "Regular"
            ticket_request = TicketRequest(user_id, ticket_type)
            self.ticket_requests["Regular"].append(ticket_request)
            requested_tickets["Regular"] -= 1
            ticket_count += 1
        

        return True

    def approve_ticket(self, user_id):
        # if user_id not in self.ticket_requests:
        #     return False
        # ticket_request = self.ticket_requests[user_id]

        while self.ticket_requests["VIP"]:
            if (self.users[user_id].tickets["VIP"] + self.users[user_id].tickets["Regular"]) >= self.max_tickets:
                print(f"{user_id}, you have reached the max tickets limit.\n")
                self.log_transaction(user_id, "VIP", "denied")
                return False
            ticket_request = self.ticket_requests["VIP"].popleft()
            user = ticket_request.user_id
            self.users[user].tickets[ticket_request.ticket_type] += 1
            self.ticket_availability["VIP"] -= 1
            self.save_users()
            self.log_transaction(user, ticket_request.ticket_type, "approved")
            self.save_availability()

        while self.ticket_requests["Regular"]:
            if (self.users[user_id].tickets["VIP"] + self.users[user_id].tickets["Regular"]) >= self.max_tickets:
                print(f"{user_id}, you have reached the max tickets limit.\n")
                self.log_transaction(user_id, "Regular", "denied")
                return False
            ticket_request = self.ticket_requests["Regular"].popleft()
            user = ticket_request.user_id
            self.users[user].tickets[ticket_request.ticket_type] += 1
            self.ticket_availability["Regular"] -= 1
            self.save_users()
            self.log_transaction(user, ticket_request.ticket_type, "approved")
            self.save_availability()
        
        self.save_users()

        if user_id == user:
            print("Ticket request approved.")
            return True
        return True

    def cancel_ticket(self, user_id, cancelled_tickets):
        while cancelled_tickets["VIP"] > 0:
            ticket_type = "VIP"
            if self.users[user_id].tickets[ticket_type] == 0:
                print(f"{user_id}, you have no {ticket_type} tickets to cancel.")
                self.save_users()
                return False
            cancelled_tickets["VIP"] -= 1
            self.users[user_id].tickets[ticket_type] -= 1
            self.ticket_availability[ticket_type] += 1
            print("Here.")
            self.save_availability()
            self.log_transaction(user_id, ticket_type, "cancelled")

        while cancelled_tickets["Regular"] > 0:
            ticket_type = "Regular"
            if self.users[user_id].tickets[ticket_type] == 0:
                print(f"{user_id}, you have no {ticket_type} tickets to cancel.")
                self.save_users()
                return False
            cancelled_tickets["Regular"] -= 1
            self.users[user_id].tickets[ticket_type] -= 1
            self.ticket_availability[ticket_type] += 1
            self.save_availability()
            self.log_transaction(user_id, ticket_type, "cancelled")

        self.log_transaction(user_id, ticket_type, "cancelled")
        self.save_users()
        return True
    

    def load_users(self):
        if os.path.exists("users.csv"):
            with open("users.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) < 3:
                        continue
                    name = row[0]
                    password = row[1]
                    tickets = dict()
                    for ticket in row[2:]:
                        ticket_type, number_of_tickets = ticket.split(":")
                        tickets[ticket_type] = int(number_of_tickets)
                    self.users[name] = User(name, password)
                    self.users[name].tickets = tickets
        else:
            print("No user data found. Starting fresh.")
    

    def load_availability(self):
        if os.path.exists("availability.csv"):
            with open("availability.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) < 2:
                        continue
                    ticket_type = row[0]
                    availability = int(row[1])
                    self.ticket_availability[ticket_type] = availability
        else:
            print("No ticket availability data found. Starting fresh.")
    
    def log_transaction(self, user_id, ticket_type, action):
        with open("transactions.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow([user_id, ticket_type, action, datetime.now()])

        
    def save_users(self):
        with open("users.csv", "w") as file:
            writer = csv.writer(file)
            for user in self.users.values():
                writer.writerow([user.name, user.password, "VIP:" + str(user.tickets["VIP"]), "Regular:" + str(user.tickets["Regular"])])

    def save_availability(self):
        with open("availability.csv", "w") as file:
            writer = csv.writer(file)
            for ticket_type, availability in self.ticket_availability.items():
                writer.writerow([ticket_type, availability])
    
def main():
    system = TicketSystem()
    cur_student = None

    while True:

        if cur_student:
            print("\n🎟️  **Ticket Management System** 🎟️\n")
            print(f"👋 Welcome, {cur_student}!\n")
            print(f"🔑 Logged in as: {system.users[cur_student].name}")
            print("\n[ **Main Menu** ]")
            print("1️⃣  View Available Tickets")
            print("2️⃣  Request a Ticket")
            print("3️⃣  Cancel a Ticket")
            print("4️⃣  View My Tickets")
            print("5️⃣  View Ticket History")
            print("6️⃣  Log Out")
            print("7️⃣  Exit")
        else:
            print("\n🎟️  **Ticket Management System** 🎟️\n")
            print("1️⃣  Register New User")
            print("2️⃣  Log In")
            print("3️⃣  Exit")

        choice = input("\n👉 Enter your choice: ").strip()

        if cur_student:
            if choice == "1":
                print("\n📋 **Available Tickets:**")
                for ticket_type, availability in system.ticket_availability.items():
                    print(f"   - {ticket_type}: {availability} available ✅")
                input("\n🔄 Press any key to continue...")
                time.sleep(1)
            elif choice == "2":
                while True:
                    try:
                        req_vip = input(f"🎫 Enter number of VIP tickets or 'E' to exit this page: ").strip()
                        if req_vip == "E":
                            break
                        vip = int(req_vip)
                        if vip < 0:
                            print("❌ Number of tickets must be at least 0.")
                            continue
                        if vip > system.max_tickets:
                            print(f"❌ Number of tickets cannot exceed {system.max_tickets}.")
                            continue
                        if system.ticket_availability["VIP"] < vip:
                            print(f"❌ Not enough VIP tickets available. Only {system.ticket_availability['VIP']} left.")
                            continue
                        else:
                            break
                    except ValueError:
                        print("❌ Invalid input. Please enter a number.")
                        continue
                if req_vip == "E":
                    continue
                while True:
                    try:
                        req_regular = input(f"🎫 Enter number of Regular tickets: ").strip()
                        if req_regular == "E":
                            break
                        regular = int(req_regular)
                        if regular < 0:
                            print("❌ Number of tickets must be at least 0.")
                            continue
                        if system.ticket_availability["Regular"] < regular:
                            print(f"❌ Not enough Regular tickets available. Only {system.ticket_availability['Regular']} left.")
                            continue
                        if regular + vip > system.max_tickets:
                            print(f"❌ Number of tickets cannot exceed {system.max_tickets}.")
                            continue
                        else:
                            break
                    except ValueError:
                        print("❌ Invalid input. Please enter a number.")
                        continue
                if req_regular == "E" or req_vip == "E":
                    continue
                system.request_ticket(cur_student, {"VIP": vip, "Regular": regular})
                system.approve_ticket(cur_student)
            elif choice == "3":
                while True:
                    try:
                        req_vip = input(f"❌ Enter number of VIP tickets to cancel or 'E' to exit this page: ").strip()
                        if req_vip == "E":
                            break
                        vip = int(req_vip)
                        if vip < 0:
                            print("❌ Number of tickets must be at least 0.")
                            continue
                        if vip > system.users[cur_student].tickets["VIP"]:
                            print(f"❌ You currently only have {system.users[cur_student].tickets['VIP']} VIP tickets.")
                            continue
                        else:
                            break
                    except ValueError:
                        print("❌ Invalid input. Please enter a number.")
                        continue
                if req_vip == "E":
                    continue
                while True:
                    try:
                        req_regular = input(f"❌ Enter number of Regular tickets to cancel: ").strip()
                        if req_regular == "E":
                            break
                        regular = int(req_regular)
                        if regular < 0:
                            print("❌ Number of tickets must be at least 0.")
                            continue
                        if regular > system.users[cur_student].tickets["Regular"]:
                            print(f"❌ You currently only have {system.users[cur_student].tickets['Regular']} Regular tickets.")
                            continue
                        else:
                            break
                    except ValueError:
                        print("❌ Invalid input. Please enter a number.")
                        continue
                if req_regular == "E" or req_vip == "E":
                    continue
                print("🔄 Cancelling tickets...")
                system.cancel_ticket(cur_student, {"VIP": vip, "Regular": regular})
                print("✅ Ticket cancellation request submitted.")
            elif choice == "4":
                print("\n🎟️ **My Tickets:**")
                for ticket_type in system.users[cur_student].tickets:
                    print(f"   - {ticket_type}: {system.users[cur_student].tickets[ticket_type]} 🎫")
                input("\n🔄 Press any key to continue...")
                time.sleep(1)
            elif choice == "5":
                print("\n📜 **Ticket Sales Summary:**")
                print("   - VIP Tickets Sold: ", 30 - system.ticket_availability["VIP"])
                print("   - Regular Tickets Sold: ", 200 - system.ticket_availability["Regular"])
                print("   - Total Tickets Sold: ", (30 - system.ticket_availability["VIP"]) + (200 - system.ticket_availability["Regular"]))
                print()
                print("   - VIP Tickets Available: ", system.ticket_availability["VIP"])
                print("   - Regular Tickets Available: ", 200 - system.ticket_availability["Regular"])
                print("\n")
                input("\n🔄 Press any key to continue...")
                time.sleep(1)
            elif choice == "6":
                cur_student = None
                print("\n✅ Logged out successfully.")
                time.sleep(1)
                print("🔄 Returning to the main menu...\n")
            elif choice == "7":
                break
            else:
                print("❌ Invalid choice. Please try again.")
        else:
            if choice == "1":
                name = input("📝 Enter your name: ").strip()
                password = input("🔒 Enter your password: ").strip()
                hashed_password = hash_password(password)
                while not system.add_user(name, hashed_password):
                    print("❌ User already exists. Please try again, or enter 'E' to exit registration.\n")
                    name = input("📝 Enter your name: ").strip()
                    password = input("🔒 Enter your password: ").strip()
                    if name == "E" or password == "E":
                        break
                    hashed_password = hash_password(password)
            elif choice == "2":
                name = input("🔑 Enter your name or 'E' to exit the Login Page: ").strip()
                if name == "E":
                    time.sleep(1)
                    print("🔄 Exiting the Login page...\n")
                    continue
                password = input("🔒 Enter your password or 'E' to exit the Login Page: ").strip()
                if password == "E":
                    time.sleep(1)
                    print("🔄 Exiting the Login page...\n")
                    continue
                while name != "E" and password != "E" and not system.authenticate_user(name, password):
                    print("❌ Invalid credentials. Please try again or enter 'E' to exit the Login page.\n")
                    name = input("🔑 Enter your name: ").strip()
                    if name == "E":
                        time.sleep(1)
                        print("🔄 Exiting the Login page...\n")
                        break
                    password = input("🔒 Enter your password: ").strip()
                    if password == "E":
                        time.sleep(1)
                        print("🔄 Exiting the Login page...\n")
                        break
                if name == "E" or password == "E":
                    continue
                cur_student = name
                print("\n✅ Logged in successfully.\n")
            elif choice == "3":
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    print("\n👋 Exiting the system. Goodbye!")
    time.sleep(1.3)

if __name__ == "__main__":
    main()
