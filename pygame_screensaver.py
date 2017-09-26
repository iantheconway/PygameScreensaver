# Import a library of functions called 'pygame'
import pygame
from math import pi
import math
import numpy as np

# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the height and width of the screen
size = [2000, 1500]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Example code for the draw module")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

x_pos = 200
y_pos = 200

x_stop = 500
y_stop = 500

num_recs = 10

a = 1
b = 1

t = 0
count = 0
up = True

tilt_increase = True


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

    def unit_vector(self, vector):
        """ Returns the unit vector of the vector.  """
        return vector / np.linalg.norm(vector)

    def angle_between(self, v1, v2):
        """ Returns the angle in radians between vectors 'v1' and 'v2'::

                >>> angle_between((1, 0, 0), (0, 1, 0))
                1.5707963267948966
                >>> angle_between((1, 0, 0), (1, 0, 0))
                0.0
                >>> angle_between((1, 0, 0), (-1, 0, 0))
                3.141592653589793
        """
        v1_u = self.unit_vector(v1)
        v2_u = self.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

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


while not done:
    count += .01
    count = count % 100

    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    # clock.tick(100)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # All drawing code happens after the for loop and but
    # inside the main while done==False loop.

    # Clear the screen and set the screen background
    screen.fill(WHITE)

    t += 1
    if t == 10:
        t = 0

    if x_pos < x_stop and up:
        x_pos += 1
    else:
        up = False
        x_pos -= 1
        if x_pos == 0:
            up = True

    if y_pos < y_stop and up:
        y_pos += 1
    else:
        up = False
        y_pos -= 1
        if y_pos == 0:
            up = True

    if t % 2 == 0:
        if a < 50 and tilt_increase:
            a += 1
        else:
            tilt_increase
            a -= 1
            if a == 0:
                tilt_increase = True

        if b < 50 and tilt_increase:
            b += 1
        else:
            tilt_increase = False
            b -= 1
            if b == 0:
                tilt_increase = True

    # print a, b, x_pos, y_pos, up


    # Draw a rectangle outline
    for i in range(num_recs):
        i = num_recs - i
        rect = MyRect([((i * a / 5.) + x_pos, (i * b / 5.) + y_pos),
                       ((i * a / 5.) + x_pos, (i * b / 5.) + y_pos + i * 10),
                       ((i * a / 5.) + x_pos + i * 10, (i * b / 5.) + y_pos + i * 10),
                       ((i * a / 5.) + x_pos + i * 10, (i * b / 5.) + y_pos)
                       ])

        # rotate rectangle
        # angle = ((np.sin(count * i * .1) + 1) / 2) * 360
        # if angle > 270 and up:
        #     angle = 0
        # rect.rotate(angle)
        points = rect.get_points()
        # pygame.draw.rect(screen, BLACK, [(i * a / 5.) + x_pos,(i * b / 5.) + y_pos, i * 10, i * 10], 2)
        pygame.draw.lines(screen, BLACK, False, points, 2)
    # pygame.draw.lines(screen, BLACK, False, [(10, 10), (10, 110), (110, 110), (110, 10), (10, 10)], 2)
    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.

    pygame.display.flip()

# Be IDLE friendly
pygame.quit()
