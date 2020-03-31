from flight import Flight
from passenger import Passenger

def main():
    f = Flight("New York", "Paris", 540)

    alice = Passenger("Alice")
    bob = Passenger("Bob")

    f.add_passenger(alice)
    f.add_passenger(bob)

    f.print_info()
    print(alice.flight_id)


if __name__ == "__main__":
    main()
