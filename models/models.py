from typing import List, Tuple, Optional

class Room:
    def __init__(self, room_id: int, size: int, has_projector: bool, has_video_conference: bool):
        self.room_id = room_id
        self.size = size
        self.has_projector = has_projector
        self.has_video_conference = has_video_conference

    def is_suitable(self, num_people: int, needs_projector: bool, needs_video_conference: bool) -> bool:
        return (self.size >= num_people and
                (not needs_projector or (needs_projector and self.has_projector)) and
                (not needs_video_conference or (needs_video_conference and self.has_video_conference)))
        
class Employee:
    def __init__(self, employee_id: int, projects: List[int]):
        self.employee_id = employee_id
        self.projects = projects

class Project:
    def __init__(self, project_id: int, employees: List[int]):
        self.project_id = project_id
        self.employees = employees
    
    def assign_employee(self, employee_id):
        self.employees.append(employee_id)

class Meeting:
    def __init__(self, meeting_id: int, project: Project, duration: int, needs_projector: bool, needs_video_conference: bool):
        self.meeting_id = meeting_id
        self.project = project
        self.room = None
        self.start_time = None
        self.duration = duration
        self.needs_projector = needs_projector
        self.needs_video_conference = needs_video_conference
        
    def assign_room(self, room: Room, start_time: int):
        self.room = room
        self.start_time = start_time
    
class MeetingSchedule:
    def __init__(self):

        self.schedule = []

    def schedule_meeting(self, meeting: Meeting, room: Room, start_time: int) -> bool:
        meeting.assign_room(room, start_time)
        self.schedule.append(meeting)
        return True
