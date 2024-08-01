from dataclasses import dataclass
import pandas as pd
from tqdm import tqdm


@dataclass
class SubgroupDatabase:
    path: str
    separator: str

    def load_database(self) -> pd.DataFrame:
        return pd.read_csv(self.path, sep=self.separator)

    def build_subgroup_representation(self, subgroups_list: list) -> pd.DataFrame:
        data = pd.read_csv(self.path, sep=self.separator)

        for label, subgroup in subgroups_list:
            indicator = data.index.isin(subgroup.index).astype(int)
            data[label] = indicator

        return data

    def parse_conditions(self, conditions_str: str, df: pd.DataFrame):
        conditions = conditions_str.split(",")
        query_conditions = []

        for cond in conditions:
            col, value = cond.split("!=" if "!=" in cond else "=")
            col = col.strip()
            value = value.strip()
            operator = "!=" if "!=" in cond else "=="

            query_conditions.append(f"`{col}` {operator} '{value}'")

        query_str = " & ".join(query_conditions)
        return df.query(query_str)

    def extract_subgroups_from_text(self, file_path: str, df: pd.DataFrame):
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        subgroups_text = text.strip().split("\n")

        subgroups = []
        for conditions_str in tqdm(subgroups_text):
            if conditions_str:
                label = conditions_str
                subgroup_df = self.parse_conditions(conditions_str, df)
                subgroups.append((label, subgroup_df))

        return subgroups


if __name__ == "__main__":
    txt_file_path = "analysis_results/ssdp_results/ssdp_genes_only_results.txt"
    subgroup_representation = SubgroupDatabase(
        "load_database/brca_metabric_clinical_plus_genes.csv",
        separator=",",
    )
    df = subgroup_representation.load_database()

    subgroups = subgroup_representation.extract_subgroups_from_text(txt_file_path, df)

    result_df = subgroup_representation.build_subgroup_representation(subgroups)
    result_df.to_csv(
        "results_analysis/coax_regression_analysis/subgroup_representation.csv",
        index=False,
    )
    print(result_df)
