import matplotlib.pyplot as plt
import seaborn as sns

def visualiser(semesters : list, gpas : list, max : int | float):
    if len(semesters) < 2:
        print('Cannot visualise GPA trend with only one semester')
    else:
        sns.lineplot(x=semesters, y=gpas, marker='o', label='GPA')
        for x_val, y_val in zip(semesters, gpas):
            plt.text(x_val, y_val - 0.15, f'{y_val:.2f}',
                 ha='center', va='top', color='tab:blue', fontweight='bold')

        plt.ylim(0, max)
        print(gpas)
        plt.legend(loc='lower right')
        plt.title("GPA Trend")
        plt.xlabel("Semester")
        plt.ylabel("Cumulative GPA")
        plt.show()