import matplotlib.pyplot as plt
import seaborn as sns
from core.analyzer import Analyzer

def visualiser(analyzer: Analyzer, gp_max: float):
    semesters : list = analyzer.semesters
    gpas : list = analyzer.all_gpas()

    if len(analyzer.semesters) < 2:
        print('Cannot visualise GPA trend with only one semester')
    else:
        sns.lineplot(x=semesters, y=gpas, marker='o', label='GPA')
        for x_val, y_val in zip(semesters, gpas):
            plt.text(x_val, y_val - 0.15, f'{y_val:.2f}',
                 ha='center', va='top', color='tab:blue', fontweight='bold')

        plt.ylim(0, gp_max)
        plt.legend(loc='lower right')
        plt.title("GPA Trend")
        plt.xlabel("Semester")
        plt.ylabel("Cumulative GPA")
        plt.show()
