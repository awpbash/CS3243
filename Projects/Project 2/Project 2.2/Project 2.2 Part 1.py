import random
def search(dct):
    values = dct['values']
    count = dct['count']
    size = dct['size']
    return best_first_climb_with_restarts(values, count, size)

# best first Hill Climbing with Random Restarts
def best_first_climb_with_restarts(values, count, size, max_iterations=100000, max_restarts=5, accept_probability=0.05):
    """Perform best first hill climbing with random restarts to balance the partition."""
    best_partition = []
    best_cost = float('inf')
    target = sum(values) // count #O(n)

    start = greedy(values, count, size)  #O(n)
    
    for restart in range(max_restarts):
        #alternate between greedy initialization and random initialization
        if restart % 2 == 0:
            partition = start  # Greedy partition
        else:
            partition = random_initial_partition(values, count, size)  # Random partition
        
        subset_sums = [sum(subset) for subset in partition]
        curr_cost = calculate_partition_cost(subset_sums, target)

        for i in range(max_iterations):
            new_cost = swap(partition, subset_sums, size, target)
            if new_cost <= curr_cost:
                curr_cost = new_cost
            #introduce randomness to avoid local minima
            elif random.random() < accept_probability:
                curr_cost = new_cost
            if curr_cost == 0:
                break


        #check if best so far
        if curr_cost < best_cost:
            best_partition = [subset[:] for subset in partition]
            best_cost = curr_cost
        #best found
        if best_cost == 0:
            break

    return best_partition

#smart swapping
def swap(partition, subset_sums, size, target):
    #find subsets with sums below and above the target
    above_target = [i for i in range(len(partition)) if subset_sums[i] > target] 
    below_target = [i for i in range(len(partition)) if subset_sums[i] < target]

    #randomly select 1 subset above and 1 below
    subset1_idx = random.choice(above_target)
    subset2_idx = random.choice(below_target)
    subset1 = partition[subset1_idx]
    subset2 = partition[subset2_idx]

    #choose random elements to swap between these subsets
    #this one somehow faster than swapping max and min  
    element_from_above = random.choice(subset1)
    element_from_below = random.choice(subset2)
    
    subset1[subset1.index(element_from_above)], subset2[subset2.index(element_from_below)] = element_from_below, element_from_above

    #update sum quickly without needing to recalculate -> O(1) instead of O(n)
    subset_sums[subset1_idx] = subset_sums[subset1_idx] - element_from_above + element_from_below
    subset_sums[subset2_idx] = subset_sums[subset2_idx] - element_from_below + element_from_above

    return calculate_partition_cost(subset_sums, target)

def calculate_partition_cost(subset_sums, target):
    return sum(abs(subset_sum - target) for subset_sum in subset_sums)

def greedy(values, count, size):
    """Generate a partition where values are distributed by alternating between the largest and smallest."""
    values.sort(reverse=True)  # Sort values in descending order
    partition = [[] for _ in range(count)]
    partition_idx = 0  # Pointer to track the partition we are assigning values to
    left = 0  # Start index (largest element)
    right = len(values) - 1  # End index (smallest element)
    # We alternate between adding the largest and smallest element
    is_largest_turn = True
    # Continue until all values are placed into partitions
    while left <= right:
        for i in range(count):
            if is_largest_turn:
                # Add the largest remaining value from the left
                if left <= right and len(partition[i]) < size:
                    partition[i].append(values[left])
                    left += 1
            else:
                # Add the smallest remaining value from the right
                if left <= right and len(partition[i]) < size:
                    partition[i].append(values[right])
                    right -= 1
        
        # Switch between adding the largest and smallest
        is_largest_turn = not is_largest_turn
    return partition

def random_initial_partition(values, count, size):
    """Generate a random initial partition."""
    random.shuffle(values)  # Shuffle the values randomly
    return [values[i * size: (i + 1) * size] for i in range(count)]

'''
Big idea my guy
First we do a greedy initialization. In here we alternate addind the largest and smallest values to the partitions
This hopefully brings all partitions close to the target sum without needing to compute the sum of each partition
We also do a random initialization. This is just to make sure we don't get stuck in a local minimum
Now for swapping logic, we use a best first hill climbing algorithm with random restarts
When searching we do a smart swap algo whereby we take 2 subsets, one with a sum above the target and one below
We then swap elements between these subsets to try and balance them
We also have a small probability to accept worse solutions to avoid getting stuck in local minima
Then hopefullee we get the best partition
Cost function is the sum of absolute differences between the target sum and the sum of each subset
'''