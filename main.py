import polars as pl
import tools.scrapper as sc
import tools.categorizer as cat
import argparse

parser = argparse.ArgumentParser(description="Scrapping Beligne")
parser.add_argument("--mode", type=str, help="Le mode de fonctionnement")
args = parser.parse_args()


def main():
    if args.mode == "scrap":
        try:
            priceList = pl.read_csv("./data/test.csv", separator=";")
            refList = priceList["ref"].to_list()
            df = sc.get_data(refList)
        except Exception as e:
            print(f"An error occurred during scraping: {e}")
            raise
        finally:
            if "df" in locals() and df is not None and len(df) > 0:
                df.write_csv("./data/data.csv")
                print(f"Data saved to ./data/data.csv with {len(df)} entries")
    if args.mode == "categorize":
        print("Categorizing data")


if __name__ == "__main__":
    main()
