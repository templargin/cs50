class Flight:

    counter = 1

    def __init__(self, origin, destination, duration):

        # keep track of ID number
        self.id = Flight.counter
        Flight.counter += 1

        # passengers on this Flight
        self.passengers = []

        # flight details
        self.origin = origin
        self.destination = destination
        self.duration = duration

    def print_info(self):
        print(f"Flight origin : {self.origin}")
        print(f"Flight destination : {self.destination}")
        print(f"Flight duration : {self.duration}")

        print()

        print("Passengers:")
        for passenger in self.passengers:
            print(f"{passenger.name}")

    def delay(self, amount):
        self.duration += amount

    def add_passenger(self, p):
        self.passengers.append(p)
        p.flight_id = self.id
