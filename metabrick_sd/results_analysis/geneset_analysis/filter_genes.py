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
        "IGFBP6",
        "CENPF",
        "PLXNA3",
        "ADAMTS8",
        "ABCF1",
        "GPR4",
        "RPL36A",
        "DTWD1",
        "MYL7",
        "KLRC3",
        "FBLN1",
        "C21orf9",
        "RABGAP1L",
        "ZWINT",
        "SGCA",
        "C2",
        "CLEC4C",
        "TRIM52",
        "TRIM16",
        "OSBP2",
        "JAZF1",
        "PRKCD",
        "RNF41",
        "ABI3BP",
        "GRHL2",
        "RPS11",
        "SLC46A1",
        "ARMCX6",
        "KIAA1161",
        "CNIH2",
        "PCGF5",
        "GNG2",
        "DNAJC5",
        "KRT16",
        "STAT5A",
        "PELI1",
        "GADD45A",
        "KLK1",
        "NPLOC4",
        "CUL5",
        "SFMBT2",
        "ERICH1",
        "FIS1",
        "C18orf34",
        "MARK2",
        "IFT122",
        "PODXL2",
        "WDR46",
        "SLC1A5",
        "FNDC3A",
        "C11orf1",
    ]

    metabrick_df = load_database(
        "metabrick_sd/results_analysis/geneset_analysis/brca_metabric.csv"
    )
    metabrick_df = filter_genes(metabrick_df, genes)
    print(metabrick_df)
    export_genes_df(metabrick_df, "genes_dataset")
