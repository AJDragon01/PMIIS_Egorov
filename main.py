import sqlite3
import os


def count_digits(num1, num2):
    count1 = len(str(abs(num1)))
    count2 = len(str(abs(num2)))
    if count1 > count2:
        return f"В числе {num1} больше цифр ({count1})"
    elif count2 > count1:
        return f"В числе {num2} больше цифр ({count2})"
    else:
        return "Количество цифр в числах одинаково"


def create_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, birth_date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS grades
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, subject TEXT, exam_date TEXT, teacher TEXT, grade INTEGER, FOREIGN KEY(student_id) REFERENCES students(id))''')
    conn.commit()
    conn.close()



class Student:
    def __init__(self, name, birth_date, id=None):
        self.name = name
        self.birth_date = birth_date
        self.id = id
        self.grades = {}

    def add_grade(self, subject, exam_date, teacher, grade):
        self.grades[subject] = {
            "exam_date": exam_date,
            "teacher": teacher,
            "grade": grade
        }

def input_students():
    choice = input("Введите 1 для ввода данных вручную или 2 для чтения из базы данных: ")

    if choice == '1':
        # Ввод данных вручную
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

    elif choice == '2':
        # Чтение данных из базы данных
        if os.path.exists('students.db'):
            conn = sqlite3.connect('students.db')
            c = conn.cursor()
            c.execute("SELECT * FROM students")
            students_data = c.fetchall()
            students = []
            for student_data in students_data:
                student_id, name, birth_date = student_data
                student = Student(name, birth_date, student_id)
                c.execute("SELECT subject, exam_date, teacher, grade FROM grades WHERE student_id = ?", (student_id,))
                grades_data = c.fetchall()
                for grade_data in grades_data:
                    subject, exam_date, teacher, grade = grade_data
                    student.add_grade(subject, exam_date, teacher, grade)
                students.append(student)
            conn.close()
            return students
        else:
            print("База данных не найдена. Создайте базу данных или введите данные вручную.")
            return []
    else:
        print("Неверный выбор. Попробуйте еще раз.")
        return input_students()

def find_best_student(students):
    best_student = None
    max_avg_grade = 0
    for student in students:
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("SELECT subject, grade FROM grades WHERE student_id = ?", (student.id,))
        grades = c.fetchall()
        total_grade = sum(grade[1] for grade in grades)
        avg_grade = total_grade / len(grades)
        conn.close()
        if avg_grade > max_avg_grade:
            max_avg_grade = avg_grade
            best_student = student
    return best_student

# Основной код
students = input_students()
best_student = find_best_student(students)
conn = sqlite3.connect('students.db')
c = conn.cursor()
c.execute("SELECT students.name, grades.subject, grades.grade, grades.exam_date, grades.teacher FROM students INNER JOIN grades ON students.id = grades.student_id WHERE students.id = ?", (best_student.id,))
grades = c.fetchall()
conn.close()


print(f"Студент с лучшей успеваемостью: {best_student.name}")
print("Предметы и оценки:")
for grade in grades:
    print(f"{grade[1]}: {grade[2]} ({grade[3]}, {grade[4]})")