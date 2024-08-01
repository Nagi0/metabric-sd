import pandas as pd
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt

def load_database(path: str, separator: str = ","):
    return pd.read_csv(path, sep=separator)

def plot_kaplan_meier_survival(subgroups_df: pd.DataFrame):
    kmf = KaplanMeierFitter()

    subgroups_list = subgroups_df.columns
    subgroups_list = subgroups_list[:-2]

    # Plot survival curve for the entire population
    kmf.fit(
        subgroups_df["Overall Survival Time [months]"],
        event_observed=subgroups_df["survival_event"],
        label="Population Mean",
    )
    ax = kmf.plot_survival_function()
    ax.lines[-1].set_linestyle("--")
    ax.lines[-1].set_color("black")
    ax.fill_between(
        kmf.survival_function_.index,
        kmf.confidence_interval_["Population Mean_lower_0.95"],
        kmf.confidence_interval_["Population Mean_upper_0.95"],
        color="black",
        alpha=0.3,
    )

    for i, col in enumerate(subgroups_list):
        subgroup = subgroups_df[
            [col, "survival_event", "Overall Survival Time [months]"]
        ]
        subgroup = subgroup.loc[subgroup[col] == 1.0]

        if i == 0:
            label = "Top1 'n'"
        elif i == 1:
            label = "Top2 'n'"
        elif i == 2:
            label = "Top1 'p'"
        elif i == 3:
            label = "Top2 'p'"

        # Plot survival curve for each subgroup
        kmf.fit(
            subgroup["Overall Survival Time [months]"],
            event_observed=subgroup["survival_event"],
            label=label,
        )
        kmf.plot_survival_function(ax=ax)

    # Customize the plot
    plt.title("Kaplan-Meier Survival Curves")
    plt.xlabel("Time")
    plt.ylabel("Survival Probability")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    metabrick_df = load_database(
        "results_analysis/coax_regression_analysis/subgroup_representation.csv"
    )
    metabrick_df["survival_event"] = metabrick_df["survival_event"].replace("p", 1)
    metabrick_df["survival_event"] = metabrick_df["survival_event"].replace("n", 0)

    num_subgroup_representations = 4

    subgroups_df = metabrick_df.iloc[:, -num_subgroup_representations:]
    subgroups_df["survival_event"] = metabrick_df["survival_event"]
    subgroups_df["Overall Survival Time [months]"] = metabrick_df[
        "Overall Survival Time [months]"
    ]
    plot_kaplan_meier_survival(subgroups_df)
