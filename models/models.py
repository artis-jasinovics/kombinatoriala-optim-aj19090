from typing import List, Tuple, Optional

class Room:
    def __init__(self, room_id: int, capacity: int, has_projector: bool, has_video_conference: bool):
        self.room_id = room_id
        self.capacity = capacity
        self.has_projector = has_projector
        self.has_video_conference = has_video_conference

    def is_suitable(self, num_people: int, needs_projector: bool, needs_video_conference: bool) -> bool:
        return (self.capacity >= num_people and
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
        self.room_id = None
        self.start_time = None
        self.duration = duration
        self.needs_projector = needs_projector
        self.needs_video_conference = needs_video_conference
        
    def assign_room(self, room_id: int, start_time: int):
        self.room_id = room_id
        self.start_time = start_time

class MeetingSchedule:
    def __init__(self):
        
        self.schedule = {}  # format: {meeting_id: (room_id, start_time)}
    
    def schedule_meeting(self, meeting: Meeting, room: Room, start_time: int) -> bool:
        """
        Try to schedule a meeting in the given room at the given start time.
        
        Returns True if the meeting was successfully scheduled, False otherwise.
        """
        # Check if the room is available and suitable
        if not room.is_suitable(len(meeting.project.employees), meeting.needs_projector, meeting.needs_video_conference):
            return False
        
        for m_id, (r_id, s_time) in self.schedule.items():
            if r_id == room.room_id and (start_time < s_time + meeting.duration and start_time + meeting.duration > s_time):
                # Time slot overlap for the same room
                return False
        
        self.schedule[meeting.meeting_id] = (room.room_id, start_time)
        return True

    def get_meetings_for_room(self, room_id: int) -> List[int]:
        return [m_id for m_id, (r_id, _) in self.schedule.items() if r_id == room_id]

    def get_meeting_details(self, meeting_id: int) -> Optional[Tuple[int, int]]:
        return self.schedule.get(meeting_id, None)

    def is_meeting_scheduled(self, meeting_id: int) -> bool:
        return meeting_id in self.schedule

    def remove_meeting(self, meeting_id: int) -> None:
        if meeting_id in self.schedule:
            del self.schedule[meeting_id]

    def clear_schedule(self) -> None:
        self.schedule.clear()