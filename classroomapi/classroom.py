import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from classroomapi.course import Course

class Classroom:
    def __init__(self, token_file):
        SCOPES = [
                "https://www.googleapis.com/auth/classroom.coursework.students",
                "https://www.googleapis.com/auth/classroom.coursework.me",
                "https://www.googleapis.com/auth/classroom.rosters",
                "https://www.googleapis.com/auth/classroom.topics",
                "https://www.googleapis.com/auth/classroom.courses",
                "https://www.googleapis.com/auth/classroom.announcements",
            ]#["https://www.googleapis.com/auth/classroom.courses.readonly"]

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                        "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        try:
            service = build("classroom", "v1", credentials=creds)
        except HttpError as error:
            service = None
            raise(ValueError(f"An error occurred: {error}"))
        self.service = service
    
    def get_courses(self):
        return [Course(x, self.service) for x in self.service.courses().list(courseStates='ACTIVE').execute().get('courses',[])]
    
    def get_course(self, course_id):
        return Course(self.service.courses().get(id=course_id).execute(), self.service)

    def create_course(self, body):
        '''
        body = {
            "id": string,
            "name": string, # required
            "section": string,
            "descriptionHeading": string,
            "description": string,
            "room": string,
            "ownerId": string, # required for creation, set to 'me'
            "courseState": enum (CourseState),
        }
        '''
        return Course(self.service.courses().create(body=body).execute(), self.service)

    def patch_course(self, course_id, body, update_mask):
        '''
            update_mask = comma-separated string of fields from these:
                name
                section
                descriptionHeading
                description
                room
                courseState
                ownerId
        '''
        return self.get_course(course_id).patch(body, update_mask)
        # return Course(self.service.courses().patch(courseId=course_id, body=body, updateMask=update_mask).execute(), self.service)

    edit_course = patch_course

    # TODO: update_course, but this might be too powerful