from IPython import embed
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
    
    def get_unexecuted_stages(self, db):
        df = db.readTableToDf('_pipeline_status')
        done_stages = list(df['done_stage'])
        stage_names = self.names()
        unexecute_stage_names = [stage_name for stage_name in stage_names if stage_name not in done_stages]
        waited_stage_lists = [stage for stage in self._stages_list if stage.name() in unexecute_stage_names]
        return Stages(waited_stage_lists)