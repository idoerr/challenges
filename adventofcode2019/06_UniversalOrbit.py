
class PlanetOrbit:

    def __init__(self, orbit_parent, planet):
        self.planet = planet
        self.parent = orbit_parent
        self.indirect_orbits = None
    
    def get_indirect_orbits(self):
        if self.indirect_orbits == None:
            if self.parent is None:
                self.indirect_orbits = 0
            else:
                self.indirect_orbits = self.parent.get_indirect_orbits() + 1
        
        return self.indirect_orbits
    
    def __str__(self):
        return self.planet
    
def common_ancestor(first_planet, second_planet):

    first_planet_ancestors = set()

    while first_planet is not None:
        first_planet_ancestors.add(first_planet)
        first_planet = first_planet.parent
    
    while second_planet is not None:
        if second_planet in first_planet_ancestors:
            return second_planet
        second_planet = second_planet.parent
    
    return None

def min_steps(first_planet, second_planet):
    ancestor = common_ancestor(first_planet, second_planet)

    return first_planet.get_indirect_orbits() + second_planet.get_indirect_orbits() - 2 * ancestor.get_indirect_orbits()


input_file = 'adventofcode2019/06_UniversalOrbit.txt'

if __name__ == '__main__':

    file_obj = open(input_file, 'r')

    node_map = {}

    for orbit_desc in file_obj.readlines():
        parent_name, child_name = orbit_desc.rstrip().split(')')

        parent_planet = node_map.get(parent_name, None)
        if parent_planet is None:
            parent_planet = PlanetOrbit(None, parent_name)
            node_map[parent_name] = parent_planet
        
        child_planet = node_map.get(child_name, None)
        if child_planet is None:
            child_planet = PlanetOrbit(parent_planet, child_name)
            node_map[child_name] = child_planet
        elif child_planet.parent == None:
            child_planet.parent = parent_planet
        else:
            raise ValueError("Planet " + child_name + " is orbiting multiple planets!")
    
    print("Part 1 Result")
    sum_indirect_orbits = sum(map(PlanetOrbit.get_indirect_orbits, node_map.values()))

    print(sum_indirect_orbits)

    print()
    print("Part 2 Result")

    you_ref = node_map["YOU"]
    san_ref = node_map["SAN"]

    print(min_steps(you_ref, san_ref) - 2)


