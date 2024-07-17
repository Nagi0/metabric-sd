from dataclasses import dataclass
from tqdm import tqdm
import pandas as pd


@dataclass
class Metabric:
    data_file: str
    gene_set_file: str
    separator: str
    label: list

    def select_label(self, dataframe: pd.DataFrame):
        if (
            "Survival Event" in self.label
            and "Overall Survival Time [months]" in self.label
        ):
            label = dataframe[self.label]
            dataframe = dataframe.drop(columns=self.label)
            dataframe = pd.concat((dataframe, label), axis=1)
        elif "Survival Event" in self.label:
            label = dataframe[self.label]
            dataframe = dataframe.drop(columns=["Overall Survival Time [months]"])
            dataframe = dataframe.drop(columns=self.label)
            dataframe = pd.concat((dataframe, label), axis=1)
            dataframe[self.label] = self.label_to_string(dataframe[self.label])
        else:
            label = dataframe[self.label]
            dataframe = dataframe.drop(
                columns=["Survival Event", "Overall Survival Time [months]"]
            )
            dataframe = dataframe.drop(columns=self.label)
            dataframe = pd.concat((dataframe, label), axis=1)

        return dataframe

    def label_to_string(self, series: pd.Series):
        return series.replace(1, "p").replace(0, "n")

    @staticmethod
    def categorize(value, q1, q3):
        if value < q1:
            return "low"
        elif value > q3:
            return "high"
        else:
            return "medium"

    def dicretize_columns(self, series: pd.Series):
        series = series.astype("float")
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        series = series.apply(self.categorize, args=(q1, q3))

        return series

    def apply_quantile_discretization(self, dataframe: pd.DataFrame):
        dataframe = dataframe.astype("object")
        columns_list = dataframe.columns
        for col in tqdm(columns_list):
            dataframe.loc[:, col] = self.dicretize_columns(dataframe[col])

        return dataframe

    def select_atributes(self, dataframe: pd.DataFrame, remove_columns_list: list):
        dataframe = dataframe.drop(columns=self.labels)
        dataframe = dataframe.drop(columns=remove_columns_list)

        return dataframe

    def export_data(self, dataframe: pd.DataFrame):
        dataframe.to_csv("brca_metabric_ssdp.csv", sep=",", index=False)

    def load_dataset(self):
        metabric_df = pd.read_csv(self.data_file, sep=self.separator)
        geneset_df = pd.read_csv(self.gene_set_file, sep=self.separator)

        clinical_columns = list(metabric_df.columns[:32])
        available_genes = list(geneset_df["Input gene ID"].values)

        genes_df = metabric_df[available_genes]
        clinical_df = metabric_df[clinical_columns]

        genes_df = self.apply_quantile_discretization(genes_df)
        output_df = pd.concat((clinical_df, genes_df), axis=1)
        output_df = self.select_label(output_df)

        return output_df


if __name__ == "__main__":
    metabric = Metabric(
        "metabrick_sd/brca_metabric_preprocessed.csv",
        "metabrick_sd/Gene Matcher Results.csv",
        ",",
        ["Survival Event"],
    )
    metabric_data = metabric.load_dataset()
    metabric.export_data(metabric_data)
