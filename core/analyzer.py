import pandas as pd
from core.models import GradingSystem


class Analyzer:
    def __init__(self, data : pd.DataFrame , grading_system : GradingSystem):
        self.df = data
        self.__grading_system = grading_system
        self.semesters = self.df['Semester'].unique()

        self.semesters_data = {}
        for sem in self.semesters:
            self.semesters_data[sem] = self.df[self.df['Semester'] == sem]

    def cgpa(self):
        grades = self.df['Grade'].to_list()
        units = self.df['Units'].to_list()
        return self.calculate(grades, units)

    def gpa(self, semester: str) -> float:
        grades = self.semesters_data[semester]['Grade'].to_list()
        units = self.semesters_data[semester]['Units'].to_list()
        return self.calculate(grades, units)

    def calculate(self, grades, units) -> float:
        i = 0
        total_unit = 0
        grade_point = 0
        while i < len(grades):
            grade_point += self.__grading_system[grades[i]] * units[i]
            total_unit += units[i]
            i += 1
        return round(grade_point/total_unit, 2)

    def all_gpas(self):
        gpas = []
        for sem in self.semesters:
            gpas.append(self.gpa(sem))
        return gpas
