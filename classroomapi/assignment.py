from classroomapi.classroom_object import ClassroomObject
from classroomapi.submission import Submission

class Assignment(ClassroomObject):
    def __init__(self, attributes, service):
        self.service = service
        super().__init__(attributes)
        
    def edit(self, body, mask):
        return self.service.courses().courseWork().patch(courseId=self.courseId, id=self.id, body=body, updateMask=mask).execute()

    def get_submissions(self):
        return [Submission(x, self.service) for x in self.service().courses().courseWork().studentSubmissions().list(courseId=self.courseId, courseWorkId=self.id).execute()]

    
