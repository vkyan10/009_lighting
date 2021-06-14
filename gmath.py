import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represented as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    normalize(normal)
    normalize(view)
    normalize(light[LOCATION])

    Ia = calculate_ambient(ambient, areflect)
    Id = calculate_diffuse(light, dreflect, normal)
    Is = calculate_specular(light, sreflect, view, normal)

    I = [0,0,0]
    for i in range(3):
        I[i] = Ia[i] + Id[i] + Is[i]
    return limit_color(I)

def calculate_ambient(alight, areflect):
    answer = [0,0,0]
    for i in range(3):
        answer[i] = alight[i] * areflect[i]
    return limit_color(answer)

def calculate_diffuse(light, dreflect, normal):
    answer = [0,0,0]
    costheta = dot_product(normal, light[LOCATION])
    for i in range(3):
        answer[i] = light[COLOR][i] * dreflect[i] * costheta
    return limit_color(answer)

def calculate_specular(light, sreflect, view, normal):
    answer = [0,0,0]

    costheta = dot_product(normal, light[LOCATION])
    # tvector = normal * dot_product(normal, light[LOCATION])
    # svector = tvector - light[LOCATION]
    # rhat = tvector + svector
    for i in range(3):
        answer[i] = 2 * normal[i] * costheta - light[LOCATION][i]
    cosalpha = max(0, dot_product(answer, view)) ** SPECULAR_EXP
    for i in range(3):
        answer[i] = light[COLOR][i] * sreflect[i] * cosalpha

    return limit_color(answer)


def limit_color(color):
    for i in range(3):
        if color[i] > 255:
            color[i] = 255
        if color[i] < 0:
            color[i] = 0
        color[i] = int(color[i])
    return color

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
