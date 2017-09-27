# Import a library of functions called 'pygame'
import pygame
from math import pi
import math
import numpy as np

# Initialize the game engine
pygame.init()


class MyRect:
    def __init__(self, points):
        self.points = points

    # def rotate(self, angle):
    #     pass
    #     rot_mat = np.matrix([[math.cos(angle), np.sin(angle)], [- math.sin(angle), np.cos(angle)]])
    #     points = np.dot(self.points, rot_mat)
    #     self.points = []
    #     for x in points:
    #         tup = ((x[0, 0], x[0, 1]))
    #         self.points.append(tup)

    def rotate(self, angle):
        # print "angle {}".format(angle)
        # get center of the square
        x_dist = np.abs(self.points[0][0] - self.points[2][0]) / 2
        y_dist = np.abs(self.points[0][1] - self.points[1][1]) / 2
        center = (self.points[0][0] + x_dist,
                  self.points[0][1] + y_dist)

        r = np.sqrt(np.power(x_dist, 2) + np.power(y_dist, 2))
        # print "radius is {}".format(r)
        # print "center is {}".format(center)
        for j, point in enumerate(self.points):
            # print "point {}".format(j + 1)
            delta_x = point[0] - center[0]
            delta_y = point[1] - center[1]
            slope = delta_y/delta_x
            # print "slope {}".format(slope)
            theta = np.arctan(slope)
            # print "original point {}".format(point)
            if j > 1:
                theta = math.radians((math.degrees(theta) + angle + 180))
            else:
                theta = math.radians((math.degrees(theta) + angle))
            # print "theta {}".format(theta)
            # print "theta in degrees {}".format(math.degrees(theta))
            x = center[0] + r * np.cos(theta)
            y = center[1] + r * np.sin(theta)
            new_point = (x, y)
            # print "new point {}".format(new_point)
            self.points[j] = new_point

    def get_points(self):
        points = self.points
        points.append(self.points[0])
        return points

class ScreenSaver():
    def __init__(self):
        # Define the colors we will use in RGB format
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        # Set the height and width of the screen
        self.size = [2000, 1500]
        self.screen = pygame.display.set_mode(self.size)

        pygame.display.set_caption("Example code for the draw module")

        # Loop until the user clicks the close button.
        self.done = False
        self.clock = pygame.time.Clock()

        self.x_pos = 200
        self.y_pos = 200

        self.x_stop = 500
        self.y_stop = 500

        self.num_recs = 10

        self.a = 1
        self.b = 1

        self.t = 0
        self.count = 0
        self.up = True

        self.tilt_increase = True

    def run(self):

        while not self.done:
            self.count += .01
            self.count = self.count % 100

            # This limits the while loop to a max of 10 times per second.
            # Leave this out and we will use all CPU we can.
            # clock.tick(100)

            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self.done = True  # Flag that we are done so we exit this loop

            # All drawing code happens after the for loop and but
            # inside the main while done==False loop.

            # Clear the screen and set the screen background
            self.screen.fill(self.WHITE)

            self.t += 1
            if self.t == 10:
                self.t = 0

            if self.x_pos < self.x_stop and self.up:
                self.x_pos += 1
            else:
                self.up = False
                self.x_pos -= 1
                if self.x_pos == 0:
                    self.up = True

            if self.y_pos < self.y_stop and self.up:
                self.y_pos += 1
            else:
                self.up = False
                self.y_pos -= 1
                if self.y_pos == 0:
                    self.up = True

            if self.t % 2 == 0:
                if self.a < 50 and self.tilt_increase:
                    self.a += 1
                else:
                    self.tilt_increase
                    self.a -= 1
                    if self.a == 0:
                        self.tilt_increase = True

                if self.b < 50 and self.tilt_increase:
                    self.b += 1
                else:
                    self.tilt_increase = False
                    self.b -= 1
                    if self.b == 0:
                        self.tilt_increase = True

            # print a, b, x_pos, y_pos, up


            # Draw a rectangle outline
            for i in range(self.num_recs):
                i = self.num_recs - i
                rect = MyRect([((i * self.a / 5.) + self.x_pos, (i * self.b / 5.) + self.y_pos),
                               ((i * self.a / 5.) + self.x_pos, (i * self.b / 5.) + self.y_pos + i * 10),
                               ((i * self.a / 5.) + self.x_pos + i * 10, (i * self.b / 5.) + self.y_pos + i * 10),
                               ((i * self.a / 5.) + self.x_pos + i * 10, (i * self.b / 5.) + self.y_pos)
                               ])

                # rotate rectangle
                # angle = ((np.sin(count * i * .1) + 1) / 2) * 360
                # if angle > 270 and up:
                #     angle = 0
                # rect.rotate(angle)
                points = rect.get_points()
                # pygame.draw.rect(screen, BLACK, [(i * a / 5.) + x_pos,(i * b / 5.) + y_pos, i * 10, i * 10], 2)
                pygame.draw.lines(self.screen, self.BLACK, False, points, 2)
            # pygame.draw.lines(screen, BLACK, False, [(10, 10), (10, 110), (110, 110), (110, 10), (10, 10)], 2)
            # Go ahead and update the screen with what we've drawn.
            # This MUST happen after all the other drawing commands.

            pygame.display.flip()
if __name__ == "__main__":
    ss = ScreenSaver()
    ss.run()
    # Be IDLE friendly
    pygame.quit()
