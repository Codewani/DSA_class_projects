
#Arrays to store data
students = []
grades = []
categories = []

#Function to categorize the grades
def category(grade):
    if 90 <= grade <= 100:
        return "Excellent"
    elif grade >= 80:
        return "Good"
    elif grade >= 70:
        return "Average"
    else:
        return "Needs Improvement"

#Function to add students
def add_student():
    if len(students) == 10:
        print("The system has reached the maximum number of students")
        return
        
    name = input("Enter the student's name: ")
    
    #Ensuring users enter numeric grades
    while True:
        try:
            grade = int(input("Enter your grade: "))
            if 0 <= grade <= 100:
                break
            else:
                print("Error: Ensure your grade is between 0 and 100")
        except ValueError:
            print("Error: Please enter a valid number for the grade.")
    
    students.append(name)
    grades.append(grade)
    categories.append(category(grade))

num_students = int(input("How many students do you want to add? "))

for i in range(num_students):
    add_student()

#Adding the table format using the .ljust() for alignment
print('\nName        Grade       Category')
print("----------------------------------")

for i in range(len(students)):
    print(f"{students[i].ljust(12)} {str(grades[i]).ljust(10)} {categories[i]}") # .ljust() for alignment




        