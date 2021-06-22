import random
import math
import pygame

#class for drawing map, obstacles and actual path calculated
class RRTMap:
    def __init__(self, start, goal, MapDimensions, obsdim, obsnum):
        self.start= start
        self.goal= goal
        self.MapDimensions= MapDimensions
        self.Maph,self.Mapw= self.MapDimensions

        #window settings
        self.MapWindowName='RRT path Planning'
        pygame.display.set_caption(self.MapWindowName)
        self.map=pygame.display.set_mode((self.Mapw,self.Maph))#for creating the canvas
        #white colour background
        self.map.fill((255,255,255))
        #variables for creating nodes and edges
        self.nodeRad= 2
        self.nodeThickness= 0
        self.edgeThickness= 1

        #list for storing obstacles
        self.obstacles=[]
        self.obsdim=obsdim
        self.obsNumber=obsnum

        #Colors
        self.grey = (70, 70, 70)
        self.Blue = (0, 0, 255)
        self.Green = (0, 255, 0)
        self.Red = (255, 0, 0)
        self.white = (255, 255, 255)

        
    def drawMap(self,obstacles):
        #draw start and goal postion as circles
        pygame.draw.circle(self.map,self.Green,self.start,self.nodeRad+5,0)#0is for a solid circle start point
        #for goal wider radius and thickess of 1 to draw a empty circle
        pygame.draw.circle(self.map,self.Green,self.start,self.nodeRad+20,1)#0is for a solid circle start point
        self.drawObs(obstacles)

    def drawPath(self):
        pass
    def drawObs(self,obstacles):
        obstaclesList=obstacles.copy() #temporary variable
        while (len(obstaclesList)>0):
            obstacle = obstaclesList.pop(0)
            pygame.draw.rect(self.map,self.grey,obstacle)


#making obstacles, add and remove nodes and edges from tree
#check collision, find the nearest neigbour
class RRTGraph:
    def __init__(self,start,goal,MapDimensions,obsdim,obsnum):
        (x,y)=start
        self.start=start
        self.goal=goal
        self.goalFlag=False
        self.maph,self.mapw=MapDimensions
        self.x=[]
        self.y=[]
        self.parent=[]

        # initialize the tree
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)

        # the obstacles
        self.obstacles=[]
        self.obsDim=obsdim
        self.obsNum=obsnum

        #path
        self.goalstate=None #flag indication whether tree reached goal or not
        self.path=[]
        

    def makeRandomRect(self):
        uppercornerx= int(random.uniform(0, self.mapw-self.obsDim))
        uppercornery= int(random.uniform(0, self.maph-self.obsDim))

        return (uppercornerx,uppercornery)

    def makeobs(self):
        #empty list for obstacles
        obs=[]

        for i in range(0,self.obsNum):
            rectang=None #temporarily holding the obstacle before storing
            startgoalcol=True #flag to check start and goal position inside obstacle
            while startgoalcol:
                #generate a random upper corner
                upper=self.makeRandomRect()
                #convert the upper corner into full rectangle object using pi game rect
                rectang=pygame.Rect(upper,(self.obsDim,self.obsDim))
                #rectang.collidepoint returns true if the point lies within the boundaries of the rectangle else false
                if rectang.collidepoint(self.start) or rectang.collidepoint(self.goal):
                    startgoalcol=True
                else:
                    startgoalcol=False
            obs.append(rectang)
        self.obstacles=obs.copy() #list is copied to class variable
        return obs

    def add_node(self, n, x, y):
        #n is the identification number of the node and its x and y coordinates
        self.x.insert(n, x)
        self.y.append(y)


    def remove_node(self,n):
        self.x.pop(n)
        self.y.pop(n)


    def add_edge(self, parent, child):
        #insert the parent of the child in the parent's list
        #child is stored as index parent is stored as element
        self.parent.insert(child, parent)


    def remove_edge(self, n):
        #n is index of child
        #we will cut the link between child and parent node
        self.parent.pop(n)

    def number_of_nodes(self):
        #total number of nodes=length of list
        return len(self.x)

    def distance(self, n1, n2):
        (x1,y1)=(self.x[n1],self.y[n1])
        (x2,y2)=(self.x[n2],self.y[n2])
        #calculate euclidean distance
        px=(float(x1)-float(x2))**2
        py=(float(y1)-float(y2))**2
        return (px+py)**(0.5)

    #to generate random samples from the map
    def sample_envir(self):
        x=int(random.uniform(0, self.mapw))
        y=int(random.uniform(0, self.maph))
        return x, y

    def nearest(self):
        pass
    #check if the newly added node to the tree is located in free space or not
    def isFree(self):
        n=self.number_of_nodes()-1 #last node id
        #extract the x and y co-ordinates of the node
        (x, y)=(self.x[n], self.y[n])
        obs=self.obstacles.copy()#temprary list for obstacles
        while len(obs)>0:
            rectang=obs.pop(0)
            if rectang.collidepoint(x,y):
                self.remove_node(n)
                return False
        return True
       
    #to check connection between two nodes crosses any obstacles
    def crossObstacle(self, x1, x2, y1, y2):
        obs=self.obstacles.copy()
        while(len(obs) > 0):
            rectang=obs.pop(0)
            #create interpolation between two nodes and check 
            ## any of them collide with the obstacle
            for i in range(0, 101):
                u=i / 100 #to generate checkpoints
                #generate x and y co=ordinates of ith checkpoint
                x = x1 * u + x2 * (1-u)
                y=y1 * u + y2 * (1-u)
                if rectang.collidepoint(x, y):
                    return True
        return False 

    def connect(self, n1, n2):
        (x1, y1)=(self.x[n1], self.y[n1])
        (x2, y2)=(self.x[n2], self.y[n2])
        if self.crossObstacle(x1, x2, y1, y2):
            self.remove_node(n2)
            return False
        else:
            self.add_edge(n1, n2) #n1 is parent n2 is child
            return True               

    def step(self):
        pass

    def path_to_goal(self):
        pass

    def getPathCoords(self):
        pass

    def bias(self):
        pass

    def expand(self):
        pass

    def cost(self):
        pass




