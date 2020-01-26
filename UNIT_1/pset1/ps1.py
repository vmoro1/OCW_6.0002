from ps1_partition import get_partitions
import time


def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name and weight pairs(cow name, weight), and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cow_dict = dict()
    f = open(filename, 'r')  
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows.
    The greedy heuristic follows the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    transportationList = []
    cow_dict = cows.copy()
    cows_sorted_weight = sorted(cows, key = lambda x : cows[x], reverse = True)  
    while bool(cow_dict):
        weight_on_ship = 0
        tmp_transportationList = []
        cows_sorted_weightCopy = cows_sorted_weight[:]
        for cow in cows_sorted_weightCopy:
            if (cow_dict[cow] + weight_on_ship) <= limit:
                tmp_transportationList.append(cow)
                weight_on_ship += cow_dict[cow]
                cow_dict.pop(cow)
                cows_sorted_weight.remove(cow)
        transportationList.append(tmp_transportationList)
    return transportationList 


#print(greedy_cow_transport(load_cows("ps1_cow_data.txt")))


def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm follows the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    transportationList = []
    cowsList= list(cows)
    for partion in (get_partitions(cowsList)):
        tmp_transportationList = []
        for configuration in partion:
            weight_on_ship = 0     
            for cow in configuration:
                weight_on_ship += cows[cow]
            if weight_on_ship > limit:
                tmp_transportationList.append('hej')
#                break###
            else:
                tmp_transportationList.append(configuration)
        if 'hej' in tmp_transportationList:
            continue
        elif len(tmp_transportationList) < len(transportationList) or not bool(transportationList):
            transportationList = tmp_transportationList[:]
    return transportationList
  
    
#print(brute_force_cow_transport(load_cows("ps1_cow_data.txt")))
    
        
def compare_cow_transport_algorithms():
    """
    Print out the number of trips returned by each algorithmnd how long each
    algorithm takes to run in seconds.

    Returns:
    Does not return anything.
    """
    start = time.time()
    greedy_transportationList = greedy_cow_transport(load_cows("ps1_cow_data.txt"))
    end = time.time()
    print('The greedy algorithm requires ', len(greedy_transportationList), ' trips and takes ', end - start, ' seconds to run.\n')
    start = time.time()
    bruteForce_transportationList = brute_force_cow_transport(load_cows("ps1_cow_data.txt"))
    end = time.time()
    print('The brute force algorithm requires ', len(bruteForce_transportationList), ' trips and takes ', end - start, ' seconds to run.')
    

#compare_cow_transport_algorithms()