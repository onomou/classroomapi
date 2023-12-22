from classroomapi.classroom_object import ClassroomObject
from classroomapi.coursework import CourseWork, Assignment, ShortAnswerQuestion, MultipleChoiceQuestion
from classroomapi.user import Student, Teacher
from classroomapi.topic import Topic
from classroomapi.material import CourseWorkMaterial

class Course(ClassroomObject):
    def __init__(self, attributes, service):
        self.service = service
        super().__init__(attributes)
    
    def discriminate_coursework(self, coursework):
        match coursework['CourseWorkType']:
            case 'ASSIGNMENT':
                return Assignment(coursework)
            case 'SHORT_ANSWER_QUESTION':
                return ShortAnswerQuestion(coursework)
            case 'MULTIPLE_CHOICE_QUESTION':
                return MultipleChoiceQuestion(coursework)
            case _ :
                return CourseWork(coursework)

    def patch(self, body, update_mask):
        return Course(self.service.courses().patch(courseId=self.id, body=body, updateMask=update_mask).execute(), self.service)

    edit = patch

    def get_coursework(self, assignment_id=None):
        if assignment_id is None:
            coursework = self.service.courses().courseWork().list(courseId=self.id, courseWorkStates=['PUBLISHED','DRAFT']).execute().get('courseWork',[])
            return [self.discriminate_coursework(x) for x in coursework]
        else:
            coursework = self.service.courses().courseWork().get(courseId=self.id, id=assignment_id).execute()
            return self.discriminate_coursework(coursework)

    def get_assignments(self):
        return [x for x in self.get_coursework() if isinstance(x, Assignment)]
    
    def get_assignment(self, assignment_id):
        coursework = self.get_coursework(assignment_id)
        return coursework if isinstance(coursework, Assignment) else None

    def get_shortanswerquestions(self):
        return [x for x in self.get_coursework() if isinstance(x, ShortAnswerQuestion)]
    
    def get_shortanswerquestion(self, assignment_id):
        coursework = self.get_coursework(assignment_id)
        return coursework if isinstance(coursework, ShortAnswerQuestion) else None

    def get_multiplechoicequestions(self):
        return [x for x in self.get_coursework() if isinstance(x, MultipleChoiceQuestion)]
    
    def get_multiplechoicequestion(self, assignment_id):
        coursework = self.get_coursework(assignment_id)
        return coursework if isinstance(coursework, MultipleChoiceQuestion) else None
    
    def create_coursework(self, body):
        '''
        body = COURSEWORK
            {
                "title": string, # required
                "workType":  # required
                    COURSE_WORK_TYPE_UNSPECIFIED	No work type specified. This is never returned.
                    ASSIGNMENT	An assignment.
                    SHORT_ANSWER_QUESTION	A short answer question.
                    MULTIPLE_CHOICE_QUESTION
                "description": string,
                "materials": [
                    {
                    object (Material)
                    }
                ],
                "state": enum (CourseWorkState),
                "dueDate": {
                    object (Date)
                },
                "dueTime": {
                    object (TimeOfDay)
                },
                "scheduledTime": string,
                "maxPoints": number,
                "assigneeMode": enum (AssigneeMode),
                "individualStudentsOptions": {
                    object (IndividualStudentsOptions)
                },
                "submissionModificationMode": enum (SubmissionModificationMode),
                "topicId": string,

                "multipleChoiceQuestion": { # only for multiple choice questions
                    object (MultipleChoiceQuestion)
                }
            }
        '''
        return CourseWork(self.service.courses().courseWork().create(courseId=self.id, body=body).execute(), self.service)

    def create_assignment(self, body):
        body['workType'] = 'ASSIGNMENT'
        return Assignment(self.create_material(body))

    def create_shortanswerquestion(self, body):
        body['workType'] = 'SHORT_ANSWER_QUESTION'
        return ShortAnswerQuestion(self.create_material(body))

    def create_multiplechoicequestion(self, body):
        body['workType'] = 'MULTIPLE_CHOICE_QUESTION'
        return MultipleChoiceQuestion(self.create_material(body))

    def get_students(self):
        return [Student(x, self.service) for x in self.service.courses().students().list(courseId=self.id).execute().get('students',[])]
    
    def get_student(self, user_id):
        return Student(self.service.courses().students().get(courseId=self.id, userId=user_id).execute(), self.service)

    def get_teachers(self):
        return [Teacher(x, self.service) for x in self.service.courses().teachers().list(courseId=self.id).execute().get('teachers',[])]
    
    def get_teacher(self, user_id):
        return Teacher(self.service.courses().teachers().get(courseId=self.id, userId=user_id).execute(), self.service)

    def get_users(self):
        return self.get_students() + self.get_teachers()
    
    # TODO: create() for both students and teachers

    # TODO: delete() for both students and teachers

    def get_topics(self):
        return [Topic(x, self.service) for x in self.service.courses().topics().list(courseId=self.id).execute().get('topics',[])]
    
    def get_topic(self, topic_id):
        return Topic(self.service.courses().topics().get(courseId=self.id, id=topic_id).execute(), self.service)
    
    def delete_topic(self, topic_id):
        return self.service().coureses().topics().delete(courseId=self.id, id=topic_id).execute()

    def patch_topic(self, topic_id, body, mask):
        return self.get_topic(topic_id).patch(body, mask)
        # return Topic(self.service.courses().topics().patch(courseId=self.id, id=topic_id, body=body, updateMask=mask).execute(), self.service)

    edit_topic = patch_topic

    def create_topic(self, body):
        '''
        body = {
            "courseId": "A String", # Identifier of the course. Read-only.
            "name": "A String", # The name of the topic, generated by the user. Leading and trailing whitespaces, if any, are trimmed. Also, multiple consecutive whitespaces are collapsed into one inside the name. The result must be a non-empty string. Topic names are case sensitive, and must be no longer than 100 characters.
            "topicId": "A String", # Unique identifier for the topic. Read-only.
            "updateTime": "A String", # The time the topic was last updated by the system. Read-only.
        }'''
        return Topic(self.service.courses().topics().create(courseId=self.id, body=body).execute(), self.service)

    '''
    Materials
    create(courseId, body=None)
    delete(courseId, id)
    get(courseId, id)
    patch(courseId, id, body=None, updateMask=None)
    '''
    def create_material(self, body):
        return CourseWorkMaterial(self.service.courses().courseWorkMaterials().create(courseId=self.id, body=body).execute(), self.service)
    
    def delete_material(self, material_id):
        return self.service.courses().courseWorkMaterials().delete(courseId=self.id, id=material_id).execute()
    
    def get_material(self, material_id):
        return CourseWorkMaterial(self.service.courses().courseWorkMaterials().get(courseId=self.id, id=material_id).execute(), self.service)
    
    def get_materials(self, states=None, drive_id=None, link=None, order_by=None):
        '''
        state = [
            COURSEWORK_MATERIAL_STATE_UNSPECIFIED
            PUBLISHED
            DRAFT
            DELETED
        ]
        drive_id = ID matches the provided string
        link = URL partially matches the provided string
        If both drive_id and link are provided, material must match both filters
        orderBy = 'updateTime asc' or 'updateTime desc'
        '''
        return [CourseWorkMaterial(x, self.service) for x in self.service.courses().courseWorkMaterials().list(courseId=self.id, courseWorkMaterialStates=states,materialDriveId=drive_id,materialLink=link,orderBy=order_by).execute().get('materials',[])]

    def patch_material(self, material_id, body, update_mask):
        '''
        body = object(CourseWorkMaterial)
        update_mask = comma-separated string of fields from these:
            title
            description
            state
            scheduledTime
            topicId
        '''
        return self.get_material(material_id).patch(body, update_mask)
        # return CourseWorkMaterial(self.service.courses().courseWorkMaterials().patch(courseId=self.id, id=material_id, body=body, updateMask=update_mask).execute(), self.service)
    
    edit_material = patch_material