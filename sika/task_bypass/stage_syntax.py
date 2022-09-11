class StageSyntax:
    def __init__(self, syntax):
        self.syntax = syntax

    def name(self):
        return self.syntax['id']

    def build_entity(self):
        return Stage.new(self.syntax)