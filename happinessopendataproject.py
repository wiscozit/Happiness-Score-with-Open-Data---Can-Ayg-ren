import pandas as pd
import matplotlib.pyplot as plt

DATA_URL = "https://ourworldindata.org/grapher/happiness-cantril-ladder.csv"


def load_data():
    df = pd.read_csv(DATA_URL)
    return df


def select_entities_and_years(df):
    entity_col = df.columns[0]
    year_col = df.columns[2]
    score_col = df.columns[3]

    entities = ["Turkey", "Lithuania", "World"]

    mask_entity = df[entity_col].isin(entities)
    mask_year = (df[year_col] >= 2011) & (df[year_col] <= 2024)

    small_df = df[mask_entity & mask_year].copy()

    small_df = small_df[[entity_col, year_col, score_col]]
    small_df = small_df.rename(
        columns={
            entity_col: "country",
            year_col: "year",
            score_col: "happiness_score",
        }
    )

    return small_df


def create_summary_table(df):
    summary_rows = []

    for country in sorted(df["country"].unique()):
        temp = df[df["country"] == country].sort_values("year")

        if temp.shape[0] < 2:
            continue

        first_year = int(temp["year"].iloc[0])
        last_year = int(temp["year"].iloc[-1])

        first_value = float(temp["happiness_score"].iloc[0])
        last_value = float(temp["happiness_score"].iloc[-1])

        absolute_change = last_value - first_value

        if first_value != 0:
            percent_change = (absolute_change / first_value) * 100
        else:
            percent_change = None

        summary_rows.append(
            {
                "country": country,
                "first_year": first_year,
                "last_year": last_year,
                "score_first_year": first_value,
                "score_last_year": last_value,
                "absolute_change": absolute_change,
                "percent_change": percent_change,
            }
        )

    summary_df = pd.DataFrame(summary_rows)
    return summary_df


def plot_trend(df):
    plt.figure(figsize=(8, 5))

    for country in sorted(df["country"].unique()):
        temp = df[df["country"] == country].sort_values("year")
        plt.plot(
            temp["year"],
            temp["happiness_score"],
            marker="o",
            label=country,
        )

    plt.xlabel("Year")
    plt.ylabel("Happiness score (0-10)")
    plt.title("Self-reported life satisfaction (2011-2024)")
    plt.legend()
    plt.tight_layout()

    plt.savefig("happiness_trend.png", dpi=200)

    plt.show()


def main():
    print("=== Happiness Open Data Project ===")
    print("Loading data from:")
    print(DATA_URL)

    df_full = load_data()
    print("Full data shape:", df_full.shape)

    df_small = select_entities_and_years(df_full)
    print("Filtered data shape:", df_small.shape)

    summary = create_summary_table(df_small)

    print("\nSummary table (first vs last year, rounded to 2 decimals):")
    print(summary.round(2))

    plot_trend(df_small)

    print("\nProgram finished.")


if __name__ == "__main__":
    main()
