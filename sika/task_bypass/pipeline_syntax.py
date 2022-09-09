class PipelineSyntax:
    def __init__(self, syntax):
        self.syntax = syntax

    def pipeline(self):
        return self.syntax['pipeline']

    def stages(self):
        stages_syntax = StagesSyntax.new(self.pipeline()['stages'])
        return stages_syntax.build_entity()

    def name(self):
        return self.syntax['name']

    def build_entity():
        Pipeline.new(self.name(), self.stages())