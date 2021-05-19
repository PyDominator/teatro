from math import pi, sin, cos
from direct.interval.FunctionInterval import HprInterval, PosInterval

from direct.task import Task
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

class teatro(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # cargando el modelo de entorno
        self.scene = self.loader.loadModel("models/environment")
        # reparentando el modelo de entorno y preparandome para renderizar
        self.scene.reparentTo(self.render)
        # aplicando escala y transformando el entorno para un posicionamiento geografico
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Agregando un proceso al administrador de tareas .
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # cargando y transformanda el actor panda 
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        # generando loop de animacion
        self.pandaActor.loop("walk")

        # creando los cuatro intervalos lerp necesarios para que el panda camine de un lado a otro
        PosInterval1 = self.pandaActor.posInterval(13, 
                                                    Point3(0, -10, 0),
                                                    startPos=Point3(0, 10, 0))
        posInterval2 = self.pandaActor.posInterval(13,
                                                    Point3(0, 10, 0),
                                                    startPos=Point3(0, -10, 0))
        HprInterval1 = self.pandaActor.hprInterval(3, 
                                                    Point3(180, 0, 0),
                                                    startHpr=Point3(0, 0, 0))
        HprInterval2 = self.pandaActor.hprInterval(3,
                                                    Point3(0, 0, 0),
                                                    startHpr=Point3(180, 0, 0))

        # creando y activando la secuencia de coordenadas de los intervalos
        self.pandaPace = Sequence(PosInterval1, HprInterval1,
                                   posInterval2, HprInterval2,
                                   name="pandaPace")
        self.pandaPace.loop()


    # definiendo el proceso de movimiento de camara 
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

duque = teatro()
duque.run()