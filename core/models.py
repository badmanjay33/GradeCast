class GradingSystem:
    def __init__(self, name : str, max_gpa : float | int, grade_mapping : dict,
                 semester_honours : dict = None, graduation_honours : dict = None):
        self.name = name
        self.__grade_mapping = grade_mapping
        self.max_gpa = float(max_gpa)
        self.semester_honours = semester_honours or {}
        self.graduation_honours = graduation_honours or {}

    @property
    def grades(self) -> list:
        return list(self.__grade_mapping.keys())

    @property
    def points(self) -> list:
        return list(self.__grade_mapping.values())

    def __getitem__(self, key) -> int | float:
        try:
            return self.__grade_mapping[key]
        except KeyError:
            raise ValueError(f"Grade '{key}' is not recognized in the {self.name}.")


# Default Grading Systems

nuc_ng = GradingSystem(
    name='NUC Nigeria',
    max_gpa=5.0,
    grade_mapping={'A': 5.0, 'B': 4.0, 'C': 3.0, 'D': 2.0, 'E': 1.0, 'F': 0.0},
    graduation_honours={
        'First Class Honours': {'max': 5.00, 'min': 4.50},
        'Second Class Honours (Upper Division)': {'max': 4.49, 'min': 3.50},
        'Second Class Honours (Lower Division)': {'max': 3.49, 'min': 2.40},
        'Third Class Honours': {'max': 2.39, 'min': 1.50},
        'Pass': {'max': 1.49, 'min': 1.00}
    }
)

nbte_ng = GradingSystem(
    name='NBTE Nigeria',
    max_gpa=4.0,
    grade_mapping={
        'A': 4.00, 'AB': 3.50, 'B': 3.25, 'BC': 3.00,
        'C': 2.75, 'CD': 2.50, 'D': 2.25, 'E': 2.00, 'F': 0.00
    },
    graduation_honours={
        'Distinction': {'max': 4.00, 'min': 3.50},
        'Upper Credit': {'max': 3.49, 'min': 3.00},
        'Lower Credit': {'max': 2.99, 'min': 2.50},
        'Pass': {'max': 2.49, 'min': 2.00}
    }
)

american_system = GradingSystem(
    name="American Grading System",
    max_gpa=4.0,
    grade_mapping={
        "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7,
        "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3, "D": 1.0, "F": 0.0
    },
    semester_honours={
        "President's List": {'max': 4.00, 'min': 3.80},
        "Dean's List": {'max': 3.79, 'min': 3.50}
    },
    graduation_honours={
        "Summa Cum Laude": {'max': 4.00, 'min': 3.90},
        "Magna Cum Laude": {'max': 3.89, 'min': 3.80},
        "Cum Laude": {'max': 3.79, 'min': 3.70},
        "University Honors": {'max': 3.69, 'min': 3.50}
    }
)