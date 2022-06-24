# from sika.task_bypass.stage import Stage
# stage = Stage({'from': 'somewhere'})
# stage.has_antecedent()

class Stage:
    def __init__(self, stage_dict):
        self.stage_dict = stage_dict

    def has_antecedent(self):
        return True if 'from' in self.stage_dict else False

    def antecedents(self):
        return self.stage_dict['from']

    def name(self):
        return self.stage_dict['id']

 
