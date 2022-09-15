
class Stages:
    def __init__(self, stages_list):
        self._stages_list = stages_list

    def names(self):
        return [ stage.name() for stage in self._stages_list ]

    def run(self, db):
        # Main stages loop - might be better way in the future (e.g. parallelisim)
        for stage in self._stages_list:

            done_stage = stage.run(db)

            # record done stage
            db.updatePipelineStatus(stage.name())
        
        # return last stage's data frame of results
        return list(done_stage.values())[0][0]