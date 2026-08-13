from core.analyzer import Analyzer
from core.models import GradingSystem
from core.visualiser import visualiser
from core.ai_insights import prompt

class Forecaster:
    def __init__(self, analyzer: Analyzer, grading_system: GradingSystem):
        self.analyzer = analyzer
        self.grading_system = grading_system

    def what_if(self, expected_grades : list, expected_units : list, visualise: bool = False) -> dict [str, float]:
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

        result = {
            "expected_gpa": expected_semester_gpa,
            "expected_cgpa": expected_cgpa
        }

        if visualise:
            visualiser(analyzer=self.analyzer, gp_max=self.grading_system.max_gpa, predictions=result)

        return result

    def next_target(self, expected_cgpa : float | int, expected_units : int, visualise: bool = False) -> float | str:
        if not (0 <= expected_cgpa <= self.grading_system.max_gpa):
            raise ValueError(f'Expected CGPA {expected_cgpa} is not in range of your grading system: {0}, {self.grading_system.max_gpa}')

        current_units = sum(self.analyzer.df['Units'].to_list())
        cgpa = self.analyzer.cgpa()

        target_points = expected_cgpa * (current_units + expected_units)
        current_points = cgpa * current_units

        expected_gpa = round((target_points - current_points) / expected_units, 2)

        if visualise:
            visualiser(analyzer=self.analyzer, gp_max=self.grading_system.max_gpa,
                       predictions={
                            "expected_gpa": expected_gpa,
                            "expected_cgpa": expected_cgpa
                       }
            )

        if expected_gpa > self.grading_system.max_gpa:
            return f'Not possible: You cannot achieve a CGPA of {expected_cgpa} with {expected_units}.\nTry taking more credits.'
        elif expected_gpa < 0:
            return f"Not possible: You cannot achieve this CGPA even if you failed all your classes.\nBut trying aiming some a CGPA higher than yours."
        else:
            return expected_gpa

    def goal_seeker(self, remaining_units: int, honour: str, semester_honours: str = None) -> str:
        # 1. Fetch current stats
        cgpa = self.analyzer.cgpa()
        current_units = sum(self.analyzer.df['Units'].to_list())
        max_system_gpa = self.grading_system.max_gpa

        # 2. Get the target thresholds
        honor_data = self.grading_system.graduation_honours.get(honour)
        if not honor_data:
            raise ValueError(f"Honor '{honour}' not found in the grading system.")
        target_cgpa = honor_data['min']

        # 3. Calculate the required GPA
        current_points = cgpa * current_units
        target_total_points = target_cgpa * (current_units + remaining_units)
        required_gpa = round((target_total_points - current_points) / remaining_units, 2)


        prompt_ = f"""
        [System Role]
        You are an insightful, highly analytical, and encouraging academic advisor. Your tone is professional and realistic.

        [Student Data]
        - Current CGPA: {cgpa:.2f}
        - Completed Units: {current_units}
        - Remaining Units: {remaining_units}

        [Student's Goal]
        - Target Graduation Honor: {honour}
        - Minimum CGPA Required: {target_cgpa}

        [The Mathematical Reality]
        - Required Average GPA across remaining units: {required_gpa:.2f}
        - Maximum Possible GPA per semester: {max_system_gpa}

        [Instructions]
        Based on the mathematical reality above, write a concise, 3-to-4 sentence advisory message to the student:
        1. If the 'Required Average GPA' is mathematically possible (less than or equal to {max_system_gpa}), tell them exactly what they need to maintain.
        2. If the 'Required Average GPA' is mathematically impossible (greater than {max_system_gpa}), break the news gently and tell them to aim for the absolute maximum instead.
        3. If the 'Required Average GPA' is below 0, congratulate them because they have mathematically secured the honor regardless of future performance.
        """

        return prompt(prompt_)

