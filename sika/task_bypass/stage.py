from sika.task_bypass.allocate_stage_tasks import allocate_stage_tasks

# from sika.task_bypass.stage import Stage
# stage = Stage({'from': 'somewhere'})
# stage.has_antecedent()

class Stage:
    def __init__(self, stage_dict):
        self.stage_dict = stage_dict

    # TODO: Refactor to make a stage data mapper for Yaml --> Stage object

    def has_antecedent(self):
        return True if 'from' in self.stage_dict else False

    # TODO: Refactor to return a List of Stage objects
    def antecedents(self):
        return self.stage_dict['from']

    def name(self):
        return self.stage_dict['id']

    # execute any particular stage
    def run(self, db):
        # TODO NEXT: Refactor make allocate stage tasks an instance method?
        # TODO: Refactor done_stage either as an object of its own or have methods to inspect it
        done_stage = allocate_stage_tasks(self.stage_dict, db)
        # save output data dataframe to sqlite db
        list(done_stage.values())[0][0].to_sql(name=self.name(), con=db.returnConnection())
        # update the done stage list
        return done_stage


 
