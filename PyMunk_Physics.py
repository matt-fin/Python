import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()

WIDTH, HEIGHT = 1000, 800
window = pygame. display. set_mode((WIDTH, HEIGHT))

def calculate_distance(p1, p2):
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

def calculate_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0]) #gives you the value in radians of the angle between your mouse and the ball


def draw(space, window, draw_options, line) : #this allows the game to draw over the screen
    window.fill("white")

    if line:
        pygame.draw.line(window, "black", line[0], line[1], 3)
        
    space.debug_draw(draw_options)
    pygame.display.update()

def create_boundaries(space, width, height): #creates my boundaries
    rects = [
        [(width/2, height - 10), (width, 20)],
        [(width/2, 10), (width, 20)],
        [(10, height/2), (20, height)],
        [(width-10, height/2), (20, height)],
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.8
        shape.friction = 0.4
        space.add(body, shape)

def create_structure(space, width, height):
    BROWN = (139, 69, 19, 100)
    rects = [
        [(600, height-120), (40, 200), BROWN, 75],
        [(900, height-120), (40, 200), BROWN, 75],
        [(750, height-240), (340, 40), BROWN, 100],
        [(860, height-340), (40, 200), BROWN, 75],
        [(650, height-340), (40, 200), BROWN, 75],
        [(750, height-450), (300, 40), BROWN, 100],
        [(750, height-550), (40, 200), BROWN, 75]

    ]
    

    for pos, size, color, mass in rects:
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Poly.create_box(body, size, radius = 1)
        shape.mass = mass
        shape.color = color
        shape.elasticity = 0.4
        shape.friction = 0.3
        space.add(body, shape)
    
def create_ball(space, radius, mass, pos): #creates by ball object
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.elasticity = 0.9
    shape.friction = 0.3
    shape.color = (255, 0, 0, 100)
    space.add(body, shape)
    return shape
    
def run(window, width, height):
    run = True
    clock = pygame.time.Clock() #set tick speed
    fps = 60
    dt = 1 / fps #delta time, lets me know what is going on in units of time in relation with fps
    space = pymunk.Space()
    space.gravity = (0, 981)

    #ball = create_ball(space, 30, 10)
    create_boundaries(space, width, height)
    create_structure(space, width, height)
    
    draw_options = pymunk.pygame_util.DrawOptions(window)

    pressed_pos = None
    ball = None
    
    while run:
        line = None
        if ball and pressed_pos:
            
            line = [pressed_pos, pygame.mouse.get_pos()]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not ball:
                    
                    pressed_pos = pygame.mouse.get_pos()
                    ball = create_ball (space, 30, 10, pressed_pos)

                elif pressed_pos:
                    ball.body.body_type = pymunk.Body.DYNAMIC
                    angle = calculate_angle(*line)
                    force = calculate_distance(*line) * 65
                    fx = math.cos(angle) * force
                    fy = math.sin(angle) * force
                    ball.body.apply_impulse_at_local_point((fx, fy), (0,0))
                    pressed_pos = None
                else:
                    space.remove(ball, ball.body)
                    ball = None

                    
                
        draw(space, window, draw_options, line)
        space.step(dt)
        clock.tick(fps)

    pygame.quit()
        
if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)

# ended the YT video and my progress on this at 35:50
# https://www.youtube.com/watch?v=tLsi2DeUsak&t=616s
