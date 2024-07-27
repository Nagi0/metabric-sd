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
        event_observed=group_1["survival_event"],
        label=group_label,
    )
    ax = kmf.plot_survival_function()

    # Plot survival curve for group 2
    kmf.fit(
        group_2["Overall Survival Time [months]"],
        event_observed=group_2["survival_event"],
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
        "metabrick_sd/load_database/brca_metabric_clinical.csv"
    )
    metabrick_df["survival_event"] = metabrick_df["survival_event"].replace("p", 1)
    metabrick_df["survival_event"] = metabrick_df["survival_event"].replace("n", 0)

    # Define the conditions for the two groups
    group_1 = metabrick_df.loc[
        (metabrick_df["MYL7"] == "< 0.79325")
        & (metabrick_df["CORO1B"] == "≥ -0.360250")
        & (metabrick_df["MRE11A"] == "< -1.2973")
    ]
    group_2 = metabrick_df[
        ~(
            (metabrick_df["MYL7"] == "< 0.79325")
            & (metabrick_df["CORO1B"] == "≥ -0.360250")
            & (metabrick_df["MRE11A"] == "< -1.2973")
        )
    ]

    plot_kaplan_meiler_survival(
        group_1,
        group_2,
        group_label="MYL7< 0.79325 & CORO1B≥ -0.360250 & MRE11A< -1.2973",
    )
