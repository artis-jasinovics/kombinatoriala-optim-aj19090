import time
from models.models import Room, Employee, Meeting, Project, MeetingSchedule
from typing import List
from algorithm.scheduler import late_acceptance_hill_climbing

def pretty_print_schedule(schedule: List[Meeting], rooms: List[Room]):
    print("Generated Meeting Schedule:")
    print("====================================")

    scheduled_rooms = list(set([meeting.room for meeting in schedule if meeting.room]))

    scheduled_rooms = sorted(scheduled_rooms, key=lambda r: r.room_id)

    for room in scheduled_rooms:
        meetings_in_room = [meeting for meeting in schedule if meeting.room == room]

        print(f"Room {room.room_id} (Capacity: {room.size}, Projector: {'Yes' if room.has_projector else 'No'}, Video Conference: {'Yes' if room.has_video_conference else 'No'}):")
        
        for meeting in sorted(meetings_in_room, key=lambda x: x.start_time):
            start_time = meeting.start_time
            print(
                f"\tMeeting {meeting.meeting_id} for Project {meeting.project.project_id} starts at {start_time} (Duration: {meeting.duration} mins)")
            print(
                f"\t\tNeeds Projector: {'Yes' if meeting.needs_projector else 'No'}, Needs Video Conference: {'Yes' if meeting.needs_video_conference else 'No'}")
            print(
                f"\t\tParticipants ({len(meeting.project.employees)}): {', '.join(str(e) for e in meeting.project.employees)}")
        print("====================================")

rooms = [
    Room(1, 2, True, False),  
    Room(2, 2, False, False)  
]

employees = [Employee(i, []) for i in range(1, 6)] 

project1 = Project(1, [employees[i].employee_id for i in [0, 1, 2]]) 
project2 = Project(2, [employees[i].employee_id for i in [2, 3, 4]])  

for emp in [employees[i] for i in [0, 1, 2]]:
    emp.projects.append(project1.project_id)
for emp in [employees[i] for i in [2, 3, 4]]:
    emp.projects.append(project2.project_id)

meetings = [
    Meeting(1, project1, 30, True, True),  
    Meeting(2, project2, 30, True, True)   
]

meeting_schedule = MeetingSchedule()

meeting_schedule.schedule_meeting(meetings[0], rooms[0], 0)
meeting_schedule.schedule_meeting(meetings[1], rooms[1], 15)  


start = time.time()
meeting_schedule.schedule, iterations, cost = late_acceptance_hill_climbing(meeting_schedule.schedule, 1000, 10000, rooms)
end = time.time()
print("The execution time is :",
      (end-start) * 10**3, "ms")

print(f"Iterations: {iterations} Cost: {cost}")
pretty_print_schedule(meeting_schedule.schedule,rooms)