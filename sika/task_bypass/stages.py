
class Stages:
    def __init__(self, stages):
        self.stages = stages

    def names(self):
        return [ stage.name() for stage in self.stages ]
        