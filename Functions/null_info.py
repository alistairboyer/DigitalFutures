import pandas

# typing
from pandas.core.frame import DataFrame
from pandas.io.formats.style import Styler


def null_info(
    dataframe: DataFrame,
    order_by_null_pc: bool = True,
) -> Styler:
    """
    Generate a new styled dataframe containing information about
    null, zero and unique values in the supplied dataframe.

    Args:
        dataframe (pandas.DataFrame):
            the supplied dataframe
        order_by_null_pc (bool):
            When `True` sorts the result by percentage null values in decreasing order;
            then by percentage zero values in decreasing order;
            then by column alphabetically.
            When False, the result is alphabetical by column label.
            Defaults to True.
    Returns:
        styler (pandas.io.formats.style.Styler):
            Styler: a DataFrame with formatting information attached for .ipynb display.
            The raw dataframe can be accessed using the `.data` attribute.
            Index:
                'column' = column names
            Columns:
                'null' = count of null values
                'null_pc' = percentage of null values
                'zero' = count of zero values
                'zero_pc' = percentage of zero values
                'n_unique' = number of unique values
                'dtype' = series datatype
    """

    # create a new dataframe from columns names
    null_info_dataframe = pandas.DataFrame([], index=dataframe.columns)
    null_info_dataframe.index.name = "columns"  # default is Columns

    #Series.count just does this
    
    # get the nulls
    null_info_dataframe["nulls"] = dataframe.isnull().sum(axis=0)
    null_info_dataframe["null_pc"] = (
        100 * null_info_dataframe["nulls"] / dataframe.shape[0]
    )

    # get the zeros
    null_info_dataframe["zeros"] = (dataframe == 0).sum(axis=0)
    null_info_dataframe["zero_pc"] = (
        100 * null_info_dataframe["zeros"] / dataframe.shape[0]
    )

    # get unique
    null_info_dataframe["n_unique"] = dataframe.nunique()

    # dtype
    null_info_dataframe["dtype"] = dataframe.dtypes

    # sort by index
    null_info_dataframe.sort_index(inplace=True)
    # sort by null percentage
    if order_by_null_pc:
        null_info_dataframe.sort_values(
            ["null_pc", "zero_pc"], ascending=False, inplace=True
        )

    # style and return
    return null_info_dataframe.style.format(
        {
            "null_pc": "{:.1f}%",
            "zero_pc": "{:.1f}%",
        }
    )


def _test_example() -> None:
    """Example using data seaborn titanic dataset."""
    print("""Example using data seaborn titanic dataset.""")
    print("https://github.com/mwaskom/seaborn-data")
    print()

    import seaborn

    df = seaborn.load_dataset("titanic")
    print(null_info(df).data)  # type: ignore[attr-defined]


if __name__ == "__main__":
    _test_example()
