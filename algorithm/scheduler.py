class MeetingScheduler:
    
    def __init__(self, rooms, employees, projects, meetings):
        self.rooms = sorted(rooms, key=lambda r: r.capacity, reverse=True)
        self.employees = employees
        self.projects = projects
        self.meetings = sorted(meetings, key=lambda m: (m.duration, m.needsProjector + m.needsVideoConference), reverse=True)
        self.schedule = []

    def can_schedule(self, meeting, room, start_time):
        #Parbaudam visu ko vien varam pirms rezerve
        if room.capacity < len(meeting.participants):
            return False
        if meeting.needsProjector and not room.hasProjector:
            return False
        if meeting.needsVideoConference and not room.hasVideoConference:
            return False

        # Check employee availability
        for employee in meeting.participants:
            if any(scheduled_meeting.startTime <= start_time < (scheduled_meeting.startTime + scheduled_meeting.duration) for scheduled_meeting in self.schedule if employee in scheduled_meeting.participants):
                return False

        return True

    def schedule_meeting(self, meeting):
        for room in self.rooms:
            for start_time in range(9, 18): # 9:00 lidz 18:00 pienemam ka darbadienu, iespejams, float?
                if self.can_schedule(meeting, room, start_time):
                    meeting.room = room
                    meeting.startTime = start_time
                    self.schedule.append(meeting)
                    return True
        return False

    def run(self):
        for meeting in self.meetings:
            if not self.schedule_meeting(meeting):
                #Te tie kartupeli un gala (algoritms) ko vajadzes izdomat
                print(f"Meeting {meeting.meetingID} could not be scheduled.")

        return self.schedule