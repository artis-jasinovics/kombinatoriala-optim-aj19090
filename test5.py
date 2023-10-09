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
    Room(1, 3, True, True), 
    Room(2, 5, True, False),  
    Room(3, 6, False, True),  
    Room(4, 4, False, False)  
]

employees = [Employee(i, []) for i in range(1, 16)]  

project1 = Project(1, [employees[i].employee_id for i in range(0, 5)])     
project2 = Project(2, [employees[i].employee_id for i in range(5, 10)])  
project3 = Project(3, [employees[i].employee_id for i in range(10, 15)])   
project4 = Project(4, [employees[i].employee_id for i in range(0, 10)])    

for i in range(0, 5):
    employees[i].projects.append(project1.project_id)
for i in range(5, 10):
    employees[i].projects.append(project2.project_id)
for i in range(10, 15):
    employees[i].projects.append(project3.project_id)
for i in range(0, 10):
    employees[i].projects.append(project4.project_id)

meetings = [
    Meeting(1, project1, 30, True, True),   
    Meeting(2, project2, 30, True, False),  
    Meeting(3, project3, 30, False, True),  
    Meeting(4, project4, 45, True, True),    
    Meeting(5, project1, 30, True, True),   
    Meeting(6, project4, 45, True, True)     
]

meeting_schedule = MeetingSchedule()

meeting_schedule.schedule_meeting(meetings[0], rooms[0], 0)
meeting_schedule.schedule_meeting(meetings[1], rooms[1], 0)
meeting_schedule.schedule_meeting(meetings[2], rooms[2], 0)
meeting_schedule.schedule_meeting(meetings[3], rooms[3], 0)
meeting_schedule.schedule_meeting(meetings[4], rooms[0], 30)   
meeting_schedule.schedule_meeting(meetings[5], rooms[3], 45)   


start = time.time()
meeting_schedule.schedule, iterations, cost = late_acceptance_hill_climbing(meeting_schedule.schedule, 1000, 1000, rooms)
end = time.time()
print("The execution time is :",
      (end-start) * 10**3, "ms")

print(f"Iterations: {iterations} Cost: {cost}")
pretty_print_schedule(meeting_schedule.schedule,rooms)