import pandas as pd


def load_database(path: str, separator: str = ","):
    return pd.read_csv(path, sep=separator)


def filter_genes(df: pd.DataFrame, genes_list: list):
    columns_list = df.columns
    if "Survival Event" in columns_list:
        genes_list.append("Survival Event")
    if "Overall Survival Time [months]" in columns_list:
        genes_list.append("Overall Survival Time [months]")

    return df[genes_list]


def export_genes_df(df: pd.DataFrame, file_name: str):
    df.to_csv(f"metabrick_sd/results_analysis/{file_name}.csv", sep=",", index=False)


if __name__ == "__main__":
    genes = [
        "RAN",
        "PAK4",
        "LARP1",
        "EEF1B2",
        "CRYAB",
        "LAMA3",
        "CUEDC1",
        "BUD31",
        "NOVA1",
        "ARAP3",
        "GOPC",
        "RHPN1",
        "ESD",
        "C2orf74",
        "NRBF2",
        "ID3",
        "WDR1",
        "FOXP1-IT1",
        "WWOX",
        "TMPO",
        "LINC00643",
        "HS3ST5",
        "LILRB4",
        "PDE1A",
        "RGMA",
        "BSN",
        "CDK6",
        "POLR3A",
        "PDGFRA",
        "TMEM41B",
        "CAPN11",
        "IL18R1",
        "CCDC33",
        "EGR2",
        "LDHB",
        "VSNL1",
        "ACOT9",
        "C6orf89",
    ]
    metabrick_df = load_database(
        "metabrick_sd/load_database/brca_metabric_survival.csv"
    )
    metabrick_df = filter_genes(metabrick_df, genes)
    print(metabrick_df)
    export_genes_df(metabrick_df, "genes_dataset_p")
