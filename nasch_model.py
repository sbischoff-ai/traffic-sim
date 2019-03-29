from random import random
from time import sleep

class Car:
    def __init__(self, velocity:int=0, max_velocity:int=3, braking_prob:float=0.1):
        self.velocity = velocity
        self.max_velocity = max_velocity
        self.braking_prob = braking_prob

    def accelerate(self, free_space_ahead):
        if self.velocity < free_space_ahead and self.velocity < self.max_velocity:
            self.velocity += 1
        elif self.velocity > free_space_ahead:
            self.velocity = free_space_ahead

    def dawdle(self):
        if self.velocity > 0 and random() < self.braking_prob:
            self.velocity -= 1

class Cell:
    def __init__(self, car:Car=None):
        self.car = car

    def has_car(self):
        return self.car is not None

class Street:
    def __init__(self, length:int, constant_velocity:int=1, density:float=0.3):
        self.cells = [Cell() if random() > density else Cell(Car(constant_velocity)) for _ in range(length)]

    def nasch_step(self):
        next_step_cells = [Cell() for _ in range(len(self.cells))]
        for position, cell in enumerate(self.cells):
            if cell.has_car():
                cell.car.accelerate(self._space_ahead(position))
                cell.car.dawdle()
                next_step_cells[(position+cell.car.velocity)%len(self.cells)].car = cell.car
        self.cells = next_step_cells

    def simulate(self, timesteps:int, interval:float=1.0):
        for _ in range(timesteps):
            print(self)
            self.nasch_step()
            sleep(interval)

    @property
    def avg_velocity(self):
        cars = [cell.car.velocity for cell in self.cells if cell.has_car()]
        return sum(cars)/len(cars)

    def _space_ahead(self, position:int):
        current_position = position
        while True:
            current_position += 1
            if self.cells[current_position%len(self.cells)].has_car():
                return current_position - position - 1

    def __str__(self):
        result = ''.join(str(cell.car.velocity) if cell.car is not None else '_' for cell in self.cells)
        result += ' avg velocity: ' + '{:f}'.format(self.avg_velocity)
        return result
