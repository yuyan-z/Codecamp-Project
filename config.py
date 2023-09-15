class Config:
    def __init__(self):
        self.sub_attrs = [
            'project',
            'state',
            'priority',
            'context',
            'tag',
            'user',
            'start_time',
            'deadline',
            'estimated_duration',
            'actual_duration',
            'recurring',
        ]

        self.choices = {
            'state': ['started', 'suspended','completed','cancelled', ''],
            'user': ['yuyan', 'oumaya', 'felipe'],
        }

        self.helps = {
            'start_time': '(DD/MM/YYYY hh:mm)',
            'deadline': '(DD/MM/YYYY hh:mm)',
            'estimated_duration': '(* min/h/d/w/m/y)',
            'actual_duration': '(* min/h/d/w/m/y)',
            'recurring': '(* min/h/d/w/m/y)',
        }

