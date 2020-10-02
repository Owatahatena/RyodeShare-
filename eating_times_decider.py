import random

#boarders_info = [(1,1),(2,3),(3,3),(4,1),(5,2),(6,3),(7,4),(8,1),(9,2),(10,1),(11,2),(12,3),(13,1),(14,3),(15,4),(16,2),(17,3),(18,2),(19,4),(20,2)]

boarders_info_size = 0

up_to_seat_of_one_group = [10,10,10,10]

request_groups = []

members_of_groups = []

output_boarders_info = []

class Seat:
    def __init__(self):
        self.ID = ID
        self.request_group = request_group

    def decide_seat(ID,request_place):
        if not up_to_seat_of_one_group[request_place-1] == len(members_of_groups[request_place-1]):
            __rest_space_of_groups(self.ID)
        else:
            __not_rest_space_of_groups(self.ID)
            
    def __rest_space_of_groups(ID):
        members_of_groups[request_place-1].append(ID)
    
   # def __not_rest_space_of_groups(ID):
        

    
def set_size_members_of_groups():
    for group in range(len(up_to_seat_of_one_group)):
        members_of_groups.append([])
        request_groups.append(0)

def get_eating_times(boarders_info):
    #up_to_seat_of_one_group = input_up_to_seat_of_one_group

#    up_to_seat_of_one_group = [10,10,10,10]
 #   request_groups = []
  #  members_of_groups = []
    output_boarders_info = []

    boarders_info_size = len(boarders_info)
    set_size_members_of_groups()
    print(members_of_groups)

    randomized_boarders_info=random.sample(boarders_info,boarders_info_size)

    sorted_boarders_info=sorted(randomized_boarders_info,key=lambda boarders_info: boarders_info[1])

    print(sorted_boarders_info)

    for member in boarders_info:
        request_groups[member[1]-1] += 1

    check_member_decide_times = []
    current_seat_of_one_group = [0]*len(up_to_seat_of_one_group)

    for member in sorted_boarders_info:
        if request_groups[member[1]-1] <= up_to_seat_of_one_group[member[1]-1]:
            output_boarders_info.append(member)
            check_member_decide_times.append(1)
            current_seat_of_one_group[member[1]-1] += 1
        else:
            check_member_decide_times.append(0)

    current_time = 1

    for member in range(len(sorted_boarders_info)):
        if check_member_decide_times[member] == 1:
            continue
        else:
            while True:
                if(current_seat_of_one_group[current_time-1] < up_to_seat_of_one_group[current_time-1]):
                    output_boarders_info.append((sorted_boarders_info[member][0],current_time))
                    current_seat_of_one_group[current_time-1] += 1
                    break
                else:
                    current_time += 1
    sorted_output_boarders_info = sorted(output_boarders_info,key=lambda boarders_info: boarders_info[1])
    
    print(sorted_boarders_info)
    print(sorted_output_boarders_info)
    print(request_groups,up_to_seat_of_one_group)
    return sorted_output_boarders_info
    #randomized_boarders_info = 
    #for boarder in boarders_info_size:
