import polars as pl
import tools.scrapper as sc


def main():
    priceList = pl.read_csv("./data/priceList.csv", separator=";")
    refList = priceList["ref"].to_list()
    sc.get_data(refList)


if __name__ == "__main__":
    main()
