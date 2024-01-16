from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

class Circle:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.radius = 5.0

def circle_points(x, y, cx, cy):
    glVertex2f(x + cx, y + cy)
    glVertex2f(y + cx, x + cy)
    glVertex2f(y + cx, -x + cy)
    glVertex2f(x + cx, -y + cy)
    glVertex2f(-x + cx, -y + cy)
    glVertex2f(-y + cx, -x + cy)
    glVertex2f(-y + cx, x + cy)
    glVertex2f(-x + cx, y + cy)

def draw_circle(circle):
    glBegin(GL_POINTS)
    x, y = 0, int(circle.radius)
    d = 1 - circle.radius
    while x <= y:
        circle_points(x, y, circle.cx, circle.cy)
        x += 1
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
    glEnd()

def initialize():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, WINDOW_WIDTH, 0.0, WINDOW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def show_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(0.447, -1.0, 0.973)
    glPointSize(2)
    
    for circle in circles:
        draw_circle(circle)

    glutSwapBuffers()

def mouse_click(button, state, x, y):
    global is_paused
    if not is_paused and button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        circles.append(Circle(x, WINDOW_HEIGHT - y))

def update_circles():
    global circles
    new_circles = []
    for circle in circles:
        circle.radius += growth_speed
        if (
            circle.cx - circle.radius >= 0
            and circle.cx + circle.radius <= WINDOW_WIDTH
            and circle.cy - circle.radius >= 0
            and circle.cy + circle.radius <= WINDOW_HEIGHT
        ):
            new_circles.append(circle)
    circles = new_circles

def timer(_):
    if not is_paused:
        update_circles()
        glutPostRedisplay()
    glutTimerFunc(16, timer, 0)

def special_keyboard(key, x, y):
    global is_paused, growth_speed
    if key == GLUT_KEY_LEFT:
        growth_speed += 1.0
    elif key == GLUT_KEY_RIGHT:
        growth_speed = max(1.0, growth_speed - 1.0)

def keyboard(key, x, y):
    global is_paused
    if key == b"\033":  # Escape key
        sys.exit()
    elif key == b" ":
        is_paused = not is_paused

if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Circles")
    glutDisplayFunc(show_screen)
    glutMouseFunc(mouse_click)
    glutTimerFunc(0, timer, 0)
    glutSpecialFunc(special_keyboard)
    glutKeyboardFunc(keyboard)
    initialize()
    circles = []
    is_paused = False
    growth_speed = 1.0
    glutMainLoop()

