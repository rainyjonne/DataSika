from sika.task_bypass.stages_syntax import StagesSyntax
from sika.task_bypass.pipeline import Pipeline

class PipelineSyntax:
    def __init__(self, syntax):
        self.syntax = syntax

    def pipeline(self):
        return self.syntax['pipeline']

    def stages(self):
        stages_syntax = StagesSyntax(self.pipeline()['stages'])
        return stages_syntax.build_entity()

    def name(self):
        return self.syntax['name']

    def build_entity(self):
        return Pipeline(self.name(), self.stages())