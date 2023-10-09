import time
from models.models import Room, Employee, Meeting, Project, MeetingSchedule
from typing import List
from algorithm.scheduler import late_acceptance_hill_climbing

def pretty_print_schedule(schedule: List[Meeting], rooms: List[Room]):
    print("Generated Meeting Schedule:")
    print("====================================")

    # First, get a unique list of rooms that have at least one scheduled meeting
    scheduled_rooms = list(set([meeting.room for meeting in schedule if meeting.room]))

    # Sort rooms by room_id for more organized output
    scheduled_rooms = sorted(scheduled_rooms, key=lambda r: r.room_id)

    for room in scheduled_rooms:
        meetings_in_room = [meeting for meeting in schedule if meeting.room == room]

        print(f"Room {room.room_id} (Capacity: {room.size}, Projector: {'Yes' if room.has_projector else 'No'}, Video Conference: {'Yes' if room.has_video_conference else 'No'}):")
        
        # Sort meetings based on start time
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
    Room(1, 4, True, True),       
    Room(2, 6, True, False),      
    Room(3, 4, False, True),      
    Room(4, 2, False, False),     
    Room(5, 10, True, True)       
]

employees = [Employee(i, []) for i in range(1, 16)]  

project1 = Project(1, [employees[i].employee_id for i in [0, 1, 2, 3, 4]])
project2 = Project(2, [employees[i].employee_id for i in [5, 6, 7, 8]])
project3 = Project(3, [employees[i].employee_id for i in [9, 10, 11]])
project4 = Project(4, [employees[i].employee_id for i in [12, 13, 14, 0]])
project5 = Project(5, [employees[i].employee_id for i in [1, 3, 5, 7, 9]])

for emp in [employees[i] for i in [0, 1, 2, 3, 4]]:
    emp.projects.append(project1.project_id)
for emp in [employees[i] for i in [5, 6, 7, 8]]:
    emp.projects.append(project2.project_id)
for emp in [employees[i] for i in [9, 10, 11]]:
    emp.projects.append(project3.project_id)
for emp in [employees[i] for i in [12, 13, 14, 0]]:
    emp.projects.append(project4.project_id)
for emp in [employees[i] for i in [1, 3, 5, 7, 9]]:
    emp.projects.append(project5.project_id)

meetings = [
    Meeting(1, project1, 30, True, False),
    Meeting(2, project2, 45, False, True),
    Meeting(3, project3, 60, False, True),
    Meeting(4, project4, 50, True, False),
    Meeting(5, project5, 40, True, True),
    Meeting(6, project1, 30, False, False),
    Meeting(7, project2, 45, True, True),
    Meeting(8, project3, 30, True, False),
    Meeting(9, project4, 30, False, True),
    Meeting(10, project5, 60, True, True)
]

meeting_schedule = MeetingSchedule()

meeting_schedule.schedule_meeting(meetings[0], rooms[0], 0)
meeting_schedule.schedule_meeting(meetings[1], rooms[1], 0)
meeting_schedule.schedule_meeting(meetings[2], rooms[2], 0)
meeting_schedule.schedule_meeting(meetings[3], rooms[3], 0)
meeting_schedule.schedule_meeting(meetings[4], rooms[4], 0)
meeting_schedule.schedule_meeting(meetings[5], rooms[0], 60)
meeting_schedule.schedule_meeting(meetings[6], rooms[1], 60)
meeting_schedule.schedule_meeting(meetings[7], rooms[2], 60)
meeting_schedule.schedule_meeting(meetings[8], rooms[3], 60)
meeting_schedule.schedule_meeting(meetings[9], rooms[4], 60)

start = time.time()
meeting_schedule.schedule, iterations, cost = late_acceptance_hill_climbing(meeting_schedule.schedule, 1000, 10000, rooms)
end = time.time()
print("The execution time is :",
      (end-start) * 10**3, "ms")

print(f"Iterations: {iterations} Cost: {cost}")
pretty_print_schedule(meeting_schedule.schedule,rooms)