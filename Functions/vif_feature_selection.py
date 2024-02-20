from statsmodels.stats.outliers_influence import variance_inflation_factor

# typing
from typing import List, Dict, Union
from pandas.core.frame import DataFrame


def vif_feature_selection(
    dataframe: DataFrame,
    threshold: float = 5.0,
    const: Union[str, int] = "const",
    verbose: bool = True,
) -> List[Union[str, int]]:
    """
    Remove columns from a dataframe by considering variance inflation factor [VIF]
    and removing the largest until all are lower than the threshold.

    VIF calculation using `statsmodels.stats.outliers_influence.variance_inflation_factor()`

    Args:
        dataframe (pandas.DataFrame):
            The dataframe for consideration.
            N.B. Must include a const column, see: `statsmodels.tools.tools.add_constant()`.
        threshold (float, optional):
            VIF threshold.
            Defaults to 5.0.
        const (str | int):
            Label of the constant column.
            Defaults to 'const'.
        verbose (bool, optional):
            When true uses `print` to display information about the process:
            the columns being removed and their associated VIF; and the final columns and VIFs.

    Returns:
        List[str | int]:
            List of column labels that meet the VIF threshold.

    Raises:
        AssertionError:
            If there is no 'const' in the dataframe.
    """

    # need to have 'const' in the vif calculation because
    # function includes call to statsmodels.regression.linear_model.OLS(endog, exog)
    # https://www.statsmodels.org/dev/_modules/statsmodels/stats/outliers_influence.html#variance_inflation_factor
    assert (
        const in dataframe.columns
    ), "There must be a `const` column in the dataframe."

    # initialise vif values to 0.0
    vifs: Dict[Union[str, int], float]
    vifs = {label: 0.0 for label in dataframe.columns}

    # loop
    while True:

        if verbose:
            print(f'checking features: {"; ". join(map(str, vifs))}')

        # calculate vifs
        vifs = {
            label: variance_inflation_factor(dataframe[list(vifs)], label_index)
            for label_index, label in enumerate(list(vifs))
            if label != const  # no need to caluclate vif for 'const'
        }

        # need to keep 'const' key and don't want to drop 'const', so set vif['const'] = 0.0
        vifs[const] = 0.0

        # get biggest vif
        # biggest_vif_label = max(vifs, key=vifs.get)  # errors in type checking
        biggest_vif_label = max(vifs, key=lambda label: vifs[label])

        # all values below threshold
        if vifs[biggest_vif_label] < threshold:
            if verbose:
                print("  ok")
            break

        # drop label with biggest vif
        if verbose:
            print(
                f"  excluding '{biggest_vif_label}' with vif of {vifs[biggest_vif_label]:.2f}"
            )
        # remove the biggest vif
        del vifs[biggest_vif_label]

    # final selection has been made
    if verbose:
        print("final selection:")
        for label, vif in vifs.items():
            print(f"  {label} [{vif=:.2f}]")

    # convert keys to list and return
    return list(vifs)


def _test_example() -> None:
    """Example using data from https://online.stat.psu.edu/stat501/lesson/12/12.4."""
    import pandas

    print(
        """Example using data from https://online.stat.psu.edu/stat501/lesson/12/12.4."""
    )
    print()

    df = pandas.read_csv(
        "https://online.stat.psu.edu/onlinecourses/sites/stat501/files/data/bloodpress.txt",
        sep="\t",
        index_col="Pt",
    )
    X = df.copy()
    X["const"] = 1.0
    y = X.pop("BP")
    vif_feature_selection(X)


if __name__ == "__main__":
    _test_example()
