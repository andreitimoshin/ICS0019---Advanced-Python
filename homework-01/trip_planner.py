class PublicTransport:
    def __init__(self, route: list[str]):
        self.route = route

    def calculate_fare(self, start_stop: str, end_stop: str) -> float:
        # Do not write a body for this method. Each subclass should define its own calculate_fare function.
        pass

    def __str__(self) -> str:
        # Do not write a body fot this method. Each subclass should define its own string representation.
        pass


class Bus(PublicTransport):
    def __init__(self, route: list[str], nr: int):
        super().__init__(route)
        self.nr = nr

    def calculate_fare(self, start_stop: str, end_stop: str) -> float:
        return 1.50

    def __str__(self) -> str:
        return f"Bus {self.nr} {self.route[-1]}"


class TrolleyBus(PublicTransport):
    def __init__(self, route: list[str], nr: int):
        super().__init__(route)
        self.nr = nr

    def calculate_fare(self, start_stop: str, end_stop: str) -> float:
        base_fee = 1.00
        additional_fee = 0.20 * ((self.route.index(end_stop) - self.route.index(start_stop)) // 3)
        return base_fee + additional_fee

    def __str__(self) -> str:
        return f"TrolleyBus {self.nr} {self.route[-1]}"


class Train(PublicTransport):
    def __init__(self, route: list[str], zones: dict[str, str]):
        super().__init__(route)
        self.zones = zones

    def calculate_fare(self, start_stop: str, end_stop: str) -> float:
        fare = 0.0
        visited_zones = set()
        for stop in self.route[self.route.index(start_stop):self.route.index(end_stop) + 1]:
            zone = self.zones[stop]
            if zone not in visited_zones:
                if zone == "Green":
                    fare += 0.75
                elif zone == "Blue":
                    fare += 0.55
                elif zone == "Red":
                    fare += 1.00
                visited_zones.add(zone)
        return round(fare, 2)

    def __str__(self) -> str:
        return f"Train {self.route[0]} - {self.route[-1]}"


class Trip:
    def __init__(self, transport: PublicTransport, start_stop: str, end_stop: str):
        self.transport = transport
        self.start_stop = start_stop
        self.end_stop = end_stop
        self.amount_of_stops = self.transport.route.index(end_stop) - self.transport.route.index(start_stop) + 1
        self.fare = self.transport.calculate_fare(start_stop, end_stop)

    def __str__(self) -> str:
        return f"Using '{self.transport}' ({self.amount_of_stops} stops), costing {self.fare}."


class TripPlanner:
    transports: list[PublicTransport] = []

    @classmethod
    def find_trips(cls, start_stop: str, end_stop: str) -> list[Trip]:
        """Return possible trips from start_stop to end_stop sorted by fare from lowest to highest."""
        possible_trips = []
        for transport in cls.transports:
            if start_stop in transport.route and end_stop in transport.route:
                trip = Trip(transport, start_stop, end_stop)
                possible_trips.append(trip)

        # Sort trips by fare from lowest to highest
        possible_trips.sort(key=lambda trip: trip.fare)

        return possible_trips

    @classmethod
    def plan_trip(cls):
        print('Welcome to Trip Planner 9000!')
        print('This trip planner will show you all the ways to get from A to B.\n')

        start_stop = input('Where would you like to travel from?  - ')
        end_stop = input('Where would you like to tarvel to?  - ')
        possible_trips = cls.find_trips(start_stop, end_stop)

        if len(possible_trips) == 0:
            print(f'\nSorry. There are no available routes from {start_stop} to {end_stop} at this time.')
            return

        print(f'There are {len(possible_trips)} available routes from {start_stop} to {end_stop}:')
        for i, trip in enumerate(possible_trips, start=1):
            print(f'{i}. {trip}')


if __name__ == '__main__':
    TripPlanner.transports = [
        Bus(
            ['Tallinn', 'Balti Jaam', 'Kelmiküla', 'Tehnika', 'Lilleküla', 'Kitseküla', 'Varre'],
            78,
        ),
        TrolleyBus(
            ['Ahtri', 'Linnahall', 'Tallinn', 'Balti Jaam', 'Kelmiküla', 'Tehnika', 'Lilleküla', 'Kitseküla', 'Varre'],
            56,
        ),
        Train(
            ['Tallinn', 'Lilleküla', 'Tondi', 'Järve', 'Rahumäe', 'Nõmme'],
            {
                'Tallinn': 'Green',
                'Lilleküla': 'Green',
                'Tondi': 'Blue',
                'Järve': 'Blue',
                'Rahumäe': 'Blue',
                'Nõmme': 'Red',
            },
        )
    ]
    TripPlanner.plan_trip()
    # -> Welcome to Trip Planner 9000!
    # -> This trip planner will show you all the ways to get from A to B.
    # ->
    # -> Where would you like to travel from? - Tallinn
    # -> Where would you like to travel to? - Lilleküla
    # ->
    # -> There are 3 available routes from Tallinn to Lilleküla:
    # -> 1. Using 'Train Tallinn - Nõmme' (1 stops), costing 0.75.
    # -> 2. Using 'TrolleyBus 56 Varre' (4 stops), costing 1.2.
    # -> 3. Using 'Bus 78 Varre' (4 stops), costing 1.5.