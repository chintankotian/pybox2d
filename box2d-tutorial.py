from Box2D import *
import pygame 


def drawPolygon(window,bodies):
    window.fill((0,0,0))
    for body in bodies:
        # print(body)
        for fixture in body.fixtures:
            polygon = fixture.shape
            x,y = list(body.position)
            vertices=[(body.transform*v)*10 for v in polygon.vertices]
            vertices=[(v[0], v[1]) for v in vertices]

            
            pygame.draw.polygon(window, (255,255,255), vertices)
            pygame.display.update()

def drawCircle(window, circles):
    for circle in circles:
        for fixture in circle.fixtures:
            data = fixture.shape
            pos = circle.transform*data.pos*10
            pos = (int(pos[0]),int(pos[1]))
            rad = data.radius*10
            pygame.draw.circle(window,(255,255,255), pos, int(rad))
            pygame.display.update()

if __name__ == "__main__":
    print('in')
    pygame.init()
    # window = pygame.display.set_mode((500,500))
    clock = pygame.time.Clock()
    SCREEN_HEIGHT = 500
    SCREEN_WIDTH = 500
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    timeStep = 1.0 / 60
    vel_iters, pos_iters = 10, 10
    
    world = b2World(gravity=(0,10), doSleep=True)
    shapes = b2PolygonShape(vertices = [(1,1), (-1,1), (0.7,2)])  
    staticBody = world.CreateDynamicBody(
        position = (1,1) 
        )

    staticBody.CreateFixture(shape = shapes, density = 10, friction = 1)
    staticBody.CreateFixture(shape = b2PolygonShape(box = (1,1)), density = 1, friction = 1)

    shapes = b2CircleShape(radius = 4)
    dynamicBody = world.CreateStaticBody(
        position = (1,50),
        shapes = shapes
        )
    dynamicBody.CreateFixture(shape = shapes, density = 1, friction = 1)

    
    # print(dynamicBody.fixtures[0].shape)
    
    # dynamicBody.CreateFixture(shape = shapes ,density = 10, friction = 0.3)
    # dynamicBody
    run = True
    while run:
        for event in pygame.event.get():
            # print(event)
            if(event.type == pygame.QUIT):
                run = False
        
        clock.tick(120)
        drawPolygon(window,[staticBody])
        drawCircle(window, [dynamicBody])
        world.Step(timeStep,vel_iters,pos_iters)
        world.ClearForces()
        # print(dynamicBody.fixtures, dynamicBody.angle)