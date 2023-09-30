class Room:
    def __init__(self, roomID, capacity, hasProjector, hasVideoConference):
        self.roomID = roomID
        self.capacity = capacity
        self.hasProjector = hasProjector
        self.hasVideoConference = hasVideoConference

class Employee:
    def __init__(self, employeeID):
        self.employeeID = employeeID
        self.projectIDs = []

class Project:
    def __init__(self, projectID):
        self.projectID = projectID
        self.employeeIDs = []

class Meeting:
    def __init__(self, meetingID, projectID, duration, needsProjector, needsVideoConference):
        self.meetingID = meetingID
        self.projectID = projectID
        self.roomID = None
        self.startTime = None
        self.duration = duration
        self.needsProjector = needsProjector
        self.needsVideoConference = needsVideoConference