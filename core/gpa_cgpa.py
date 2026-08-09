import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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

    @property
    def grading_system(self) -> str:
        return str(self.__grading_system['name'])

    @grading_system.setter
    def grading_system(self, grading_system):
        self.__grading_system = grading_system

    def all_gpas(self):
        gpas = []
        for sem in self.semesters:
            gpas.append(self.gpa(sem))
        return gpas



class Forecaster(Analyzer):
    def what_if(self, *expected_grades):
        cgpa = self.cgpa()


def gpa_visualiser(analyzer: Analyzer):
    gpas = analyzer.all_gpas()
    semesters = analyzer.semesters
    if len(semesters) < 2:
        print('Cannot visualise GPA trend with only one semester')
    else:
        sns.lineplot(x=semesters, y=gpas, marker='o', label='GPA')
        for x_val, y_val in zip(semesters, gpas):
            plt.text(x_val, y_val - 0.15, f'{y_val:.2f}',
                 ha='center', va='top', color='tab:blue', fontweight='bold')

        plt.ylim(0, analyzer.gpa_max())
        print(gpas)
        plt.legend(loc='lower right')
        plt.title("GPA Trend")
        plt.xlabel("Semester")
        plt.ylabel("Cumulative GPA")
        plt.show()

