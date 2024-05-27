def count_digits(num1, num2):
    count1 = len(str(abs(num1)))
    count2 = len(str(abs(num2)))
    if count1 > count2:
        return f"В числе {num1} больше цифр ({count1})"
    elif count2 > count1:
        return f"В числе {num2} больше цифр ({count2})"
    else:
        return "Количество цифр в числах одинаково"

class Student:
    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date
        self.grades = {}

    def add_grade(self, subject, exam_date, teacher, grade):
        self.grades[subject] = {
            "exam_date": exam_date,
            "teacher": teacher,
            "grade": grade
        }

def input_students():
    students = []
    num_students = int(input("Введите количество студентов: "))
    for i in range(num_students):
        name = input(f"Введите ФИО студента {i+1}: ")
        birth_date = input(f"Введите дату рождения студента {i+1} (гггг-мм-дд): ")
        student = Student(name, birth_date)
        num_grades = int(input(f"Введите количество предметов для студента {i+1}: "))
        for j in range(num_grades):
            subject = input(f"Введите название предмета {j+1}: ")
            exam_date = input(f"Введите дату экзамена для предмета {j+1} (гггг-мм-дд): ")
            teacher = input(f"Введите ФИО преподавателя для предмета {j+1}: ")
            grade = int(input(f"Введите оценку для предмета {j+1}: "))
            student.add_grade(subject, exam_date, teacher, grade)
        students.append(student)
    return students

def find_best_student(students):
    best_student = None
    max_avg_grade = 0
    for student in students:
        total_grade = sum(grade["grade"] for grade in student.grades.values())
        avg_grade = total_grade / len(student.grades)
        if avg_grade > max_avg_grade:
            max_avg_grade = avg_grade
            best_student = student
    return best_student

# Основной код
students = input_students()
best_student = find_best_student(students)
print(f"Студент с лучшей успеваемостью: {best_student.name}")
print("Предметы и оценки:")
for subject, grade_info in best_student.grades.items():
    print(f"{subject}: {grade_info['grade']} ({grade_info['exam_date']}, {grade_info['teacher']})")