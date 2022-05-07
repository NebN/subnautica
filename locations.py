from dataclasses import dataclass
from enum import Enum
import csv

def get_locations():
    locations = []

    with open('locations.csv') as locations_file:
        reader = csv.DictReader(locations_file, delimiter=';')
        for row in reader:
            degrees_from_root = orientations_to_degrees(
                orientation_from_location=row['orientation_from_location'],
                orientation_from_root=row['orientation_from_root']
            )
            # print(row['name'], degrees_from_root)
            locations.append(
                Location(
                    name=row['name'],
                    depth=int(row['depth']) if row['depth'] else 0,
                    distance=int(row['distance']),
                    degrees_from_root=degrees_from_root
                )
            )
    
    return locations

class Cardinality(Enum):
    E = 0
    NE = 45
    N = 90
    NW = 135
    W = 180
    SW = 225
    S = 270
    SE = 315

    def degrees(self):
        return self.value

@dataclass
class Location:
    name: str
    depth: int
    distance: int
    degrees_from_root: float

def orientations_to_degrees(orientation_from_location, orientation_from_root):
    def orientation_to_degrees(orientation):
        base_cardinality, *maybeOffset = orientation.split('+')
        base_degrees = Cardinality[base_cardinality].degrees()
        offset_degrees = float(maybeOffset[0]) * 7.5 if maybeOffset else 0
        return base_degrees - offset_degrees

    if orientation_from_root:
        return orientation_to_degrees(orientation_from_root)
    else:
        degrees_from_location = orientation_to_degrees(orientation_from_location)
        flipped = degrees_from_location + 180
        if flipped > 360:
            return flipped - 360
        else:
            return flipped        
