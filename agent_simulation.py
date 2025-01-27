import random

# Constants
STAIRCASE_LENGTH = 10  # Number of steps in the staircase
K = 4  # Distance within which agents can see each other

# Directions
UP = -1
DOWN = 1

# Slot indices
LEFT = 0
MIDDLE = 1
RIGHT = 2

# Flag
RETURN_TO_MIDDLE = False

data = None

# Initialize the staircase
# Each step is represented as a list of 3 slots: [left, middle, right]
# None means the slot is empty, otherwise it stores the direction of the agent (UP or DOWN)
staircase = [[None, None, None] for _ in range(STAIRCASE_LENGTH)]

# Initialize step counts
# Each step is represented as a list of 3 slots: [left, middle, right]
# Each slot stores the cumulative number of timesteps agents have spent there
step_counts = [[0, 0, 0] for _ in range(STAIRCASE_LENGTH)]

def print_staircase():
    """Print the current state of the staircase."""
    for step in staircase:
        print("|".join([" " if slot is None else "↑" if slot == UP else "↓" for slot in step]))
    print("-" * (3 * STAIRCASE_LENGTH))

# def print_step_counts():
#     """Print the cumulative step counts for each slot in the staircase."""
#     print("Cumulative Step Counts:")
#     for step in step_counts:
#         print("|".join([f"{count:3}" for count in step]))
#     print("-" * (3 * STAIRCASE_LENGTH))

def print_step_counts():
    """Print the cumulative step counts for each slot in the staircase as a Python array."""
    print("step_counts = [")
    for i, step in enumerate(step_counts):
        # Format the step as a list of integers
        step_str = "    [" + ", ".join(f"{count:3}" for count in step) + "]"
        # Add a comma unless it's the last step
        if i < STAIRCASE_LENGTH - 1:
            step_str += ","
        print(step_str)
    print("]")
    return f'[{step_str}]'

def spawn_agent(position, direction):
    """Spawn an agent at the given position and direction."""
    step = staircase[position]

    for d in range(1, K + 1):
        if 0 <= position + d * direction < STAIRCASE_LENGTH:  # scan ahead
            opposing_step = staircase[position + d * direction]
            if any(slot == -direction for slot in opposing_step):
                # Move to the rightmost slot from their perspective
                if direction == DOWN:
                    step[LEFT] = direction
                else:
                    step[RIGHT] = direction
                break
    else:
        step[MIDDLE] = direction

def move_agents():
    """Move all agents according to the rules."""
    global staircase
    new_staircase = [[None, None, None] for _ in range(STAIRCASE_LENGTH)]

    for i in range(STAIRCASE_LENGTH):
        for j in range(3):
            if staircase[i][j] is not None:
                direction = staircase[i][j]
                new_position = i + direction

                ### Agent remains on staircase
                if 0 <= new_position < STAIRCASE_LENGTH:
                    # Check if the agent needs to move to the rightmost slot
                    if j == MIDDLE:
                        # Check for opposing agents within distance K
                        for d in range(1, K + 1):
                            if 0 <= i + d * direction < STAIRCASE_LENGTH:  # scan ahead
                                opposing_step = staircase[i + d * direction]
                                if any(slot == -direction for slot in opposing_step):
                                    # Move to the rightmost slot from their perspective
                                    if direction == DOWN:
                                        target_slot = LEFT
                                    else:
                                        target_slot = RIGHT
                                    break
                        else:  # no opposing people in sight
                            target_slot = j

                    else:  # is not in the middle
                        if RETURN_TO_MIDDLE:
                            for d in range(1, K + 1):
                                if 0 <= i + d * direction < STAIRCASE_LENGTH:  # scan ahead
                                    opposing_step = staircase[i + d * direction]
                                    if any(slot == -direction for slot in opposing_step):
                                        # Move to the rightmost slot from their perspective
                                        if direction == DOWN:
                                            target_slot = LEFT
                                        else:
                                            target_slot = RIGHT
                                        break
                            else:  # no opposing people in sight
                                target_slot = MIDDLE
                        else:
                            target_slot = j

                    # Move the agent
                    new_staircase[new_position][target_slot] = direction

                else:
                    # Agent has reached the end of the staircase and is removed
                    pass

    # Update step counts for the current timestep
    for i in range(STAIRCASE_LENGTH):
        for j in range(3):
            if staircase[i][j] is not None:
                step_counts[i][j] += 1

    staircase = new_staircase

def simulate(steps):
    """Run the simulation for a given number of steps."""
    for step in range(steps):
        # print(f"Step {step + 1}:")
        # Spawn new agents at the top and bottom


        if random.random() < 0.5:
            if random.random() < 0.02:
                spawn_agent(0, DOWN)
                if random.random() < 0.3:
                    spawn_agent(STAIRCASE_LENGTH - 1, UP)
        else:

            if random.random() < 0.02:
                spawn_agent(STAIRCASE_LENGTH - 1, UP)

                if random.random() < 0.3:
                    spawn_agent(0, DOWN)




        # print_staircase()
        move_agents()

    # Print cumulative step counts at the end of the simulation
    data = eval(print_step_counts())

# Run the simulation for 10 steps
simulate(5000)