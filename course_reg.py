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

def parse_time_range(time_range: str):
        parts = time_range.split('-')
        if len(parts) != 2:
            return None, None
        start_str = parts[0].strip()  
        end_str = parts[1].strip()    
        try:
            start_time = datetime.strptime(start_str, "%I:%M %p")
            end_time = datetime.strptime(end_str, "%I:%M %p")
            return start_time, end_time
        except ValueError:
            return None, None
        
class Student:
    def __init__(self, student_id: str, name: str, password: str):
        self.student_id = student_id
        self.name = name
        self.password = password
        self.registered_courses: Set[str] = set()

    def __repr__(self) -> str:
        return f"Student(ID: {self.student_id}, Name: {self.name}, Password: {self.password})"

class Course:
    def __init__(self, course_id: str, name: str, instructor: str, max_students: int = 30, time: str = ""):
        self.course_id = course_id
        self.name = name
        self.instructor = instructor
        self.max_students = max_students
        self.time = time
        self.enrolled_students: Set[str] = set()

    def __str__(self) -> str:
        return f"Course(ID: {self.course_id}, Name: {self.name}, Instructor: {self.instructor}, Time: {self.time})"

class EnrollmentSystem:
    def __init__(self):
        self.students = {}
        self.courses = {}
        self.load_data()
        if not self.courses:
            self.initialize_courses()

    def initialize_courses(self):
        courses = [
            ("CS101", "Introduction to Programming", "Dr. Smith", 30, "10:00 AM - 11:30 AM"),
            ("CS102", "Data Structures", "Dr. Johnson", 30, "11:00 AM - 12:30 PM"),
            ("CS103", "Algorithms", "Dr. Williams", 30, "3:00 PM - 4:30 PM"),
            ("CS104", "Database Systems", "Dr. Brown", 30, "10:00 AM - 11:30 AM"),
            ("CS105", "Web Development", "Dr. Davis", 30, "1:00 PM - 2:30 PM"),
            ("CS106", "Software Engineering", "Dr. Miller", 30, "3:00 PM - 4:30 PM"),
            ("CS107", "Computer Networks", "Dr. Wilson", 30, "10:00 AM - 11:30 AM"),
            ("CS108", "Operating Systems", "Dr. Moore", 30, "1:00 PM - 2:30 PM"),
            ("CS109", "Machine Learning", "Dr. Taylor", 30, "3:00 PM - 4:30 PM")
        ]
        for course_id, name, instructor, max_students, time in courses:
            self.courses[course_id] = Course(course_id, name, instructor, max_students, time)
    
    def get_time_conflict(self, student_id: str, new_course_id: str):
        student = self.students[student_id]
        new_course = self.courses[new_course_id]
        
        # If the new course has no time set, assume no conflict.
        if not new_course.time:
            return None

        new_start, new_end = parse_time_range(new_course.time)
        if not new_start or not new_end:
            return None

        # Check each already registered course for overlap
        for course_id in student.registered_courses:
            enrolled_course = self.courses[course_id]
            if not enrolled_course.time:
                continue
            exist_start, exist_end = parse_time_range(enrolled_course.time)
            if not exist_start or not exist_end:
                continue
            # Check for overlapping intervals:
            if new_start < exist_end and new_end > exist_start:
                return enrolled_course  # Return the conflicting course
        return None


    
    def register_student(self, student_id: str, name: str, password: str) -> bool:
        if student_id in self.students:
            print("Error: Student ID already exists")
            return False
        hashed_password = hash_password(password)
        self.students[student_id] = Student(student_id, name, hashed_password)
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
            print(f"Time: {course.time}")
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
        
        # Check for a time conflict using the new method.
        conflict_course = self.get_time_conflict(student_id, course_id)
        if conflict_course:
            print(f"Error: Time conflict with your registered course '{conflict_course.course_id}'.")
            print(f"'{conflict_course.course_id}' is currently held at {conflict_course.time}.")
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
            print(f"Time: {course.time}")
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

    def save_courses(self):
        with open('courses.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for course in self.courses.values():
                writer.writerow([course.course_id, course.name, course.instructor, 
                                course.max_students, course.time, ','.join(course.enrolled_students)])

    def save_enrollment(self, student_id: str, course_id: str):
        with open('enrollments.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([student_id, course_id, datetime.now()])
    
    def save_students(self):
        with open('students.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for student in self.students.values():
                writer.writerow([student.student_id, student.name, student.password, ','.join(student.registered_courses)])
      
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

    def load_data(self):
        if os.path.exists('students.csv'):
            with open('students.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    student_id, name, password, registered_courses = row
                    # Store the password as-is, it's already hashed
                    student = Student(student_id, name, password)
                    if registered_courses:
                        student.registered_courses = set(registered_courses.split(','))
                    self.students[student_id] = student

        if os.path.exists('courses.csv'):
            with open('courses.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 6:  # Make sure we have at least 6 columns (including time)
                        course_id, name, instructor, max_students, time, enrolled_students = row
                        course = Course(course_id, name, instructor, int(max_students), time)
                        if enrolled_students:
                            course.enrolled_students = set(enrolled_students.split(','))
                    else:  # Backward compatibility for files without time
                        course_id, name, instructor, max_students, enrolled_students = row
                        course = Course(course_id, name, instructor, int(max_students))
                        if enrolled_students:
                            course.enrolled_students = set(enrolled_students.split(','))
                    self.courses[course_id] = course

def show_banner():
    print("\nGRAMBLING STATE UNIVERSITY")
    print("=" * 60)
    print("\nCourse Registration System")
    print("=" * 60)

def main():
    system = EnrollmentSystem()
    cur_student = None

    while True:
        if cur_student:
            print("Please select an option:")
            print("-" * 60)
            print("1. View available courses")
            print("2. Enroll in course")
            print("3. Drop course")
            print("4. View student schedule")
            print("5. View enrollment history")
            print("6. Log out")
            print("7. Exit")
        else:
            show_banner()
            print("Please select an option:")
            print("-" * 60)
            print("1. Register new student")
            print("2. Log In")
            print("3. Exit")

        choice = input("Enter your choice (1-7): ") if cur_student else input("Enter your choice (1-3): ")

        if not cur_student:
            show_banner()
            if choice == '1':
                print("\nWelcome to the Sign up Page.\n")
                student_id = input("Enter student ID: ")
                name = input("Enter student name: ")
                password = input("Enter your password: ")
                system.register_student(student_id, name, password)

            elif choice == '2':
                print("\nWelcome to the Log in Page.\n")
                student_id = input("Enter student ID or 'E' to exit out of the Login page: ")
                if student_id == 'E':
                    continue
                password = input("Enter your password or 'E' to exit out of the Login page: ")
                if password == 'E':
                    continue
                while student_id not in system.students or not verify_password(system.students[student_id].password, password):
                    print("The student_id and password combination you entered is not valid.")
                    student_id = input("Enter student ID or 'E' to exit out of the Login page: ")
                    if student_id == 'E':
                        break
                    password = input("Enter your password or 'E' to exit out of the Login page: ")
                    if password == 'E':
                        break
                if student_id == 'E' or password == 'E':
                    continue

                cur_student = student_id        

            elif choice == '3':
                print("Thank you for using the Course Registration System!")
                break

        else:
            if choice == '1':
                system.view_available_courses()

            elif choice == '2':
                student_id = cur_student
                system.view_available_courses()
                course_id = input("Enter the course ID or 'E' to exit this page: ")
                while course_id != 'E' and not system.enroll_student(student_id, course_id):
                    course_id = input("Enter course ID or 'E' to exit this page: ")

            elif choice == '3':
                student_id = cur_student
                print("\nHere are the classes you are taking: \n")
                system.view_student_schedule(student_id)
                print()
                course_id = input("Enter course ID of the course you want to drop or 'E' to exit this page: ")
                while course_id != 'E' and not system.drop_course(student_id, course_id):
                    print("Please Enter a course ID for a course you are enrolled in or 'E' if you have not enrolled in any courses.")
                    course_id = input("Enter course ID or 'E' to exit this page: ")

            elif choice == '4':
                student_id = cur_student
                system.view_student_schedule(student_id)

            elif choice == '5':
                system.view_enrollment_history()

            elif choice == '6':
                cur_student = None
            elif choice == '7':
                print("Thank you for using the Course Registration System!")
                break
            else:
                print("Invalid choice. Please try again.")
        print("\n" + "-" * 60)

if __name__ == "__main__":
    main()
