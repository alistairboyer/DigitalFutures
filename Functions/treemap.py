import numpy
import seaborn
import matplotlib.pyplot


def treemap(
    ax,
    df,
    x,
    y,
    *,
    ypalette=None,
    dropna=False,
    fill_width=False,
    sorter=None,
    vsep=True,
    **barplotkwargs,
) -> None:
    """
    Draw a treemap area plot of two (or one) features within a dataframe on an axis.

    Args:
        ax (matplotlib.axis): axis.
        df (pandas.DataFrame): dataframe.
        x (str | int): Label of x series. Set equal to y for a 1-D plot.
        y (str | int): Label of y series. Set equal to x for a 1-D plot.
        ypalette (dict, optional): Dict of value: color for the vertical axis. Defaults to auto.
        dropna (bool, optional): Drop nan values. Defaults to False.
        fill_width (bool, optional): Fill nans to full width when True or leave space to represent nans when False. Defaults to False.
        sorter (_type_, optional): Sorter for sorting value counts. Defaults to None when descending count is used.
        vsep (bool, optional): Draw vertical separating line. Defaults to True.
        **barplotkwargs (Any): keyword arguments for `sns.barplot()`.
    """

    # initialise variables for labels
    column_labels = [x] if x == y else [x, y]
    count_label = f"{x}_{y}_count"
    x_label = f"{x}_copy" if x == y else x

    # calculate count crosstab
    value_counts = (
        df[column_labels]
        .value_counts(dropna=dropna, normalize=False)
        .to_frame(count_label)
        .reset_index()
    )
    
    # initialise palette
    if ypalette is None:
        ypalette = {k: v for k, v in zip(sorted(value_counts[y].unique()), seaborn.color_palette())}

    # insert dummy column for single axis display
    if x == y:
        value_counts.insert(loc=1, column=x_label, value="")

    # sort
    if sorter is not None:
        value_counts = sorter(value_counts)
    else:
        value_counts = value_counts.sort_values([x_label, y], ascending=False)

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
        for y_value, height, bottom in zip(group[y], heights, bottoms):

            # do the plot!
            seaborn.barplot(
                x=[x],
                y=[height],
                width=[width],
                bottom=[bottom],
                native_scale=True,
                color=ypalette.get(y_value) if ypalette is not None else None,
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
    seaborn.set_theme()
    seaborn.set_context("paper")

    if "get_ipython" not in locals():
        seaborn.mpl.use("TkAgg")

    df = seaborn.load_dataset("penguins")

    palette = {
        name: seaborn.color_palette()[n] for 
        n, name in enumerate(df["species"].unique())
    }

    fig, axs = plt.subplots(4, 1, sharey=True, figsize=(4,12))

    treemap(axs[0], df, "species", "species", ypalette=palette)
    axs[0].set_xticks([])
    axs[0].set_ylabel("species")
    handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in palette.values()]
    axs[0].legend(handles, palette.keys())

    treemap(axs[1], df, "sex", "species", ypalette=palette)
    axs[1].set_xlabel("sex - dropna=False")
    axs[1].set_ylabel("species")

    treemap(axs[2], df, "sex", "species", dropna=True, ypalette=palette)
    axs[2].set_xlabel("sex - dropna=True")
    axs[2].set_ylabel("species")

    treemap(axs[3], df, "sex", "species", dropna=True, fill_width=True, ypalette=palette)
    axs[3].set_xlabel("sex - dropna=True, fill_width=True")
    axs[3].set_ylabel("species")

    fig.suptitle("Penguin Species Distribution by Sex", fontweight="bold")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    example()


