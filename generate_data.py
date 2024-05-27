import sqlite3
import random
from datetime import date, timedelta

# Списки русских имен, фамилий и отчеств
russian_names = ['Александр', 'Андрей', 'Анна', 'Василий', 'Виктор', 'Дмитрий', 'Екатерина', 'Елена', 'Иван', 'Игорь', 'Ирина', 'Константин', 'Ксения', 'Максим', 'Мария', 'Михаил', 'Наталья', 'Никита', 'Ольга', 'Петр', 'Роман', 'Светлана', 'Сергей', 'Татьяна']
russian_surnames = ['Иванов', 'Смирнов', 'Кузнецов', 'Соколов', 'Попов', 'Лебедев', 'Козлов', 'Новиков', 'Морозов', 'Петров', 'Волков', 'Соловьев', 'Васильев', 'Зайцев', 'Павлов', 'Семенов', 'Голубев', 'Виноградов', 'Богданов', 'Воробьев', 'Федоров', 'Михайлов', 'Беляев', 'Тарасов']
russian_patronymics = ['Александрович', 'Андреевич', 'Анатольевич', 'Борисович', 'Васильевич', 'Викторович', 'Владимирович', 'Геннадьевич', 'Григорьевич', 'Дмитриевич', 'Евгеньевич', 'Иванович', 'Игоревич', 'Константинович', 'Максимович', 'Михайлович', 'Николаевич', 'Олегович', 'Павлович', 'Петрович', 'Романович', 'Сергеевич', 'Степанович', 'Федорович']

# Списки предметов и оценок
subjects = ['Математика', 'Физика', 'Химия', 'Биология', 'Информатика', 'История', 'Литература', 'Английский язык']
grades = [2, 3, 4, 5]

def generate_name():
    name = f"{random.choice(russian_names)} {random.choice(russian_surnames)} {random.choice(russian_patronymics)}"
    return name

def generate_birth_date():
    start_date = date(1990, 1, 1)
    end_date = date(2005, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    birth_date = start_date + timedelta(days=random_days)
    return birth_date.strftime('%Y-%m-%d')

def generate_exam_date():
    start_date = date(2024, 6, 1)
    end_date = date(2024, 6, 30)
    random_days = random.randint(0, (end_date - start_date).days)
    exam_date = start_date + timedelta(days=random_days)
    return exam_date.strftime('%Y-%m-%d')

def populate_database():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()

    # Очистка таблиц перед заполнением
    c.execute("DELETE FROM grades")
    c.execute("DELETE FROM students")

    # Генерация и сохранение данных студентов
    for _ in range(30):
        name = generate_name()
        birth_date = generate_birth_date()
        c.execute("INSERT INTO students (name, birth_date) VALUES (?, ?)", (name, birth_date))
        student_id = c.lastrowid

        num_subjects = random.randint(4, 7)
        for _ in range(num_subjects):
            subject = random.choice(subjects)
            exam_date = generate_exam_date()
            teacher = generate_name()
            grade = random.choice(grades)
            c.execute("INSERT INTO grades (student_id, subject, exam_date, teacher, grade) VALUES (?, ?, ?, ?, ?)",
                      (student_id, subject, exam_date, teacher, grade))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    populate_database()
    print("База данных успешно заполнена тестовыми данными.")