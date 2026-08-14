from google import genai
import os
from dotenv import load_dotenv
from google.genai import errors
import pandas as pd
from core.models import GradingSystem
import time


class Advisor:
    def __init__(self, analyzer, forecaster=None):
        load_dotenv()
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY2"))
        self.analyzer = analyzer
        self.forecaster = forecaster

        self.persona = ("You are a relatable, direct, and highly practical academic mentor. You speak to students like a\
        supportive and cool professor. Tone is conversational and upbeat. DO NOT use bureaucratic, overly formal, or\
                        dramatic language.")

    def _prompt(self, text: str) -> str:
        max_retries = 3

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=text
                )
                return response.text

            except errors.APIError as e:
                if e.code == 429: # Rate Limits
                    if attempt < max_retries - 1:
                        sleep_time = 2 ** attempt

                        # Override with Google's exact requested wait time if provided
                        if hasattr(e, 'response') and e.response is not None:
                            header_time = e.response.headers.get('Retry-After')
                            if header_time and header_time.isdigit():
                                sleep_time = int(header_time)

                        print(f"[API] Rate limit hit. Retrying in {sleep_time}s...")
                        time.sleep(sleep_time)
                        continue

                    # Final attempt failed
                    retry_time = 60
                    if hasattr(e, 'response') and e.response is not None:
                        header_time = e.response.headers.get('Retry-After')
                        if header_time and header_time.isdigit():
                            retry_time = int(header_time)
                    return f"Sorry, you're out of API tokens. Please wait {retry_time} seconds before asking the Advisor another question."

                elif e.code == 503: # Server Overload
                    if attempt < max_retries - 1:
                        sleep_time = 2 ** attempt
                        print(f"[API] Server overloaded. Retrying in {sleep_time}s...")
                        time.sleep(sleep_time)
                        continue
                    return "The AI Advisor is currently experiencing a massive spike in global traffic.\nTry again in about 5 minutes!"

                # Handle bad API Keys or other configuration issues (400, 401, 403, 404)
                else:
                    return f"The AI Advisor ran into configuration issues  (Error {e.code})."

            except Exception as e:
                return f"Failed to connect to the AI Advisor. Please check your internet connection. (Error: {e})"

    def goal_seeker(self, remaining_units: int, honour: str, grading_system: GradingSystem) -> str:
        cgpa = self.analyzer.cgpa()
        current_units = sum(self.analyzer.df['Units'].to_list())
        max_system_gpa = grading_system.max_gpa

        honor_data = grading_system.graduation_honours.get(honour)
        if not honor_data:
            return f"Honor '{honour}' not found in the grading system."

        target_cgpa = honor_data['min']
        current_points = cgpa * current_units
        target_total_points = target_cgpa * (current_units + remaining_units)
        required_gpa = round((target_total_points - current_points) / remaining_units, 2)

        prompt = f"""
        [System Role]
        {self.persona}

        [Student Data]
        - Current CGPA: {cgpa:.2f} (Credits: {current_units})
        - Goal: {honour} (Requires: {target_cgpa})
        - Required Average for remaining {remaining_units} units: {required_gpa:.2f}
        - System Max GPA: {max_system_gpa}

        [Instructions]
        Write a punchy, 3-sentence response. Use bold text for key numbers.
        1. If mathematically possible (required <= {max_system_gpa}), tell them the exact average to lock in.
        2. If impossible (required > {max_system_gpa}), be straightforward. Pivot immediately to tell them to aim for a perfect {max_system_gpa} to reach their absolute maximum ceiling instead.
        3. If required is <= 0, tell them they've already secured the bag.
        """
        return self._prompt(prompt)

    def what_if(self, expected_grades: list, expected_units: list) -> str:
        if not self.forecaster:
            return "Forecaster module required for What-If Analysis."

        results = self.forecaster.what_if(expected_grades, expected_units)
        current_cgpa = self.analyzer.cgpa()

        prompt = f"""
        [System Role]
        {self.persona}

        [Simulation Data]
        - Current Baseline CGPA: {current_cgpa:.2f}
        - Simulated Semester GPA: {results['expected_gpa']:.2f}
        - New Projected CGPA: {results['expected_cgpa']:.2f}

        [Instructions]
        Write a 3-sentence analysis. Acknowledge the hypothetical semester GPA they are aiming for. Explain exactly how this shifts their overall trajectory (pulls it up, drags it down, or keeps it steady). Use bold text for the numbers.
        """
        return self._prompt(prompt)

    def progress_report(self, total_degree_units: int) -> str:
        cgpa = self.analyzer.cgpa()
        current_units = sum(self.analyzer.df['Units'].to_list())
        percentage = (current_units / total_degree_units) * 100

        prompt = f"""
        [System Role]
        {self.persona}

        [Student Data]
        - Current CGPA: {cgpa:.2f}
        - Completed Units: {current_units} / {total_degree_units}
        - Degree Completion: {percentage:.1f}%

        [Instructions]
        Write a punchy, 3-sentence summary of their progress. Tell them exactly what percentage of their degree they have completed. Assess their CGPA trajectory (strong, solid, or needs a boost). Use bold text for key numbers.
        """
        return self._prompt(prompt)

    def subject_analysis(self) -> str:
        df = self.analyzer.df.copy()

        # Extract the subject prefix (e.g., "MAT 110" -> "MAT")
        df['Subject'] = df['Course Code'].apply(lambda x: str(x).split(' ')[0] if pd.notnull(x) else 'Unknown')

        subject_summary = []
        for subject, group in df.groupby('Subject'):
            total_units = group['Units'].sum()
            grades_received = ", ".join(group['Grade'].tolist())
            subject_summary.append(f"- {subject} ({total_units} units): Grades -> [{grades_received}]")

        summary_text = "\n".join(subject_summary)

        prompt = f"""
        [System Role]
        {self.persona} You are analyzing a student's transcript to find trends.

        [Subject Data]
        {summary_text}

        [Instructions]
        Write a 4-sentence strategic analysis. Identify their strongest subject area. Identify a subject area where they struggle or see dips. Give one highly practical piece of advice on how to balance their schedule next semester based on these trends.
        """
        return self._prompt(prompt)

    def semester_review(self, grading_system: GradingSystem) -> str:
        latest_semester = self.analyzer.df.iloc[-1]['Semester']
        latest_df = self.analyzer.df[self.analyzer.df['Semester'] == latest_semester]

        latest_units = latest_df['Units'].sum()
        current_cgpa = self.analyzer.cgpa()

        # Calculate GPA for the latest semester
        points = sum([grading_system[g] * u for g, u in zip(latest_df['Grade'], latest_df['Units'])])
        latest_gpa = round(points / latest_units, 2) if latest_units else 0.00

        prompt = f"""
        [System Role]
        {self.persona} You are conducting a retrospective review of their last term.

        [Last Semester Data]
        - Term: {latest_semester}
        - Credits taken: {latest_units}
        - Semester GPA: {latest_gpa:.2f}
        - Overall Historical CGPA: {current_cgpa:.2f}

        [Instructions]
        Write a 3-sentence retrospective debrief. Compare their latest Semester GPA to their historical CGPA. Factor in their credit load (heavy or light?). Give them a closing hype-man statement to carry momentum into their next term. Use bold text for key stats.
        """
        return self._prompt(prompt)