class StagesSyntax:
    def __init__(self, syntax):
        self.syntax = syntax
        self.stages_syntax = [ StageSyntax.new(stage_syntax) for stage_syntax in self.syntax ]

    def names(self):
        return [ stage.name for stage in self.stages_syntax ]

    def build_entity():
        stages_array = [ stage_syntax.build_entity() for stage_syntax in self.stages_syntax ]
        Stages.new(stages_array)