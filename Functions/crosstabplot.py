import numpy
import seaborn
import matplotlib.pyplot

from typing import Callable, Optional, Any
from pandas.core.frame import DataFrame
from matplotlib.axes import Axes


def crosstabplot(
    ax: Axes,
    df: DataFrame,
    x_label: str,
    y_label: str,
    *,
    y_palette: Optional[dict[str, Any]] = None,
    dropna: bool = False,
    fill_width: bool = False,
    sorter: Optional[Callable[[DataFrame], DataFrame]] = None,
    vsep: bool = True,
    **barplotkwargs: Any,
) -> None:
    """
    Draw a treemap-type crosstab area plot of two (or one) features within a dataframe on an axis.

    Args:
        ax (matplotlib.axis): axis.
        df (pandas.DataFrame): dataframe.
        x_label (str): Label of x series. Set equal to y for a vertical 1-D plot.
        y_label (str): Label of y series. Set equal to x for a vertical 1-D plot.
        y_palette (dict, optional): Dict of {value: color} for the vertical axis. Defaults to None when the palette is automatically generated from the unique values of the data.
        dropna (bool, optional): Drop nan values. Defaults to False.
        fill_width (bool, optional): Fill nans to full width when True or leave space to represent nans when False. Defaults to False.
        sorter (_type_, optional): Sorter for sorting value counts. Defaults to None when descending count is used.
        vsep (bool, optional): Draw vertical separating line. Defaults to True.
        **barplotkwargs (Any): keyword arguments for `sns.barplot()`.
    """

    # initialise variables for labels
    column_labels = [x_label] if x_label == y_label else [x_label, y_label]
    count_label = f"{x_label}_{y_label}_count"
    x_label = f"{x_label}_copy" if x_label == y_label else x_label

    # calculate count crosstab
    value_counts = (
        df[column_labels]
        .value_counts(dropna=dropna, normalize=False)
        .to_frame(count_label)
        .reset_index()
    )

    # initialise palette
    if y_palette is None:
        y_palette = {
            k: v
            for k, v in zip(
                sorted(value_counts[y_label].unique()), seaborn.color_palette()
            )
        }

    # insert dummy column for single axis display
    if value_counts.shape[1] == 2:
        value_counts.insert(loc=1, column=x_label, value="")

    # sort
    if sorter is not None:
        value_counts = sorter(value_counts)
    else:
        value_counts = value_counts.sort_values([x_label, y_label], ascending=False)

    # get groups
    groups = value_counts.groupby(x_label, dropna=False, sort=False)

    # calculate horizontal data
    width_scale = groups[count_label].sum().sum() if fill_width else len(df)
    widths = groups[count_label].sum() / width_scale
    xs = numpy.pad(widths, (1, 0), constant_values=(0,))[:-1].cumsum() + widths / 2.0

    # iterate horizontally
    for (_, group), width, x in zip(groups, widths, xs):

        # calculate vertical data
        heights = group[count_label] / group[count_label].sum()
        bottoms = numpy.pad(heights, (1, 0), constant_values=(0,))[:-1].cumsum()

        # reset color cycle back to 0
        ax.set_prop_cycle(None)

        # iterate vertically
        for y_value, height, bottom in zip(group[y_label], heights, bottoms):

            # do the plot!
            seaborn.barplot(
                x=[x],
                y=[height],
                width=[width],
                bottom=[bottom],
                native_scale=True,
                color=y_palette.get(y_value) if y_palette is not None else None,
                ax=ax,
                **barplotkwargs,
            )

        # vertical separator
        if vsep and (x + width / 2.0) < 1.0:
            ax.axvline(x + width / 2.0, color="white", linewidth=0.5, linestyle="--")

    # axis settings
    ax.set(
        xticks=xs,
        xticklabels=xs.index,
        xlim=(0.0, 1.0),
        ylim=(0.0, 1.0),
    )


def example() -> None:
    plt = seaborn.mpl.pyplot

    if "get_ipython" not in locals():
        seaborn.mpl.use("TkAgg")

    # get example data
    df = seaborn.load_dataset("penguins")

    # generate palette
    palette = {
        name: seaborn.color_palette()[n]
        for n, name in enumerate(df["species"].unique())
    }

    # set up axes
    fig, axs = plt.subplots(4, 1, sharey=True, figsize=(4, 12))

    # do crosstab - 1D "sex" (same label for x and y)
    crosstabplot(axs[0], df, "species", "species", y_palette=palette)
    axs[0].set_xticks([])
    axs[0].set_ylabel("species")
    handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in palette.values()]
    axs[0].legend(handles, palette.keys())

    # do crosstab - "sex" vs "species"
    crosstabplot(axs[1], df, "sex", "species", y_palette=palette)
    axs[1].set_xlabel("sex [dropna=False]")
    axs[1].set_ylabel("species")

    # do crosstab - "sex" vs "species", demonstrate dropna
    crosstabplot(axs[2], df, "sex", "species", dropna=True, y_palette=palette)
    axs[2].set_xlabel("sex [dropna=True]")
    axs[2].set_ylabel("species")

    # do crosstab - "sex" vs "species", demonstrate fill_width
    crosstabplot(
        axs[3], df, "sex", "species", dropna=True, fill_width=True, y_palette=palette
    )
    axs[3].set_xlabel("sex [dropna=True, fill_width=True]")
    axs[3].set_ylabel("species")

    # overall title and layout
    fig.suptitle("Penguin Species Distribution by Sex", fontweight="bold")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    example()
