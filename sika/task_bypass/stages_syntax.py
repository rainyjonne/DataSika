from sika.task_bypass.stage_syntax import StageSyntax
from sika.task_bypass.stages import Stages

class StagesSyntax:
    def __init__(self, syntax):
        self.syntax = syntax
        self.stages_syntax = [ StageSyntax(stage_syntax) for stage_syntax in self.syntax ]

    def names(self):
        return [ stage.name for stage in self.stages_syntax ]

    def build_entity(self):
        stages_array = [ stage_syntax.build_entity() for stage_syntax in self.stages_syntax ]
        return Stages(stages_array)