class GradingSystem:
    def __init__(self, name : str, max_gpa : float | int, grade_mapping : dict):
        self.name = name
        self.__grade_mapping = grade_mapping
        self.max_gpa = float(max_gpa)

    @property
    def grades(self) -> list:
        return list(self.__grade_mapping.keys())

    @property
    def points(self) -> list:
        return list(self.__grade_mapping.values())

    def __getitem__(self, key) ->  int | float:
        try:
            return self.__grade_mapping[key]
        except KeyError:
            raise ValueError(f"Grade '{key}' is not recognized in the {self.name}.")


# Default Grading Systems
nuc_ng = GradingSystem('NUC Nigeria', 5, {'A': 5,'B': 4, 'C': 3, 'D': 2, 'E': 1, 'F': 0})
nbte_ng = GradingSystem('NBTE Nigeria', 4, {'A': 4, 'AB': 3.5, 'B': 3.25, 'BC': 3.00,
                                            'C': 2.75, 'CD': 2.50, 'D': 2.25, 'E': 2.0, 'F': 0.0})
american_system = GradingSystem("American Grading System", 4, {"A": 4.0, "A-": 3.7, "B+": \
    3.3, "B": 3.0, "B-": 2.7, "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3, "D": 1.0, "F": 0.0})
