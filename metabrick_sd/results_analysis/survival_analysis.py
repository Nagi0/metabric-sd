import pandas as pd
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt


def load_database(path: str, separator: str = ","):
    return pd.read_csv(path, sep=separator)


def plot_kaplan_meiler_survival(
    group_1: pd.DataFrame, group_2: pd.DataFrame, group_label: str
):
    kmf = KaplanMeierFitter()

    # Plot survival curve for group 1
    kmf.fit(
        group_1["Overall Survival Time [months]"],
        event_observed=group_1["Survival Event"],
        label=group_label,
    )
    ax = kmf.plot_survival_function()

    # Plot survival curve for group 2
    kmf.fit(
        group_2["Overall Survival Time [months]"],
        event_observed=group_2["Survival Event"],
        label="Others",
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
        "metabrick_sd/load_database/brca_metabric_survival.csv"
    )

    # Define the conditions for the two groups
    group_1 = metabrick_df.loc[
        (metabrick_df["Relapse Event"] == 1.0)
        & (metabrick_df["ESD"] == "low")
        & (metabrick_df["C2orf74"] == "low")
    ]
    group_2 = metabrick_df[
        ~(
            (metabrick_df["Relapse Event"] == 1.0)
            & (metabrick_df["ESD"] == "low")
            & (metabrick_df["C2orf74"] == "low")
        )
    ]

    plot_kaplan_meiler_survival(
        group_1, group_2, group_label="Relapse Event=1.0 & ESD=low & C2orf74=low"
    )
