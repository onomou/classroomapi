from classroomapi.classroom_object import ClassroomObject

class Material(ClassroomObject):
    def __init__(self, attributes, service):
        self.service = service
        super().__init__(attributes)
      