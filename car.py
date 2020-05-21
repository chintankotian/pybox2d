import pygame
from  Box2D import *
from createBoundary import createBoundary, drawCircle, drawPolygon




class Car():
    def __init__(self,world,carBodyWidth,carBodyHeight,carX,carY,tireRad,SCREEN_WIDTH,SCREEN_HEIGHT):
        self.world = world
        self.carBodyWidth = carBodyWidth
        self.carBodyHeight =carBodyHeight
        self.carX = carX
        self.carY =  carY
        self.tireRad = tireRad
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        # self.build()

        # BUILDIG CAR BODY
    def build(self):
        carBodyFix = b2FixtureDef(
            shape = b2PolygonShape(box = (self.carBodyWidth,self.carBodyHeight)),
            friction = 1,
            density = 1,
            # restitution = 1.0,
            # massData = 100
            )

        carBody = self.world.CreateDynamicBody(
            position = (self.carX, self.carY ),
            fixtures = carBodyFix,
            # angle = 1
            # massData = 100
            )
        # carBody.mass = 500.0
        tireFix = b2FixtureDef(
            shape = b2CircleShape(radius = self.tireRad),
            friction = 1,
            density = 0.7,
            # restitution = 1.0
            )

        tire1 = world.CreateDynamicBody(
            position = ((self.carX - self.carBodyWidth - self.tireRad - 1),(self.carY - self.carBodyHeight - self.tireRad - 1)),
            fixtures = tireFix
            )
        
        tire2 = world.CreateDynamicBody(
            position = ((self.carX + self.carBodyWidth + self.tireRad + 1),(self.carY - self.carBodyHeight - self.tireRad - 1)),
            fixtures = tireFix
            )

        pj1 = self.world.CreateWheelJoint(
            bodyA = carBody,
            bodyB = tire1,
            anchor = tire1.position,
            axis = (0,1),
            # lowerTranslation = 1.0,
            # upperTranslation = -0.1,
            # enableLimit=True,
            # damping = 0.7,
            # frquency = 2,
            maxMotorTorque = 100.9,
            motorSpeed = -100.0,
            enableMotor = True,
            frequencyHz = 6,
            dampingRatio = 0.7
            # translation = 1
            )
        pj2 = self.world.CreateWheelJoint(
            bodyA = carBody,
            bodyB = tire2,
            anchor = tire2.position,
            axis = (0,1),
            maxMotorTorque = 10.0,
            motorSpeed = 0.0,
            enableMotor = True,
            frequencyHz = 6,
            dampingRatio = 0.7
            )
        # top_triangle = world.CreateStaticBody(
        #     position = (1,400/ppm)
        #     )
        # top_triangle.CreatePolygonFixture(vertices = [(0,-10), (0,10), (20,12)], density =  1, friction = 0.9)

        test_box1Fix = b2FixtureDef(
            shape = b2PolygonShape(box = (1,2)),
            friction = 1,
            density = 1,
            restitution = 1.0
            )
        test_box1 = world.CreateStaticBody(
            position = ((SCREEN_WIDTH/2)/ppm,(SCREEN_HEIGHT - (SCREEN_HEIGHT/2))/ppm),
            fixtures = test_box1Fix
            )

        test_box1Fix = b2FixtureDef(
            shape = b2PolygonShape(box = (4,1)),
            friction = 1,
            density = 1,
            # restitution = 1.0

            )

        test_box2 = world.CreateDynamicBody(
            position = ((SCREEN_WIDTH/2)/ppm,(SCREEN_HEIGHT - (SCREEN_HEIGHT/2 - 40))/ppm),
            fixtures = test_box1Fix
            )
        
        # pj2 = world.CreatePrismaticJoint(
        #     bodyA = test_box1,
        #     bodyB = test_box2,
        #     axis = (0,-1),
        #     upperTranslation = -10.0,
        #     lowerTranslation = 4.0,
        #     enableLimit = True,
        #     anchor = test_box1.worldCenter,
        #     enableMotor = True,
        #     motorSpeed = 1.0,
        #     maxMotorForce = 0.1,
        #     )
        

        return [[carBody,test_box1,test_box2],[tire1,tire2],[pj1,pj2]]


class PygameDraw(b2DrawExtended):
    """
    This debug draw class accepts callbacks from Box2D (which specifies what to
    draw) and handles all of the rendering.

    If you are writing your own game, you likely will not want to use debug
    drawing.  Debug drawing, as its name implies, is for debugging.
    """
    surface = None
    axisScale = 10.0

    def __init__(self, test=None, **kwargs):
        b2DrawExtended.__init__(self, **kwargs)
        self.flipX = False
        self.flipY = True
        self.convertVertices = True
        self.test = test

    def StartDraw(self):
        print('hello')
        self.zoom = self.test.viewZoom
        self.center = self.test.viewCenter
        self.offset = self.test.viewOffset
        self.screenSize = self.test.screenSize

    def EndDraw(self):
        pass

    def DrawPoint(self, p, size, color):
        """
        Draw a single point at point p given a pixel size and color.
        """
        self.DrawCircle(p, size / self.zoom, color, drawwidth=0)

    def DrawAABB(self, aabb, color):
        """
        Draw a wireframe around the AABB with the given color.
        """
        points = [(aabb.lowerBound.x, aabb.lowerBound.y),
                  (aabb.upperBound.x, aabb.lowerBound.y),
                  (aabb.upperBound.x, aabb.upperBound.y),
                  (aabb.lowerBound.x, aabb.upperBound.y)]

        pygame.draw.aalines(self.surface, color, True, points)

    def DrawSegment(self, p1, p2, color):
        """
        Draw the line segment from p1-p2 with the specified color.
        """
        pygame.draw.aaline(self.surface, color.bytes, p1, p2)

    def DrawTransform(self, xf):
        """
        Draw the transform xf on the screen
        """
        p1 = xf.position
        p2 = self.to_screen(p1 + self.axisScale * xf.R.x_axis)
        p3 = self.to_screen(p1 + self.axisScale * xf.R.y_axis)
        p1 = self.to_screen(p1)
        pygame.draw.aaline(self.surface, (255, 0, 0), p1, p2)
        pygame.draw.aaline(self.surface, (0, 255, 0), p1, p3)

    def DrawCircle(self, center, radius, color, drawwidth=1):
        """
        Draw a wireframe circle given the center, radius, axis of orientation
        and color.
        """
        radius *= self.zoom
        if radius < 1:
            radius = 1
        else:
            radius = int(radius)

        pygame.draw.circle(self.surface, color.bytes,
                           center, radius, drawwidth)

    def DrawSolidCircle(self, center, radius, axis, color):
        """
        Draw a solid circle given the center, radius, axis of orientation and
        color.
        """
        radius *= self.zoom
        if radius < 1:
            radius = 1
        else:
            radius = int(radius)

        pygame.draw.circle(self.surface, (color / 2).bytes + [127],
                           center, radius, 0)
        pygame.draw.circle(self.surface, color.bytes, center, radius, 1)
        pygame.draw.aaline(self.surface, (255, 0, 0), center,
                           (center[0] - radius * axis[0],
                            center[1] + radius * axis[1]))

    def DrawPolygon(self, vertices, color):
        """
        Draw a wireframe polygon given the screen vertices with the specified color.
        """
        if not vertices:
            return

        if len(vertices) == 2:
            pygame.draw.aaline(self.surface, color.bytes,
                               vertices[0], vertices)
        else:
            pygame.draw.polygon(self.surface, color.bytes, vertices, 1)

    def DrawSolidPolygon(self, vertices, color):
        """
        Draw a filled polygon given the screen vertices with the specified color.
        """
        if not vertices:
            return

        if len(vertices) == 2:
            pygame.draw.aaline(self.surface, color.bytes,
                               vertices[0], vertices[1])
        else:
            pygame.draw.polygon(
                self.surface, (color / 2).bytes + [127], vertices, 0)
            pygame.draw.polygon(self.surface, color.bytes, vertices, 1)

    # the to_screen conversions are done in C with b2DrawExtended, leading to
    # an increase in fps.
    # You can also use the base b2Draw and implement these yourself, as the
    # b2DrawExtended is implemented:
    # def to_screen(self, point):
    #     """
    #     Convert from world to screen coordinates.
    #     In the class instance, we store a zoom factor, an offset indicating where
    #     the view extents start at, and the screen size (in pixels).
    #     """
    #     x=(point.x * self.zoom)-self.offset.x
    #     if self.flipX:
    #         x = self.screenSize.x - x
    #     y=(point.y * self.zoom)-self.offset.y
    #     if self.flipY:
    #         y = self.screenSize.y-y
    #     return (x, y)



if __name__ == "__main__":
   
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 500
    ppm = 1
    polygons = []
    circles = []
    
    iter_time = 1./60
    pos_iters = 1
    vel_iters = 1

    class myContactListener(b2ContactListener):
        def __init__(self):
            b2ContactListener.__init__(self)

        def BeginContact(self,contact):
            # print(contact)
            pass



    # draw = MyDraw()
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption('car')
    
    world = b2World(gravity = (0,-10), doSleep = True,contactListener = myContactListener())
    world.renderer = PygameDraw(surface=window)
    # print(x)
    polygons += createBoundary(world=world, SCREEN_HEIGHT=SCREEN_HEIGHT,SCREEN_WIDTH=SCREEN_WIDTH,ppm=ppm)
    # BOX BODIES
    
    carBody,tires,joints = Car(world,4,2,15,20,3,SCREEN_WIDTH,SCREEN_HEIGHT).build()
    polygons += carBody
    # print(len(carBody))
    circles += tires
    # print(circles[0].position)
    # print(circles[1].position)

    run = not False

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False

        keys = pygame.key.get_pressed()
        if(keys[pygame.K_SPACE]):
            # print('speed')\
            # for joint in joints:
            joints[0].motorSpeed += 10.0 * ppm
            # print(joints[0].motorSpeed)
        
        if(keys[pygame.K_LEFT]):
            # print('speed')
            # for joint in joints:
            joints[0].motorSpeed -= 10.0 * ppm
            # print(joints[0].motorSpeed)
        
            
        # for joint in joints:
        #     # print(joint)
        #     joint.motorForce = 10.0
        world.Step(iter_time,vel_iters,pos_iters)
        drawPolygon(window,polygons,SCREEN_HEIGHT)
        drawCircle(window, circles,SCREEN_HEIGHT)
        pygame.display.flip()
        # world.renderer.StartDraw()
        # print(world.DrawDebugData())


    