import locations
from SubnauticaMap import SubnauticaMap

locations = locations.get_locations()

sub_map = SubnauticaMap()
sub_map.show(locations)