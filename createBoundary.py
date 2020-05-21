from Box2D import *
import pygame


def createBoundary(world,SCREEN_HEIGHT, SCREEN_WIDTH,ppm = 20):
    pixel_to_meter = lambda x : x*ppm
    meter_to_pixel = lambda x : x/ppm

    fixture = b2FixtureDef(
        friction = 1,
        shape = b2PolygonShape(box=(meter_to_pixel(SCREEN_WIDTH/2),1))
        )
    top_box = world.CreateStaticBody(
        position = (meter_to_pixel(SCREEN_WIDTH/2), meter_to_pixel(0)),
        shapes = b2PolygonShape(box=(meter_to_pixel(SCREEN_WIDTH/2),1)),
        fixtures = fixture
        )
    fixture = b2FixtureDef(
        friction = 1,
        shape = b2PolygonShape(box=(meter_to_pixel(SCREEN_WIDTH/2),1))
        )
    bottom_box = world.CreateStaticBody(
            position = (meter_to_pixel(SCREEN_WIDTH/2), meter_to_pixel(SCREEN_HEIGHT)),
            shapes = b2PolygonShape(box=(meter_to_pixel(SCREEN_WIDTH/2),1)),
            fixtures = fixture
            )
    fixture = b2FixtureDef(
        friction = 1,
        shape = b2PolygonShape(box=(1, meter_to_pixel(SCREEN_HEIGHT/2)))
        )
    right_box = world.CreateStaticBody(
            position = (meter_to_pixel(SCREEN_WIDTH), meter_to_pixel(SCREEN_HEIGHT/2)),
            shapes = b2PolygonShape(box=(1, meter_to_pixel(SCREEN_HEIGHT/2))),
            fixtures = fixture
            )
    left_box = world.CreateStaticBody(
            position = (meter_to_pixel(0), meter_to_pixel(SCREEN_HEIGHT/2)),
            shapes = b2PolygonShape(box=(1, meter_to_pixel(SCREEN_HEIGHT/2))),
            fixtures = fixture
            )

    return [right_box,left_box,top_box,bottom_box]


def drawPolygon(window,bodies,SCREEN_HEIGHT):
    window.fill((0,0,0))
    for body in bodies:
        # print(body)
        for fixture in body.fixtures:
            polygon = fixture.shape
            x,y = list(body.position)
            vertices=[(body.transform*v)*10 for v in polygon.vertices]
            vertices=[(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
            pygame.draw.polygon(window, (255,255,255), vertices)
    # pygame.display.update()

def drawCircle(window, circles,SCREEN_HEIGHT):
    for circle in circles:
        for fixture in circle.fixtures:
            data = fixture.shape
            pos = circle.transform*data.pos*10
            pos = (int(pos[0]),SCREEN_HEIGHT - int(pos[1]))
            rad = data.radius*10
            pygame.draw.circle(window,(255,255,255), pos, int(rad))
    # pygame.display.update()