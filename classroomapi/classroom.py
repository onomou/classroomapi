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
        return [Course(x, self.service) for x in self.service.courses().list(courseStates='ACTIVE').execute()['courses']]
    
    def get_course(self, course_id):
        return Course(self.service.courses().get(id=course_id).execute(), self.service)

    def create_course(self, body):
        '''
        { # A Course in Classroom.
                { # A set of materials that appears on the "About" page of the course. These materials might include a syllabus, schedule, or other background information relating to the course as a whole.
                "materials": [ # Materials attached to this set.
                    { # A material attached to a course as part of a material set.
                    "driveFile": { # Representation of a Google Drive file. # Google Drive file attachment.
                        "id": "A String", # Drive API resource ID.
                    },
                    "form": { # Google Forms item. # Google Forms attachment.
                        "formUrl": "A String", # URL of the form.
                    },
                    "link": { # URL item. # Link atatchment.
                        "url": "A String", # URL to link to. This must be a valid UTF-8 string containing between 1 and 2024 characters.
                    },
                    "youTubeVideo": { # YouTube video item. # Youtube video attachment.
                        "id": "A String", # YouTube API resource ID.
                    },
                    },
                ],
                "title": "A String", # Title for this set.
                },
            ],
            "courseState": "A String", # State of the course. If unspecified, the default state is `PROVISIONED`.
            "description": "A String", # Optional description. For example, "We'll be learning about the structure of living creatures from a combination of textbooks, guest lectures, and lab work. Expect to be excited!" If set, this field must be a valid UTF-8 string and no longer than 30,000 characters.
            "descriptionHeading": "A String", # Optional heading for the description. For example, "Welcome to 10th Grade Biology." If set, this field must be a valid UTF-8 string and no longer than 3600 characters.
            "id": "A String", # Identifier for this course assigned by Classroom. When creating a course, you may optionally set this identifier to an alias string in the request to create a corresponding alias. The `id` is still assigned by Classroom and cannot be updated after the course is created. Specifying this field in a course update mask results in an error.
            "name": "A String", # Name of the course. For example, "10th Grade Biology". The name is required. It must be between 1 and 750 characters and a valid UTF-8 string.
            "room": "A String", # Optional room location. For example, "301". If set, this field must be a valid UTF-8 string and no longer than 650 characters.
            "section": "A String", # Section of the course. For example, "Period 2". If set, this field must be a valid UTF-8 string and no longer than 2800 characters.
                "id": "A String", # Drive API resource ID.
            },
            }
        '''
        return Course(self.service.courses().create(body=body).execute(), self.service)
    
    def edit_course(self, course_id, body, update_mask):
        return Course(self.service.courses().patch(courseId=course_id, body=body, updateMask=update_mask).execute(), self.service)

    # TODO: update_course, but this might be too powerful