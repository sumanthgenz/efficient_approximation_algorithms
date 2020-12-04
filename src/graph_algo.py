import networkx as nx
from parse import *
from utils import *
import sys
from os.path import basename, normpath
import glob

def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
    n = G.number_of_nodes()
    rooms = [list(range(0,n))]
    n_rooms = 1

    # while True:
    
    #shuffle(rooms)
    best_moves = []
    old_from_room, old_to_room = None, None
    new_from_room, new_to_room = None, None

    invalid_rooms = [(calculate_stress_for_room(r, G) > (s/n_rooms)) for r in rooms]
    if any(invalid_rooms):
        from_idx = invalid_rooms.index(True)
        old_from_room = rooms[from_idx]
        # max_dec_S, min_dec_H = 0, float('inf')
       
       #define as sum of best reduction and stress and best 
        max_score = 0
        optimal_student_idx, filtered_rooms = None, None

        for student_idx in range(len(old_from_room)):
            new_from_room = old_from_room[:student_idx] + old_from_room[student_idx + 1:]
            dec_S =  calculate_stress_for_room(old_from_room, G) - calculate_stress_for_room(new_from_room, G)
            # dec_H = calculate_happiness_for_room(filtered_rooms, G)

            # if dec_H < min_dec_H:
            #     min_dec_H = dec_H
            #     optimal_student_idx = student_idx
            # if dec_S > max_dec_S:
            #     max_dec_S = dec_S
            #     optimal_student_idx = student_idx
            # print(min_dec_H, max_dec_S)
        
            #see if its possible to move the optimal student to an existing room besides the one they just got removed form
            for to_idx in range(len(rooms)):
                if from_idx != to_idx:
                    old_to_room = rooms[to_idx]
                    new_to_room = old_to_room + [old_from_room[student_idx]]
                    inc_H = calculate_happiness_for_room(new_to_room, G) + calculate_happiness_for_room(old_to_room, G)
                    if (calculate_stress_for_room(new_to_room, G) > (s/n_rooms)):
                        best_moves.append((dec_S + inc_H, from_idx, to_idx, student_idx))
                    else:
                        best_moves.append(dec_S, from_idx, 'n/a', student_idx)
                    
        best_moves = sorted(best_moves, key=lambda x: -x[0])
        move = best_moves[0]

        #move is tuple (happiness, from_room_idx, to_room_idx, student_from_room_idx)

        #if no possible move to existing room, place them in a new room
        if move[2] == 'n/a':
            rooms[move[1]] = rooms[move[1]][:move[3]] + rooms[move[1]][move[3]+1:]
            rooms.append([old_from_room[optimal_student_idx]])
            n_rooms += 1

        else:
            rooms[move[2]].append(rooms[move[1]][move[3]])
            rooms[move[1]] = rooms[move[1]][:move[3]] + rooms[move[1]][move[3]+1:]

        rooms[from_idx] = old_from_room[:optimal_student_idx] + old_from_room[optimal_student_idx+1:]
        rooms.append([old_from_room[optimal_student_idx]])
        n_rooms += 1

    else:
        #format per elem: (happiness, room idx fro, room idx to, student idx in fro)
        for from_idx in range(len(rooms)):
            for student_idx in range(len(rooms[from_idx])):
                for to_idx in range(len(rooms)):
                    if from_idx != to_idx:
                        old_from_room = rooms[from_idx]
                        old_to_room = rooms[to_idx]
                        new_from_room = old_from_room[:student_idx] + old_from_room[student_idx + 1:]
                        new_to_room = old_to_room + [old_from_room[student_idx]]


                        #check that proposed move is valid
                        #happines from move = (new_to_room - old_to_room) + (new_from_room - old_from_room)

        #calculate whether moving a given student to their own breakout is more optimal

        #randomly choose between top5 best moves with 70% probability, top10 with 20% probability, bottom 10 with 10% probability 


    #     print(calculate_happiness_for_room([0,1,2], G))
    #     print(calculate_stress_for_room([0,1,2], G))

    return None, None
    pass
    # return convert_dictionary(rooms)


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
<<<<<<< HEAD
    # small_hitlist = [5, 12, 14, 17, 21, 25, 29, 31, 36, 40, 41, 42, 43, 44, 
    # 49, 57, 58, 62, 64, 65, 66, 67, 68, 70, 76, 81, 82, 84, 85, 89, 
    # 91, 92, 93, 96, 98, 102, 104, 106, 107, 112, 117, 118, 119, 122,
    # 125, 126, 129, 132, 134, 135, 136, 138, 141, 143, 149, 150, 154,
    # 155, 157, 160, 163, 165, 167, 169, 171, 179, 181, 183, 185, 194, 
    # 210, 212, 216, 219, 222, 231, 234, 236, 239]

    # maybe = [141]
    # small_hitlist = [14, 29, 85, 117, 129, 134, 155, 
    # 234]

    # print(len(small_hitlist))

    # for i in range(len(small_hitlist[:1])):
        # num = small_hitlist[i]

    # paths = ["data/inputs/small-{}.in".format(num)]*num_rollouts


    num_rollouts = 2
    inputs = glob.glob('data/inputs/large?*.in')
    for input_path in inputs:

        cores = multiprocessing.cpu_count()
        paths = [input_path] * num_rollouts
        output_path = 'data/anik_large_outputs/' + basename(normpath(input_path))[:-3] + '.out'

        with multiprocessing.Pool(cores) as p:
            rollouts = p.map(solo_main, paths)

    
        rollouts = sorted(rollouts, key=lambda x: -x[0])
        max_score, max_Dict = rollouts[0][0], rollouts[0][1]
        # print("Medium-{} Total Happiness: {}".format(input_path[-3:], max_score))
        write_output_file(max_Dict, output_path)

    # for _ in range(num_rollouts):
    #     D, k = solve(G, s, greed=False, max_step=50)
    #     assert is_valid_solution(D, G, s, k)

    #     Dg, kg = solve(G, s, greed=True, max_step=60)
    #     assert is_valid_solution(Dg, G, s, kg)
    #     careful = calculate_happiness(D ,G)
    #     greedy = calculate_happiness(Dg ,G)
    #     if careful > max_c:
    #         max_c = careful
    #         max_D = D

    #     if greedy > max_g:
    #         max_g = greedy
    #         max_Dg = Dg

    # if max_c >= max_g:
    #     print("Total Happiness: {}".format(max_c))
    #     # write_output_file(D, 'new_outputs/small-1.out')

    # else:
    #     print("Total Happiness: {}".format(max_g))
    #     # write_output_file(Dg, 'new_outputs/small-1.out')

# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('data/inputs/medium?*.in')
#     for input_path in inputs:
#         output_path = 'data/outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path)


#         D, k = solve(G, s, greed=False, max_step=50)
#         assert is_valid_solution(D, G, s, k)

#         Dg, kg = solve(G, s, greed=True, max_step=60)
#         assert is_valid_solution(Dg, G, s, kg)

#         careful = calculate_happiness(D ,G)
#         greedy = calculate_happiness(Dg ,G)

#         if careful >= greedy:
#             write_output_file(D, output_path)
=======
    # assert len(sys.argv) == 2
    # path = sys.argv[1]
    path = "data/inputs/medium-31.in"
    G, s = read_input_file(path)
    D, k = solve(G, s)
    # assert is_valid_solution(D, G, s, k)
    # print("Total Happiness: {}".format(calculate_happiness(D, G)))
    # write_output_file(D, 'new_outputs/small-1.out')
>>>>>>> parent of 598dc1b... yea


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('inputs/*')
#     for input_path in inputs:
#         output_path = 'new_ outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         happiness = calculate_happiness(D, G)
#         write_output_file(D, output_path)