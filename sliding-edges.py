from Box2D import *
import pygame
from pygame.locals import *
import time
import os
from createBoundary import createBoundary

def drawPolygon(window, bodies):
    window.fill((0,0,0))
    for body in bodies:
        for fixture in body.fixtures:
            polygon = fixture.shape
            vertices = [(body.transform*v)*ppm for v in polygon.vertices]
            vertices = [(v[0],v[1]) for v in vertices]
            pygame.draw.polygon(window,(255,255,255),vertices)
            pygame.display.update()



if __name__ == "__main__":
    SCREEN_HEIGHT = 700
    SCREEN_WIDTH = 500
    ppm = 10
    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Edge sliding')
    clock = pygame.time.Clock()
    
    pixel_to_meter = lambda x : x*ppm
    meter_to_pixel = lambda x : x/ppm

    #BOX2D params
    iter_time = 1.0/60
    vel_iter, pos_iter = 6,2

    world =  b2World(gravity = (0,10), doSleep = True)

    createBoundary(world=world,SCREEN_HEIGHT = SCREEN_HEIGHT, SCREEN_WIDTH=SCREEN_WIDTH,ppm=ppm)
    
    # top box
   

    top_triangle = world.CreateStaticBody(
            position = (1, meter_to_pixel(150))
            )
    top_triangle.CreatePolygonFixture(vertices = [(0,-10), (0,10), (20,12)], density =  1, friction = 0.9)

    top_triangle = world.CreateStaticBody(
            position = (meter_to_pixel(SCREEN_WIDTH -1), meter_to_pixel(SCREEN_WIDTH -150))
            )
    top_triangle.CreatePolygonFixture(vertices = [(0,10), (0,-10), (-20,12)], density =  1, friction = 0.9)


    sensor = b2FixtureDef(shape = b2PolygonShape(box=(1,1)), density = 1, friction = 1, restitution = 1,isSensor = True)
    box = b2FixtureDef(shape = b2PolygonShape(box=(1,1)), density = 1, friction = 1, restitution = 1,filter = b2Filter(groupIndex = -1,categoryBits = 0x0002))
    
    box2 = b2FixtureDef(shape = b2PolygonShape(box=(1,1)), density = 1, friction = 1, restitution = 1,filter = b2Filter(groupIndex = -10,categoryBits = 0x0004,))
    box1 = b2FixtureDef(shape = b2PolygonShape(box=(1,1)), density = 1, friction = 1, restitution = 1,filter = b2Filter(groupIndex = -2,categoryBits = 0x0006, maskBits = 0xFFFF & (~0x0002 & ~0x0004)))
    test_box = world.CreateDynamicBody(
            position = (2,3),
        #     shapes = b2PolygonShape(box=(1,1)),
            angle = 0,
            fixtures = [box,sensor],
            allowSleep = True,
        #     fixedRotation = True,
            active = True

            )
#     test_box.CreatePolygonFixture(box = (1,1), density = 1, friction = 1, restitution =1,groupIndex = -1)
   
    test_box_1 = world.CreateDynamicBody(
            position = (20,3),
            angle = 0,
            fixtures = box1,
            )
#     test_box.CreatePolygonFixture(box = (1,1), density = 1, friction = 1, restitution =0.5,groupIndex = -1)

    test_box_2 = world.CreateDynamicBody(
            position = (2,3),
            fixtures = box2,
            angle = 0
            )
    joint = world.CreateDistanceJoint(
        bodyA = test_box_1,
        bodyB = test_box_2,
        anchorA = test_box_1.worldCenter,
        anchorB = test_box_2.worldCenter,
        frequencyHz = 2,
        dampingRatio = 0.4,
        collideConnected = True
        )
    print(test_box_1.worldCenter)
#     test_box.CreatePolygonFixture(box = (1,1), density = 1, friction = 1, restitution =0.5)

#     test_box = world.CreateDynamicBody(
#             position = (11,1),
#             shapes = b2PolygonShape(box=(1,1)),
#             angle = 0
#             )
#     test_box.CreatePolygonFixture(box = (1,1), density = 1, friction = 1, restitution =0.5)
    # test_box.CreatePolygonFixture1(position = (1,1),box = (1,1), density = 1, friction = 1)

    run = True
    while run:
        # time.sleep(1./240)
        for event in pygame.event.get():
            # print(event)
            if(event.type == pygame.QUIT):
                run = False
        drawPolygon(window,world.bodies)
        world.Step(iter_time,vel_iter,pos_iter)
        # world.ClearForces()
        clock.tick(60)
        # if len(world.contacts) > 0:
        #         data = list(world.contacts)
        #         body_pairs = [(p['fixtureA'].body, p['fixtureB'].body) for p in world.contacts]




