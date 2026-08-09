from core.analyzer import Analyzer


class Forecaster:
    def __init__(self, analyzer: Analyzer, data, expected_data):
        self.analyzer = analyzer

    def what_if(self, expected_grades : list, expected_units : list) -> float:
        expected_gpa = self.analyzer.gpa(grades=expected_grades, units=expected_units)

        self.analyzer.cgpa()

    def next_target(self):
        ...

    def goal_seeker(self):
        ...