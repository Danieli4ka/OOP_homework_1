# класс студентов
class Student:
    all_students = []

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    #оценка лектора
    def rate_lecturer(self, lecturer, course, grade):
        if (
                isinstance(lecturer, Lecturer)
                and (course in self.courses_in_progress or course in self.finished_courses)
                and course in lecturer.courses_attached
        ):
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
        else:
            raise ValueError(f'Ошибка оценки, студент {self.name} или учитель {lecturer.name} не относятся к курсу '
                         f'{course}')

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return calculate_average(self) < calculate_average(other)

    def __str__(self):
        return (f'Имя: {self.name} '
                f'\nФамилия: {self.surname} '
                f'\nСредняя оценка за домашние задания: {calculate_average(self):.2f}'
                f'\nКурсы в процессе изучения: {', '.join(self.courses_in_progress)}'
                f'\nЗавершенные курсы: {', '.join(self.finished_courses)}')


# класс учителей
class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


# класс лекторы
class Lecturer (Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return calculate_average(self) < calculate_average(other)

    def __str__(self):
        return (f'Имя: {self.name} '
                f'\nФамилия: {self.surname} '
                f'\nСредняя оценка за лекции: {calculate_average(self):.2f}')


# класс эксперты, проверяющие задания
class Reviewer (Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if (
                isinstance(student, Student)
                and course in self.courses_attached
                and (course in student.courses_in_progress or course in student.finished_courses)
        ):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            raise ValueError(f'Ошибка оценки, эксперт {self.name} или студент {student.name} '
                                    f'не относятся к курсу {course}')

    def __str__(self):
        return f'Имя: {self.name} \nФамилия: {self.surname}'

#вычисление средней по одному студенту
def calculate_average(entity):
    total_grades = [grade for grades in entity.grades.values() for grade in grades]
    return sum(total_grades) / len(total_grades) if total_grades else 0


#средняя студентов по одному курсу
def average_homework_grade(students, course):
    if not students:
        print('Список студентов пуст.')
        return 0
    total_grades = []
    for student in students:
        if course in student.grades:
            total_grades.extend(student.grades[course])
    if total_grades:
        return sum(total_grades) / len(total_grades)
    else:
        print(f'Нет оценок для курса "{course}".')
        return 0


#средняя лекторов по одному курсу
def average_lecture_grade(lecturers, course):
    if not lecturers:
        print('Список лекторов пуст.')
        return 0
    total_grades = []
    for lecturer in lecturers:
        if course in lecturer.grades:
            total_grades.extend(lecturer.grades[course])
    if total_grades:
        return sum(total_grades) / len(total_grades)
    else:
        print(f'Нет оценок для курса "{course}".')
        return 0

lecturer_1 = Lecturer('Oleg', 'Babukin')
lecturer_1.courses_attached.append('Python')
lecturer_1.courses_attached.append('SQL')

lecturer_2 = Lecturer('Alena', 'Batickaya')
lecturer_2.courses_attached.append('Git')
lecturer_2.courses_attached.append('Java')

student_1 = Student('Valya', 'Bakhovkina', 'F')
student_1.courses_in_progress.append('Python')
student_1.finished_courses.append('Git')
student_1.finished_courses.append('SQL')

student_2 = Student('Aleksander', 'Smirnov', 'M')
student_2.courses_in_progress.append('Java')
student_2.courses_in_progress.append('Git')
student_2.finished_courses.append('Python')

reviewer_1 = Reviewer('Larisa', 'Ivanova')
reviewer_1.courses_attached.append('Python')
reviewer_1.courses_attached.append('Git')

reviewer_2 = Reviewer('Kate', 'Klim')
reviewer_2.courses_attached.append('Java')
reviewer_2.courses_attached.append('SQL')

student_1.rate_lecturer(lecturer_1, 'Python', 8)
student_1.rate_lecturer(lecturer_2, 'Git', 7)
#проверяем, что студент не может поставить оценку не своему курсу или не тому лектору :
#student_1.rate_lecturer(lecturer_1, 'Java', 10)
student_1.rate_lecturer(lecturer_1, 'SQL', 8)

student_2.rate_lecturer(lecturer_1, 'Python', 9)
student_2.rate_lecturer(lecturer_2, 'Git', 4)
student_2.rate_lecturer(lecturer_2, 'Java', 10)

reviewer_1.rate_hw(student_1, 'Python', 9)
reviewer_1.rate_hw(student_2, 'Git', 7)

reviewer_2.rate_hw(student_2, 'Java', 6)
reviewer_2.rate_hw(student_1, 'SQL', 5)
#проверяем, что эксперт не может поставить оценку не своему курсу или не тому студенту:
#reviewer_2.rate_hw(student_2, 'SQL', 5)

print()
print(student_1)
print()
print(student_2)
print()
print(lecturer_1)
print()
print(lecturer_2)
print()
print(reviewer_1)
print()
print(reviewer_2)
print()

if student_1 > student_2:
    print(f'{student_1.name} {student_1.surname} имеет средний балл выше, чем {student_2.name} {student_2.surname}')
elif student_1 < student_2:
    print(f'{student_2.name} {student_2.surname} имеет средний балл выше, чем {student_1.name} {student_1.surname}')
else:
    print(f'{student_1.name} {student_1.surname} и {student_2.name} {student_2.surname} '
          f'имеют равный средний балл')

print()

if lecturer_1 > lecturer_2:
    print(f'{lecturer_1.name} {lecturer_1.surname} имеет среднюю оценку за лекции выше, чем'
          f' {lecturer_2.name} {lecturer_2.surname}')
elif lecturer_1 < lecturer_2:
    print(f'{lecturer_2.name} {lecturer_2.surname} имеет среднюю оценку за лекции выше, чем'
          f'{lecturer_1.name} {lecturer_1.surname}')
else:
    print(f'{lecturer_1.name} {lecturer_1.surname} и {lecturer_2.name} {lecturer_2.surname} '
          f'имеют одинаковую среднюю оценку за лекции')


students = [student_1, student_2]
course_name_s = 'Java'
average_grade_python = average_homework_grade(students, course_name_s)
print(f'Средняя оценка студентов за курс {course_name_s}: {average_grade_python}')

lecturers = [lecturer_1, lecturer_2]
course_name_l = 'Python'
average_lecture_python = average_lecture_grade(lecturers, course_name_l)
print(f'Средняя оценка лекторов за курс {course_name_l}: {average_grade_python}')