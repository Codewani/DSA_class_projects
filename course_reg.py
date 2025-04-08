import csv
import hashlib
import os
from typing import Set
from datetime import datetime

def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_hash: str, provided_password: str) -> bool:
    """Verify a password against its hash"""
    return stored_hash == hash_password(provided_password)

class Student:
    def __init__(self, student_id: str, name: str, password: str, already_hashed= False):
        self.student_id = student_id
        self.name = name
        if already_hashed:
            self.password = password
        else:
            # Hash the password before storing it
            self.password = hash_password(password)
        self.registered_courses: Set[str] = set()

    def __repr__(self) -> str:
        return f"Student(ID: {self.student_id}, Name: {self.name}, Password: {self.password})"

class Course:
    def __init__(self, course_id: str, name: str, instructor: str, max_students: int = 30):
        self.course_id = course_id
        self.name = name
        self.instructor = instructor
        self.max_students = max_students
        self.enrolled_students: Set[str] = set()

    def __str__(self) -> str:
        return f"Course(ID: {self.course_id}, Name: {self.name}, Instructor: {self.instructor})"

class EnrollmentSystem:
    def __init__(self):
        self.students = {}
        self.courses = {}
        self.load_data()
        if not self.courses:
            self.initialize_courses()

    def initialize_courses(self):
        courses = [
            ("CS101", "Introduction to Programming", "Dr. Smith"),
            ("CS102", "Data Structures", "Dr. Johnson"),
            ("CS103", "Algorithms", "Dr. Williams"),
        ]
        for course_id, name, instructor in courses:
            self.courses[course_id] = Course(course_id, name, instructor)

    def register_student(self, student_id: str, name: str, password: str) -> bool:
        if student_id in self.students:
            print("Error: Student ID already exists")
            return False
        self.students[student_id] = Student(student_id, name, password)
        self.save_students()
        print(f"Successfully registered student: {name}")
        return True

    def view_available_courses(self):
        print("\nAvailable Courses:")
        print("-" * 60)
        for course in self.courses.values():
            available_slots = course.max_students - len(course.enrolled_students)
            print(f"Course ID: {course.course_id}")
            print(f"Name: {course.name}")
            print(f"Instructor: {course.instructor}")
            print(f"Available slots: {available_slots}")
            print("-" * 60)

    def enroll_student(self, student_id: str, course_id: str) -> bool:
        if student_id not in self.students:
            print("Error: Student not found")
            return False

        if course_id not in self.courses:
            print("Error: Course not found")
            return False

        student = self.students[student_id]
        course = self.courses[course_id]

        if course_id in student.registered_courses:
            print("Error: Student already enrolled in this course")
            return False

        if len(course.enrolled_students) >= course.max_students:
            print("Error: Course is full")
            return False

        student.registered_courses.add(course_id)
        course.enrolled_students.add(student_id)
        print(f"Successfully enrolled {student.name} in {course.name}")
        self.save_enrollment(student_id, course_id)
        self.save_students()
        self.save_courses()
        self.log_enrollment_action(student_id, course_id, "ENROLL")  # Log ENROLL
        return True

    def drop_course(self, student_id: str, course_id: str) -> bool:
        if student_id not in self.students or course_id not in self.courses:
            print("Error: Invalid student ID or course ID")
            return False

        student = self.students[student_id]
        course = self.courses[course_id]

        if course_id not in student.registered_courses:
            print("Error: Student is not enrolled in this course")
            return False

        student.registered_courses.remove(course_id)
        course.enrolled_students.remove(student_id)
        print(f"Successfully dropped {course.name} for {student.name}")

        self.save_students()
        self.save_courses()
        self.update_enrollments()
        self.log_enrollment_action(student_id, course_id, "DROP")  # Log DROP
        return True

    def view_student_schedule(self, student_id: str):
        if student_id not in self.students:
            print("Error: Student not found")
            return

        student = self.students[student_id]
        print(f"\nSchedule for {student.name}:")
        print("-" * 60)
        for course_id in student.registered_courses:
            course = self.courses[course_id]
            print(f"Course: {course.name} (ID: {course.course_id})")
            print(f"Instructor: {course.instructor}")
            print("-" * 60)
    
    def view_enrollment_history(self):
        if not os.path.exists('enrollment_history.csv'):
            print("No enrollment history found.")
            return

        print("\nEnrollment History:")
        print("-" * 60)
        with open('enrollment_history.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                student_id, course_id, action, timestamp = row
                print(f"Student ID: {student_id} | Course ID: {course_id} | Action: {action} | Time: {timestamp}")
        print("-" * 60)


    def save_students(self):
        with open('students.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for student in self.students.values():
                writer.writerow([student.student_id, student.name, student.password, ','.join(student.registered_courses)])

    def save_courses(self):
        with open('courses.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for course in self.courses.values():
                writer.writerow([course.course_id, course.name, course.instructor, course.max_students, ','.join(course.enrolled_students)])

    def save_enrollment(self, student_id: str, course_id: str):
        with open('enrollments.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([student_id, course_id, datetime.now()])

    def load_data(self):
        if os.path.exists('students.csv'):
            with open('students.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    student_id, name, password, registered_courses = row
                    student= Student(student_id, name, password, already_hashed=True)
                    if registered_courses:
                        student.registered_courses = set(registered_courses.split(','))
                    self.students[student_id] = student

        if os.path.exists('courses.csv'):
            with open('courses.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    course_id, name, instructor, max_students, enrolled_students = row
                    course = Course(course_id, name, instructor, int(max_students))
                    if enrolled_students:
                        course.enrolled_students = set(enrolled_students.split(','))
                    self.courses[course_id] = course

    def update_enrollments(self):
        enrollments = []
        for student in self.students.values():
            for course_id in student.registered_courses:
                enrollments.append([student.student_id, course_id, datetime.now()])

        with open('enrollments.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for enrollment in enrollments:
                writer.writerow(enrollment)

    def log_enrollment_action(self, student_id: str, course_id: str, action: str):
        with open('enrollment_history.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([student_id, course_id, action, datetime.now()])


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPress Enter to continue...")

def print_title(title):
    print("\n" + "=" * 60)
    print(title.center(60))
    print("=" * 60)

def main():
    system = EnrollmentSystem()
    cur_student = None
    assert hash_password("1234") == hash_password("1234")

    while True:
        clear_screen()
        print_title("🏛️ University Course Registration System 🏛️")

        if cur_student:
            print("Logged in as:", system.students[cur_student].name)
            print("\n[ Main Menu ]")
            print("1. 📚 View Available Courses")
            print("2. 📝 Enroll in a Course")
            print("3. ❌ Drop a Course")
            print("4. 📅 View My Schedule")
            print("5. 📜 View Enrollment History")
            print("6. 🔓 Log Out")
            print("7. 🚪 Exit")
        else:
            print("\n[ Welcome ]")
            print("1. 🆕 Register New Student")
            print("2. 🔐 Log In")
            print("3. 🚪 Exit")

        choice = input("\nEnter your choice: ").strip()

        if not cur_student:
            if choice == '1':
                clear_screen()
                print_title("🆕 Register New Student")
                student_id = input("Enter student ID: ").strip()
                name = input("Enter student name: ").strip()
                password = input("Enter your password: ").strip()
                if system.register_student(student_id, name, password):
                    print("✅ Successfully registered!")
                else:
                    print("❌ Registration failed. Try again.")
                pause()

            elif choice == '2':
                clear_screen()
                print_title("🔐 Student Log In")
                student_id = input("Enter student ID: ").strip()
                password = input("Enter password: ").strip()
                if student_id in system.students and verify_password(system.students[student_id].password, password):
                    cur_student = student_id
                    print("✅ Login successful!")
                else:
                    print("❌ Invalid ID or password.")
                pause()

            elif choice == '3':
                print("\nThank you for using the Course Registration System!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
                pause()

        else:
            if choice == '1':
                clear_screen()
                system.view_available_courses()
                pause()

            elif choice == '2':
                clear_screen()
                system.view_available_courses()
                course_id = input("\nEnter Course ID to enroll (or 'E' to exit): ").strip()
                if course_id.upper() != 'E':
                    if system.enroll_student(cur_student, course_id):
                        print("✅ Enrollment successful!")
                    else:
                        print("❌ Enrollment failed.")
                pause()

            elif choice == '3':
                clear_screen()
                system.view_student_schedule(cur_student)
                course_id = input("\nEnter Course ID to drop (or 'E' to exit): ").strip()
                if course_id.upper() != 'E':
                    if system.drop_course(cur_student, course_id):
                        print("✅ Course dropped successfully!")
                    else:
                        print("❌ Drop failed.")
                pause()

            elif choice == '4':
                clear_screen()
                system.view_student_schedule(cur_student)
                pause()

            elif choice == '5':
                clear_screen()
                system.view_enrollment_history()
                pause()

            elif choice == '6':
                cur_student = None
                print("🔓 Logged out successfully.")
                pause()

            elif choice == '7':
                print("\nThank you for using the Course Registration System!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
                pause()

        print("\n" + "-" * 60)

if __name__ == "__main__":
    main()
