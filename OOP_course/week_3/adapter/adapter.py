class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee
        self.lights = []
        self.obstacles = []

    def lighten(self, grid):
        self.dim = (len(grid[0]), len(grid))
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 1:
                    self.lights.append((j,i))
                elif grid[i][j] == -1:
                    self.obstacles.append((j,i))
        
        self.adaptee.set_dim(self.dim)
        self.adaptee.set_obstacles(self.obstacles)
        self.adaptee.set_lights(self.lights)
        return self.adaptee.generate_lights()