import polars as pl


def formatCategoriesFromSQL(
    ps_category_path, ps_category_lang_path, toCSV=False, outputPath=None
):
    """
    Format the categories from SQL database to a DataFrame.
    Args:
        ps_category_path (str): Path to the ps_category CSV file.
        ps_category_lang_path (str): Path to the ps_category_lang CSV file.
        toCSV (bool): If True, save the DataFrame as a CSV file.
        outputPath (str): Path to save the CSV file if toCSV is True.
    Returns:
        pl.DataFrame: Formatted categories DataFrame.
    """
    ps_category = pl.read_csv(ps_category_path)
    ps_category_lang = pl.read_csv(ps_category_lang_path)
    categories = (
        ps_category.join(
            ps_category_lang,
            left_on="id_category",
            right_on="id_category",
            how="left",
        )
        .filter(pl.col("id_lang") == 1)
        .select(
            pl.col("id_category"),
            pl.col("id_parent"),
            pl.col("active"),
            pl.col("id_shop"),
            pl.col("name"),
        )
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


def getRootCategories(ps_category_path, ps_category_lang_path, id_parent=2):
    """
    Get the root categories from the SQL database.
    Args:
        ps_category_path (str): Path to the ps_category CSV file.
        ps_category_lang_path (str): Path to the ps_category_lang CSV file.
        id_parent (int): The parent ID to filter categories.
    Returns:
        pl.DataFrame: Filtered categories DataFrame.
    """
    ps_category = formatCategoriesFromSQL(ps_category_path, ps_category_lang_path)

    ps_category = ps_category.filter(
        pl.col("id_parent") == id_parent, pl.col("id_shop") == 2
    )

    return ps_category
