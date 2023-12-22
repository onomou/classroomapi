from classroomapi.classroom_object import ClassroomObject

class CourseWorkMaterial(ClassroomObject):
    def __init__(self, attributes, service):
        self.service = service
        super().__init__(attributes)
    
    def patch(self, body, update_mask):
        '''
        body = object(CourseWorkMaterial)
        updateMask = comma-separated string of fields from these:
            title
            description
            state
            scheduledTime
            topicId
        '''
        return CourseWorkMaterial(self.service.courses().courseWorkMaterials().patch(courseId=self.courseId, id=self.id, body=body, updateMask=update_mask).execute(), self.service)
    
    edit = patch