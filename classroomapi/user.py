from classroomapi.classroom_object import ClassroomObject

class User(ClassroomObject):
    def __init__(self, attributes, service):
        self.service = service
        super().__init__(attributes)
        
class Student(User):
    def __init__(self, attributes, service):
        self.user_type = 'Student'
        super().__init__(attributes, service)

class Teacher(User):
    def __init__(self, attributes, service):
        self.user_type = 'Teacher'
        super().__init__(attributes, service)