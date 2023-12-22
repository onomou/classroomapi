from classroomapi.classroom_object import ClassroomObject

class Topic(ClassroomObject):
    def __init__(self, attributes, service):
        self.service = service
        super().__init__(attributes)
    
    def patch(self, body, mask):
        return Topic(self.service.courses().topics().patch(courseId=self.courseId, id=self.topicId, body=body, updateMask=mask).execute(), self.service)

    edit = patch