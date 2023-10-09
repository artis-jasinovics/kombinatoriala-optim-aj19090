import random

def late_acceptance_hill_climbing(initial_schedule, L, max_iterations, rooms):
    #Initialize
    current_schedule = initial_schedule
    current_cost = cost_function(current_schedule)
    
    #Create a list with L entries of the initial solution cost
    cost_list = [current_cost] * L
    best_schedule = current_schedule
    best_cost = current_cost

    #Iterate for a maximum number of steps
    for i in range(max_iterations):
        #Create a neighboring solution
        neighbor_schedule = generate_neighbor(current_schedule,rooms)
        neighbor_cost = cost_function(neighbor_schedule)
        
        #Compare the neighborcost with the cost L steps back
        if neighbor_cost <= cost_list[i % L]:
            current_schedule = neighbor_schedule
            current_cost = neighbor_cost

        #Check if the current solution is the best so far
        if current_cost < best_cost:
            best_cost = current_cost
            best_schedule = current_schedule

        cost_list[i % L] = current_cost
        
        #If a good solution is found then leave early
        if neighbor_cost == 0:
            return neighbor_schedule, i, 0


    #Return the best solution found
    return best_schedule, i, best_cost

def generate_neighbor(schedule, rooms):
    new_schedule = schedule.copy()

    # Detect problematic meetings
    conflict_count = {
        "meeting_room": calculate_meeting_room_conflicts(new_schedule, "CALC"), #Returns conflict count
        "meeting_employee": calculate_meeting_employee_conflicts(new_schedule, "CALC"),
        "room_capacity": calculate_room_overcapacity(new_schedule, "CALC"),
        "equipment": calculate_equipment_mismatch(new_schedule, "CALC")
    }
    
    conflicting_meetings = {
        "meeting_room": calculate_meeting_room_conflicts(new_schedule, "GET"), #Returns tuple (meeting1, meeting2)
        "meeting_employee": calculate_meeting_employee_conflicts(new_schedule, "GET"), #Returns tuple (meeting1, meeting2)
        "room_capacity": calculate_room_overcapacity(new_schedule, "GET"), #Returns meeting
        "equipment": calculate_equipment_mismatch(new_schedule, "GET") #Returns meeting
    }

    # Choose a conflict type based on the conflict which appears the most
    chosen_conflict = max(conflict_count, key=conflict_count.get)

    problematic_meeting = conflicting_meetings[chosen_conflict]

    if chosen_conflict == "meeting_room":
        action = random.choice(["shift_time", "swap_rooms"])
        
        if action == "shift_time":
            #Set time to the end of the meeting with the latest end time, otherwise add 10 minutes
            if (problematic_meeting[0].start_time + problematic_meeting[0].duration) < (problematic_meeting[1].start_time + problematic_meeting[1].duration):
                problematic_meeting[0].start_time = problematic_meeting[1].start_time + problematic_meeting[1].duration
            elif (problematic_meeting[1].start_time + problematic_meeting[1].duration) < (problematic_meeting[0].start_time + problematic_meeting[0].duration):
                problematic_meeting[1].start_time = problematic_meeting[0].start_time + problematic_meeting[0].duration
            else:
                problematic_meeting[0].start_time += 30
        else:  # swap_rooms
            new_room = choose_new_room_for_meeting(problematic_meeting[0], rooms, new_schedule)  # This function intelligently selects a room for the meeting
            problematic_meeting[0].room = new_room

    elif chosen_conflict == "meeting_employee":
        #Set time to the end of the meeting with the latest end time, otherwise add 10 minutes
        if (problematic_meeting[0].start_time + problematic_meeting[0].duration) > (problematic_meeting[1].start_time + problematic_meeting[1].duration):
            problematic_meeting[0].start_time = problematic_meeting[1].start_time + problematic_meeting[1].duration
        elif (problematic_meeting[1].start_time + problematic_meeting[1].duration) > (problematic_meeting[0].start_time + problematic_meeting[0].duration):
            problematic_meeting[1].start_time = problematic_meeting[0].start_time + problematic_meeting[0].duration
        else:
            problematic_meeting[0].start_time += 30

    elif chosen_conflict == "room_capacity" or chosen_conflict == "equipment":
        new_room = choose_new_room_for_meeting(problematic_meeting, rooms, new_schedule)
        problematic_meeting.room = new_room

    return new_schedule


def cost_function(schedule):
        meeting_room_conflicts = calculate_meeting_room_conflicts(schedule, "CALC")
        meeting_employee_conflicts = calculate_meeting_employee_conflicts(schedule, "CALC")
        room_overcapacity = calculate_room_overcapacity(schedule, "CALC")
        equipment_mismatch = calculate_equipment_mismatch(schedule, "CALC")

        alpha, beta, gamma, delta = 8, 2, 2, 8

        total_cost = (alpha * meeting_room_conflicts +
                  beta * meeting_employee_conflicts +
                  gamma * room_overcapacity +
                  delta * equipment_mismatch)

        return total_cost


def calculate_meeting_room_conflicts(schedule, method):

    conflicts = 0
    for meeting1 in schedule:
        for meeting2 in schedule:
            if meeting1 != meeting2 and meeting1.room == meeting2.room and meetings_overlap(meeting1, meeting2):
                if method == "GET":
                    return (meeting1,meeting2)
                conflicts += 1
    return conflicts
    

def calculate_meeting_employee_conflicts(schedule, method):
    conflicts = 0
    for meeting1 in schedule:
        for meeting2 in schedule:
            if meeting1 != meeting2 and meetings_overlap(meeting1, meeting2):
                shared_employees = set(meeting1.project.employees).intersection(set(meeting2.project.employees))
                if method == "GET" and len(shared_employees) > 0:
                    return (meeting1, meeting2)
                conflicts += len(shared_employees)
    return conflicts

def calculate_room_overcapacity(schedule, method): #Too many people in one room
    overcapacity = 0
    for meeting in schedule:
        room = meeting.room 
        if len(meeting.project.employees) > room.size:
            if method == "GET" and len(meeting.project.employees) - room.size > 0:
                return meeting
            overcapacity += len(meeting.project.employees) - room.size
    return overcapacity

def calculate_equipment_mismatch(schedule, method):
    mismatches = 0
    for meeting in schedule:
        room = meeting.room
        if meeting.needs_projector and not room.has_projector:
            mismatches += 1
        if meeting.needs_video_conference and not room.has_video_conference:
            mismatches += 1
        if method == "GET" and mismatches > 0:
            return meeting
    return mismatches

def meetings_overlap(meeting1, meeting2):
    if meeting1.start_time >= meeting2.start_time + meeting2.duration:
        return False
    if meeting2.start_time >= meeting1.start_time + meeting1.duration:
        return False
    return True

def choose_new_room_for_meeting(meeting, rooms, schedule):
    # Filter rooms based on meeting requirements
    suitable_rooms = [room for room in rooms if room.is_suitable(
        len(meeting.project.employees),
        meeting.needs_projector,
        meeting.needs_video_conference
    )]

    suitable_rooms.sort(key=lambda x: x.size)

    # Check room availability
    for room in suitable_rooms:
        if is_room_available(room, meeting.start_time, meeting.duration, schedule):
            return room

    #If none is found then random will do
    return random.choice(rooms)

def is_room_available(room, start_time, duration, schedule):
    end_time = start_time + duration
    for meeting in schedule:
        if meeting.room == room:
            if not (meeting.start_time + meeting.duration <= start_time or
                    meeting.start_time >= end_time):
                return False
    return True