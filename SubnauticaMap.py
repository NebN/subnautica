from tkinter import *
import math


class SubnauticaMap:

    WIDTH = 1000
    HEIGHT = 1000
    CENTER_X, CENTER_Y = WIDTH / 2, HEIGHT / 2
    HUNDRED_METERS_SIZE = 20
    SCALE = 100 / HUNDRED_METERS_SIZE

    LOCATION_SIZE = 10
    HALF_LOCATION_SIZE = LOCATION_SIZE / 2

    def __init__(self):
        self.root = Tk()
        self.root.title('subnautica')
        self.root.geometry(f"{SubnauticaMap.WIDTH}x{SubnauticaMap.HEIGHT}")
        self.canvas = Canvas(self.root, width=SubnauticaMap.WIDTH, height=SubnauticaMap.HEIGHT, background="#468b94")
        self.canvas.pack()

        self.red_range = list(reversed(range(0x00, 0xFF)))
        self.red_max_ix = len(self.red_range) - 1
        self.green_range = list(reversed(range(0x00, 0xFF)))
        self.green_max_ix = len(self.green_range) - 1
        self.blue_range = list(reversed(range(0x00, 0xFF)))
        self.blue_max_ix = len(self.blue_range) - 1
        self.max_depth = 0

    def show(self, locations):
        max_distance = max(map(lambda x: x.distance, locations))
        self.max_depth = max(map(lambda x: x.depth, locations))
        self.scale =  SubnauticaMap.WIDTH / 2 / (max_distance + 100)
        house_size = SubnauticaMap.LOCATION_SIZE * 2
        half_house_size = house_size / 2
        self.canvas.create_rectangle(
            SubnauticaMap.CENTER_X - half_house_size, 
            SubnauticaMap.CENTER_Y - half_house_size, 
            SubnauticaMap.CENTER_X + half_house_size, 
            SubnauticaMap.CENTER_Y + half_house_size, 
            fill="red")
        for location in locations:
            self.draw_location(location)
        
        self.root.mainloop()

    @staticmethod
    def real_distance(location):
        return math.sqrt((location.distance * location.distance) - (location.depth * location.depth))

    def location_to_coordinates(self, location):
        magnitude = SubnauticaMap.real_distance(location) * self.scale
        x = math.cos(math.radians(location.degrees_from_root)) * magnitude

        # Y axis is reversed as top is 0 and bottom is WIDTH
        y = - math.sin(math.radians(location.degrees_from_root)) * magnitude
        # print(location.name, location.degrees_from_root, x, y)
        return x, y


    def depth_color(self, location):
        position = location.depth / self.max_depth

        red_ix = int(self.red_max_ix * position)
        green_ix = int(self.green_max_ix * position)
        blue_ix = int(self.blue_max_ix * position) 

        red = self.red_range[red_ix]
        green = self.green_range[green_ix]
        blue = self.blue_range[blue_ix]

        color = f'#{red:0>2X}{green:0>2X}{blue:0>2X}' 

        return color

    def draw_location(self, location):
        x, y = self.location_to_coordinates(location)

        # TOP LEFT (x,y)
        x1 = SubnauticaMap.CENTER_X + x - SubnauticaMap.HALF_LOCATION_SIZE
        y1 = SubnauticaMap.CENTER_Y + y - SubnauticaMap.HALF_LOCATION_SIZE

        # BOTTOM RIGHT (x,y)
        x2 = x1 + SubnauticaMap.LOCATION_SIZE
        y2 = y1 + SubnauticaMap.LOCATION_SIZE

        # print(location.name, x1, y1, x2, y2)

        self.canvas.create_oval(x1, y1, x2, y2, fill=self.depth_color(location))
        text_fill = 'orange' if 'portal destination' in location.name.lower() else 'black'
        self.canvas.create_text(x1, y1 + 15, text=f'{location.name} ({location.depth}m)', fill=text_fill)
