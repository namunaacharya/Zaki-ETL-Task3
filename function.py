from datetime import date
from abc import abstractmethod, ABC

class Enrollment(ABC):
    student_count = 0

    def __init__(self, st_name:str, course_name:str, enroll_date, status='enrolled'):
        self.st_name = st_name
        self.course_name = course_name
        self.enroll_date = enroll_date
        self.status = status
        self.topics = {'Python', 'SQL', 'Pyspark'}
        self.level = ['Basic', 'Intermediate', 'Advanced']
        self.grade = {'Basic': 70, 'Intermediate': 80}
        self.is_active = False
        Enrollment.student_count += 1

    @abstractmethod
    def enroll_type(self):
        pass

    def student(self):
        return(f'{self.st_name} has enrolled in {self.course_name} on {self.enroll_date}')

    def course_stat(self):
        current_date = date.today().strftime('%Y-%m-%d')
        if self.enroll_date >= '2025-04-01'  and self.enroll_date <= current_date:
            self.is_active = True
        elif self.enroll_date < '2025-04-01':
            self.status = 'Completed'   
        else: 
            self.status = 'Invalid'
            raise ValueError('Invalid date')
            
    def st_status(self):
        if self.is_active:
            print(f"{self.st_name} is currently studying.")
        else:
            print(f"{self.st_name} has completed the course.")

    def new_topic(self, *topic):
        self.topics.add(topic)
        print(f'Updated topics: {self.topics}')

    def check_level(self, new_level):
        if new_level in self.level: 
            print(f"{new_level} level is available.")
        else:
            print(f"{new_level} level isn't available.")

    def add_grade(self, level:str, score:int):
        self.grade[level] = score
        print(f"Grades: {self.grade}")

def average_grade(student):
    average = sum(student.grade.values()) / len(student.grade)
    return average

# new = Enrollment('Namuna','Data Science','2025-01-30')
# new.student()
# new.course_stat()
# new.st_status()
# new.new_topic('Power BI','Excel')
# new.check_level('Beginner')
# new.add_grade('Advanced', 80)
# avg_grade = round(average_grade(new),2)
# print(f"Average grade of {new.st_name} is {avg_grade}")

# new1 = Enrollment('Namm','Data Science','2025-01-30')
# print(Enrollment.student_count)

class OnlineEnrollment(Enrollment):
    online_students = 0

    def __init__(self, st_name, course_name, enroll_date, platform, status='enrolled',):
        super().__init__(st_name, course_name, enroll_date, status)
        self.platform = platform
        OnlineEnrollment.online_students += 1

    def enroll_type(self):
        parent = super().student()
        print(f"{parent} through {self.platform}")

class PhysicalEnrollment(Enrollment):
    physical_students = 0

    def __init__(self, st_name, course_name, enroll_date, branch, status='enrolled',):
        super().__init__(st_name, course_name, enroll_date, status)
        self.branch = branch
        PhysicalEnrollment.physical_students += 1

    def enroll_type(self):
        parent = super().student()
        print(f"{parent} from {self.branch} branch.")

enroll_data = OnlineEnrollment('Namm','Data Science','2025-01-30','LinkedIn')
enroll_data1 = PhysicalEnrollment('Namuna','Data Science','2025-01-30','Kalanki')
enroll_data.enroll_type()
enroll_data1.enroll_type()
print(f"Total students : {Enrollment.student_count}")
print(f"Online students: {OnlineEnrollment.online_students}")
print(f"Physical students: {PhysicalEnrollment.physical_students}")




