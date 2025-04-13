import polars as pl


def formatCategories(
    ps_category_path, ps_category_lang_path, toCSV=False, outputPath=None
):
    ps_category = pl.read_csv(ps_category_path)
    ps_category_lang = pl.read_csv(ps_category_lang_path)
    categories = ps_category.join(
        ps_category_lang,
        left_on="id_category",
        right_on="id_category",
        how="left",
    ).select(
        pl.col("id_category"),
        pl.col("id_parent"),
        pl.col("active"),
        pl.col("id_shop"),
        pl.col("name"),
    )

    if toCSV:
        if outputPath:
            categories.write_csv(outputPath)
            print(f"Write in : {outputPath}")
        else:
            categories.write_csv("data/categories.csv")
            print("Write by default in 'data/categories.csv'")
    else:
        return categories
