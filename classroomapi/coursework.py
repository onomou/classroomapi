from classroomapi.classroom_object import ClassroomObject
from classroomapi.submission import Submission

class CourseWork(ClassroomObject):
    def __init__(self, attributes, service, CourseWorkType = 'COURSE_WORK_TYPE_UNSPECIFIED'):
        self.service = service
        self.CourseWorkType = CourseWorkType
        super().__init__(attributes)
    
    def patch(self, body, mask):
        return CourseWork(self.service.courses().courseWork().patch(courseId=self.courseId, id=self.id, body=body, updateMask=mask).execute(), self.service)

    edit = patch

    def modify_assignees(self, body):
        '''
        body = {
            "assigneeMode": enum (AssigneeMode),
            "modifyIndividualStudentsOptions": {
                object (ModifyIndividualStudentsOptions)
            }
        }

        AssigneeMode:
            ASSIGNEE_MODE_UNSPECIFIED: No mode specified. This is never returned.
            ALL_STUDENTS: All students can see the item. This is the default state.
            INDIVIDUAL_STUDENTS: A subset of the students can see the item.
        
        ModifyIndividualStudentsOptions:
            {
                "addStudentIds": [
                    string
                ],
                "removeStudentIds": [
                    string
                ]
            }
        '''
        return CourseWork(self.service().courses().courseWork().modifyAssignees(courseId=self.courseId, courseWorkId=self.Id, body=body), self.service)

    edit_assignees = modify_assignees

    def get_submissions(self):
        return [Submission(x, self.service) for x in self.service().courses().courseWork().studentSubmissions().list(courseId=self.courseId, courseWorkId=self.id).execute()]

class Assignment(CourseWork):
    def __init__(self, attributes, service):
        self.service = service
        super().__init__(attributes, CourseWorkType='ASSIGNMENT')
        
class ShortAnswerQuestion(CourseWork):
    def __init__(self, attributes, service):
        self.service = service
        super().__init__(attributes, CourseWorkType='SHORT_ANSWER_QUESTION')
        
class MultipleChoiceQuestion(CourseWork):
    def __init__(self, attributes, service):
        self.service = service
        super().__init__(attributes, CourseWorkType='MULTIPLE_CHOICE_QUESTION')
        
    
