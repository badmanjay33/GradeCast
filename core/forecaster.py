from core.analyzer import Analyzer
from core.models import GradingSystem


class Forecaster:
    def __init__(self, analyzer: Analyzer, grading_system: GradingSystem):
        self.analyzer = analyzer
        self.grading_system = grading_system

    def what_if(self, expected_grades : list, expected_units : list) -> dict [str, float]:
        # Expected GPA
        expected_semester_gpa = self.analyzer.calculate(expected_grades, expected_units)

        # Expected CGPA
        # Calculate grade point
        cgpa = self.analyzer.cgpa()
        total_units = sum(self.analyzer.df['Units'].to_list())
        grade_points = cgpa * total_units


        expected_grade_points = sum(
            self.grading_system[g] * u
            for g, u in zip(expected_grades, expected_units)
        )
        total_expected_units = sum(expected_units)

        final_units = total_units + total_expected_units

        expected_cgpa = 0.0
        if final_units > 0:
            expected_cgpa = round((grade_points + expected_grade_points) / final_units, 2)

        return {
            "expected_gpa": expected_semester_gpa,
            "expected_cgpa": expected_cgpa
        }

    def next_target(self, expected_cgpa : float | int, expected_units : int) -> float | str:
        if not (0 <= expected_cgpa <= self.grading_system.max_gpa):
            raise ValueError(f'Expected CGPA {expected_cgpa} is not in range of your grading system: {0}, {self.grading_system.max_gpa}')

        current_units = sum(self.analyzer.df['Units'].to_list())
        cgpa = self.analyzer.cgpa()

        target_points = expected_cgpa * (current_units + expected_units)
        current_points = cgpa * current_units

        expected_gpa = round((target_points - current_points) / expected_units, 2)
        if expected_gpa > self.grading_system.max_gpa:
            return f'Not possible: You cannot achieve a CGPA of {expected_cgpa} with {expected_units}.\nTry taking more credits.'
        elif expected_gpa < 0:
            return f"Not possible: You cannot achieve this CGPA even if you failed all your classes.\nBut trying aiming some a CGPA higher than yours."
        else:
            return expected_gpa

    def goal_seeker(self):
        ...
        # tell it your remaining units and cgpa, and it tells you what you should get to reach an honor