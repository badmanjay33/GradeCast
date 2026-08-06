import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Grading system
us = {
    "name": "American",
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "C-": 1.7,
    "D+": 1.3,
    "D": 1.0,
    "F": 0.0
}

nuc_ng = {
    'name': 'NUC Nigeria',
    'A': 5,
    'B': 4,
    'C': 3,
    'D': 2,
    'E': 1,
    'F': 0
               }
# Polytechnics as Regulated by National Board for Technical Education (NBTE)
# Some schools use {'D': 2.00, 'E': 1.50}
nbte_ng = {
    'name': 'NBTE Nigeria',
    'A': 4,
    'AB': 3.5,
    'B': 3.25,
    'BC': 3.00,
    'C': 2.75,
    'CD': 2.50,
    'D': 2.25,
    'E': 2.00,
    'F': 0.00
}


class Analyzer:
    def __init__(self, path : str ='test_grades.csv', grading_system : dict = us):
        self.df = pd.read_csv(path)
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

    def gpa_max(self):
        return list(self.__grading_system.values())[1]


class Forecaster(Analyzer):
    def what_if(self):
        ...


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


analyzer = Analyzer(path='test_grades.csv', grading_system=nuc_ng)
print(analyzer.cgpa())
print(analyzer.gpa('Fall 2024'))
gpa_visualiser(analyzer)
