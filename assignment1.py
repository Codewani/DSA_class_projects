#Arrays to store data
students = []
grades = []
cartegories = []

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

#Function to sadd students
def add_student():
    if len(students) == 10:
        print("The system has reached the maximum number of students")
        return
    name = input("Enter the student's name: ")
    grade = int(input("Enter your grade: "))

    while not 0 <= grade <= 100:
        print("Error: Ensure your grade is between 0 and 100")
        grade = int(input("Enter your grade: "))
    
    students.append(name)
    grades.append(grade)
    cartegories.append(category(grade))

num_students = int(input("How many students do you want to add? "))

for i in range(num_students):
    add_student()

#Adding the table format
print('\nName        Grade       Category')
print("----------------------------------")
#print("Name      Grade       category")
for i in range(len(students)):
    print(f"{students[i]}    {grades[i]}    {cartegories[i]}")



        