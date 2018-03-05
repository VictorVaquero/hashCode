""" Variable definition:
    R : Number of rows
    C : Number of columns
    F : Number of vehicles( They all start at (0,0))
    N : Number of rides
    B : Bonus
    T : Stepst in the simulation
    -------------
    rides : List of individual rides
        a: Starting intersection row
        b: Starting intersection column
        x: Finishing intersection row
        y: Finishing intersection column
        s: Earliest start
        f: Latest finish
    -------------
    rides_done: Whether or not the ride has been asigned to a vehicle
        c: What car will do the ride
        sr: Step at which the car will start the ride
        fr: Step at which the car will finish the ride
    -------------
    vehicles : List of individual cars
        v: List of rides index
            i: Index of the ride
        (The car's position is that of the finish intersection
        of his last ride. If it has no rides, it is equal to (0,0))

"""

INITIAL_POS = (0, 0)
INITIAL_TIME = 0


def doRide(car, ride):
    """ Compute when the car could do it,
        when would it finish it and
        if it could win the bonus
        Return->
            rs: When the car could do the ride
            rf: When the car could finish the ride
            b: Whether or not the car could win the bonus
        EXCEPTION: Return None if the car can't make the ride

    """
    global MAX_DISTANCE_START, MAX_DISTANCE_FINISH
    (a, b, x, y, s, f) = ride
    lenght_ride = abs(x - a) + abs(y - b)
    # Simple heuristic to make it faster
    if lenght_ride > MAX_DISTANCE_FINISH:  # So it doesn't take too long rides
        return None
    if car is None or len(car) == 0:  # No car or no rides asigned to the car
        (cx, cy) = INITIAL_POS
        cs = INITIAL_TIME
    else:  # Else, look in the list
        last_ride = car[-1]
        (cx, cy) = tuple(rides[last_ride][0:2])  # Position of the car
        # When will the car be at that position
        cs = rides_done[last_ride][2]
    # Distance to the ride's starting intersection
    distance = abs(cx - a) + abs(cy - b)
    if distance > MAX_DISTANCE_START:  # Do not take too far away ones
        return None
    when = max(cs + distance, s)
    if when + lenght_ride > f:  # The car cant make it
        return None

    return when, when + lenght_ride, when == s

# Main


(R, C, F, N, B, T) = map(int, input().split(" "))

rides = []
for i in range(N):
    rides.append([int(x) for x in input().split(" ")])
# End of file read
rides_done = [None] * N
vehicles = [None] * F
MAX_DISTANCE_START = max(R, C)   # How far it looks to start a ride
# How far is willing to go for a single ride
MAX_DISTANCE_FINISH = max(R, C) / 4
TIME_DIVISIONS = 5
RIDES_CUTS = int(N / TIME_DIVISIONS)

# Order the rides by starting step
time_ordered_rides = sorted(range(N), key=lambda x: rides[x][4])

for t in range(TIME_DIVISIONS):
    no_more = 0
    # Until the algorith cannot find any more suitable rides
    while no_more < RIDES_CUTS:
        for j in range(len(vehicles)):
            c = vehicles[j]
            ride = None
            for i in time_ordered_rides[t * RIDES_CUTS:N if t == TIME_DIVISIONS else (t + 1) * RIDES_CUTS]:
                r = rides[i]
                info = doRide(c, r)
                if info is None:  # Ride is no good
                    continue
                (s, p, b) = info  # Right now I just use the first step
                if((rides_done[i] is None or rides_done[i][1] > s)
                        and (ride is None or rs > s)):
                    # Only do it if the car can do it earlier
                    # than every other car, and every other ride
                    ride = i
                    (rs, rf, rb) = info
            # If a new ride is selected, state it
            if ride is not None:
                # If the ride was already asigned, take it away
                if rides_done[ride] is not None:
                    aux = None
                    # Delete every ride to the one we want from
                    #    both lists, rides_done and vehicles
                    while(aux != ride):
                        aux = vehicles[rides_done[ride][0]].pop()
                        rides_done[aux] = None
                rides_done[ride] = (j, rs, rf)
                if c is None:
                    vehicles[j] = c = []
                c.append(ride)
                no_more = 0
            else:
                no_more += 1
# print("Number of vehicles: ", F)
# print("Number of rides: ", N)
# print(vehicles)
for v in vehicles:
    if v is None:
        print("0")
    else:
        print(len(v), end="")
        for i in v:
            print(" ", i, end="")
        print("")
