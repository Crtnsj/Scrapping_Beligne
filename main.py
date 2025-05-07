import polars as pl

import domain.services.scrapper as sc
import domain.services.categorizer as cat
import infrastructure.ollamaAPI as ollama
import argparse
import domain.services.creator as testcreator
from infrastructure.prestashopAPI import PrestaShopAPI

parser = argparse.ArgumentParser(description="Scrapping Beligne")
parser.add_argument("--mode", type=str, help="Le mode de fonctionnement")
parser.add_argument("--sinput", type=str, help="Le fichier d'entrée pour le scrapping")
parser.add_argument("--tAgentModelFile", type=str, help="Le fichier du model agent")
parser.add_argument("--tools", type=str, help="Le nom de l'outil à utiliser")
args = parser.parse_args()


def main():
    if args.mode == "scrap":
        try:
            priceList = pl.read_csv(args.sinput, separator=";")
            refList = priceList["ref"].to_list()
            df = sc.get_data(refList)
        except Exception as e:
            print(f"An error occurred during scraping: {e}")
            raise
        finally:
            if "df" in locals() and df is not None and len(df) > 0:
                df.write_csv("./data/data.csv")
                print(f"Data saved to ./data/data.csv with {len(df)} entries")
    elif args.mode == "categorize":
        cat.categorize(
            pl.read_csv("./data/data.csv"),
        )
    elif args.tools == "createAgentFromJson":
        if args.tAgentModelFile is None:
            raise ValueError("Le fichier du model agent est requis")
        else:
            ollama.createModelFromJson(args.tAgentModelFile)
    elif args.mode == "test":
        api = PrestaShopAPI(
            "http://localhost:8080/api/", "8PUU9Z9QCUH3R73MSSRYPT4IDL65XLMB"
        )
        df = pl.read_csv("data/data_test.csv")
        testcreator.createArticles(df, api)


if __name__ == "__main__":
    main()
