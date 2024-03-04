# Pandas
_Alistair Boyer_

Pandas version: 1.5.3
Numpy version: 1.25.2




## Creating, Reading and Converting Data

creating pandas objects
```python
pandas.Series(
    [data_point, ...],         # from iterable
    index=[index, ...],        # default is RangeIndex(0, 1, 2, ...)
    name=name,
    dtype=dtype,               # default is to infer
)  # -> Series
pandas.Series(
    {index: data_point, ...},  # from dict
    ...
)  # -> Series

pandas.DataFrame(
    {column_label: series_data, ...}  # from dict
)  # -> DataFrame
pandas.DataFrame(
    zip(series_data, ...),            # from iterables
    columns=[column_label, ...],
)  # -> DataFrame

series.to_frame(column_label)  # -> DataFrame

```

copy
```python
DataFrame.copy()  # -> DataFrame
Series.copy()  # -> Series
```

reading data
```python
pandas.read_csv(
    {path | url | stream},
    encoding='utf-8',
    sep=',',                  # \t for tab
    header={1 | None | int},  # location of header row
    names=column_names,       # if header is None
    index_col={0 | name},
)  # -> DataFrame

# chunks as a stream
chunks = pandas.read_csv(
    src,
    chunksize=n,
    ...,
)  # -> DataFrame

# concat chunks
pandas.concat(chunks)  # -> DataFrame
```

read and conversion methods

['read_clipboard', 'read_csv', 'read_excel', 'read_feather', 'read_fwf', 'read_gbq', 'read_hdf', 'read_html', 'read_json', 'read_orc', 'read_parquet', 'read_pickle', 'read_sas', 'read_spss', 'read_sql', 'read_sql_query', 'read_sql_table', 'read_stata', 'read_table', 'read_xml']


['to_clipboard', 'to_csv', 'to_dict', 'to_excel', 'to_feather', 'to_gbq', 'to_hdf', 'to_html', 'to_json', 'to_latex', 'to_markdown', 'to_numpy', 'to_orc', 'to_parquet', 'to_period', 'to_pickle', 'to_records', 'to_sql', 'to_stata', 'to_string', 'to_timestamp', 'to_xarray', 'to_xml']


['to_clipboard', 'to_csv', 'to_dict', 'to_excel', 'to_frame', 'to_hdf', 'to_json', 'to_latex', 'to_list', 'to_markdown', 'to_numpy', 'to_period', 'to_pickle', 'to_sql', 'to_string', 'to_timestamp', 'to_xarray']


## Information about the Dataset

shape and size
```python
DataFrame.shape    # READONLY -> Tuple[int, int]
Series.shape       # READONLY -> Tuple[int]

DataFrame.size     # READONLY -> int, equivalent to DataFrame.shape[0] * DataFrame.shape[1]
```

indexes
```python
DataFrame.columns  # -> Index
DataFrame.keys()   # -> Index, equivalent to DataFrame.columns

DataFrame.index    # -> Index
Series.index       # -> Index
Series.keys()      # -> Index, equivalent to DataFrame.index
```

counts
```python
len(DataFrame | Series)        # -> int
DataFrame.count()              # -> int, equivalent to len(DataFrame)
Series.count()                 # -> int, equivalent to len(Series)

DataFrame.nunique()            # -> Series of counts
Series.nunique()               # -> int

DataFrame.value_counts(
    normalize={False | True},  # scale so all add up to 1.0
)  # -> Series, multiindex = column labels, values = (normalised) count descending
Series.value_counts(...)
```

informaton about nulls
```python
DataFrame.info(
    verbose={True | False},
)  # -> None
Series.info(...)  # -> None
# print VALUES and RETURN None

Series.hasnans  # -> bool

DataFrame.isnull().sum()
Series.isnull().sum()
```

unique values
```python
Series.unique()  # -> ndarray, alisas of numpy.unique(Series)
set(Series)      # -> set
```

## Accessing Data by Index

head and tail
```python
DataFrame.head(n=5)  # -> DataFrame, equivalent to DataFrame.iloc[:n] including -ve
Series.head(n=5)     # -> Series, equivalent to Series.iloc[:n] including -ve
```
```python
DataFrame.tail(n=5)  # -> DataFrame, equivalent to DataFrame.iloc[-n:] including -ve
Series.tail(n=5)     # -> Series, equivalent to Series.iloc[-n:] including -ve
```

all content
```python
DataFrame.values        # -> ndarray
Series.values           # -> ndarray

DataFrame.items()       # -> Generator of column Series
DataFrame.iterrows()    # -> Generator of row Series
DataFrame.itertuples()  # -> Generator of NamedTuples for each row

Series.items()          # -> Generator of Tuples (index, value)
```

indexing using [&nbsp;] and . {`__getitem__`, `__getattribute__`}
```python
DataFrame[column_label]         # -> Series, alias of DataFrame.loc[:, column_label]
DataFrame.column_label          # -> Series, alias of DataFrame.loc[:, column_label]
DataFrame[[column_label, ...]]  # -> DataFrame of selected columns, alias of DataFrame.loc[:, [column_label, ...]]

DataFrame[start:stop:step]      # -> DataFrame of sliced rows, alias of DataFrame.loc[row_index_slice, :]

Series[row_label]               # -> value, alias of Series.loc['row_label']

# Bonus:
#DataFrame.get(column_labels, default)
#DataFrame.pop()
```

loc - label indexing (inclusive ranges)
```python
# label indexing
DataFrame.loc[row_label(s), column_label(s)]         # -> DataFrame
Series.loc[row_label(s)]                             # -> value

# slice indexing
DataFrame.loc[row_label_slice, column_label_slice]   # -> DataFrame
Series.loc[row_label_slice]                          # -> Series

# mask indexing
DataFrame.loc[row_bool_mask, column_bool_mask]       # -> DataFrame
Series.loc[row_bool_mask]                            # -> Series

# can mix methods of .loc indexing
```

iloc - integer indexing (exclusive ranges)
```python
# value indexing
DataFrame.iloc[row_index(es), column_index(es)]      # -> DataFrame
Series.iloc[row_index]                               # -> Series

# slice indexing
DataFrame.iloc[row_index_slice, column_index_slice]  # -> DataFrame
Series.iloc[row_index_slice]                         # -> Series

# can mix methods of .iloc indexing
```

slicing
```python
slice(
    start=None,
    stop,      # if a single value is passed as *arg then it is considered as stop
    step=None,
)

[start:stop:step] === slice(start, stop, step)
[start:stop] === slice(start, stop, None)
[::step] === slice(None, None, step)

: === slice(None) === slice(None, None, None)
... === fill other axes with ':'

[val] == [slice(val, val+1, None)][0]
```

## Accessing Data with Tools

filtering
```python
DataFrame.filter(         # filter by index
    items=[labels, ],     # supply items= OR like= OR regex=
    like='substring',
    regex=rexpression',
    axis={1 | 0},
)  # -> DataFame

DataFrame.select_dtypes(           # filter columns by data type
    include={None | [datatype, ...]},
    exclude={None | [datatype, ...]},
)  # -> DataFrame
```

where
```python
DataFrame.where(
    condition,
    value_if_false
)

# see also:
numpy.where(
    condition,
    value_if_true,
    value_if_false,
)
```

random sampling
```python
DataFrame.sample(
    n=n,                     # number of samples
    replace={False | True},  # allow duplicates
)  # -> DataFrame

Series.sample(...)  # -> Series
```

query
```python
DataFrame.query(
    "col1 + col2 ** 2",      # text query
    inplace={False | True},
    **kwargs,                # for any operation within the query
)
```

## Index

```python
DataFrame.set_index(
    label,                   # column to set as index
    inplace={False | True},
)

DataFrame.reset_index(
    drop={False | True},     # delete index or move to standard column
    inplace={False | True},
)
Series.reset_index(...)  # -> DataFrame

# manual column ordering
DataFrame.reindex(
    columns=desired_order_of_column_labels,
)
```

## Data Types

dtype
```python
DataFrame.dtypes   # READONLY -> Series of column dtype
Series.dtype       # READONLY -> dtype
```

astype
```python
Series.astype(
    int, str, float, 'int', 'uint32', 'category', ...
)

DataFrame.astype(
    {colname: type, }
)
```

## Joining and Adding Data

join
```python
# N.B. index must be the same
DataFrame.join(
    {DataFrame | Series | Collection},
    r_suffix=r_suffix,                  # labels for overlapping column labels
)  # -> DataFrame
```

merge
```python
DataFrame.merge(
    other_data,
    how={'left' | 'inner' | ...,},
    on=column_label,
    left_on=column_label,
    right_on=column_label,
    suffixes=('_x', '_y'),    
)  # -> DataFrame

```

concat
```python
pandas.concat(
    (DataFrames, Series, ...),  # collection of data sources
    axis={0 | 1},               # 0: add to rows, 1: add to columns
)  # -> DataFrame
```

insert
```python
DataFrame.insert(
    loc=iloc,
    column=column_label,
    value=data,
)
```

## Explode

Convert list-like data to separate __rows__ with __repeated__ index
```python
DataFrame.explode(
    column=label,
)  # -> DataFrame

Series.explode(
)  # -> Series

```

## Nulls

null filters
```python
DataFrame.isnull()   # -> DataFrame of bools, equivalent to DataFrame.isna()
DataFrame.notnull()  # -> DataFrame of bools, equivalent to DataFrame.notna()

Series.isnull()      # -> Series of bools, equivalent to Series.isna()
Series.notnull()     # -> Series of bools, equivalent to Series.notna()
```

dropping nulls
```python
DataFrame.dropna(
    axis=0,                      # along rows
    subset=[column_label, ...],  # columns to consider
    how={'any' | 'all'},         # drop if one or all null
    inplace={False | True}
)  # -> DataFrame (or None if inplace)
```

filling nulls
```python
DataFrame.fillna(
    value={value | dict | Series | Dataframe},  # new value
    inplace={False | True}
)  # -> DataFrame (or None if inplace)

# see also:
DataFrame.bfill()
DataFrame.ffill()
```

null friendly methods
```python
DataFrame.radd, .rsub, .rmul, .rdiv, .rfloordiv, .rmod, .rpow
# equivalent to add, etc. but with the option to supply a value to use in case of null
```

## Deleting and Renaming

dropping
```python
DataFrame.drop(
    labels=[column_label, ...],
    axis={0 | 1},                  # 0 = rows (default), 1 = cols
    inplace={False | True},
)

Series.drop(
    labels=[row_label, ...],
    inplace={False | True},
)

# see also DataFrame.pop()
```

dropping duplicates
```python
DataFrame.drop_duplicates(
    subset=[column_label, ...],
    keep={'first' | 'last' | False}   # False DROPS ALL duplicates
    inplace={False | True},
)

Series.drop_duplicates(
    ...
)
```

renaming
```python
DataFrame.rename (
    columns={from: to},
    inplace={False | True},
)

DataFrame.columns = new_column_labels
Series.name = new_series_label

DataFrame.index = new_index
Series.index = new_index
```

## Sorting

sorting values
```python
DataFrame.sort_values(
    [column_labels, ...],             # or single value
    ascending=[{True | False}, ...],  # or single value
    inplace={False | True},
)

Series.sort_values(...)
```

sorting index
```python
DataFrame.sort_index(
    inplace={False | True},
)
Series.sort_index(...)
```

rank
```python
Series.rank(
    method={'average' | 'min' | 'max' | 'first' | 'dense'},  # how to rank groups with same value
    na_option={'keep' | 'top' | 'bottom'},                   # what to do with nulls
)
```

## Analysis

Overview Statistics
```python
DataFrame.describe(
    include={None | "all" | [dtype, ...]},
    exclude={None | [dtype, ...]},
    percentiles=[0.25, 0.5, 0.75],
)  # -> DataFrame[index=agg_name, columns=columns]
Series.describe(...)  # -> Series[index=agg_name, columns=columns]

# EXCLUDES NULL VALUES
# Default information: 'count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'
# include='all' adds: 'unique', 'top', 'freq'
```

Correlation
```python
DataFrame.corr(
    method={"pearson" | "kendall" | "spearman" | Callable},
    numeric_only={False | True},
)  # -> DataFrame, cross-tabulated correlation (1.0 along diagonal)
```

Variance and Covariance
```python
DataFrame.var(
    numeric_only={False | True},
)  # -> Series, index = column names; values = variance

DataFrame.cov(
    numeric_only={False | True},
)  # -> DataFrame, cross-tabulated covariance (variance along diagonal)
```

## Binning

binning based on ranges
```python
pandas.cut(
    Series,
    bins={n | [bin_edge, ...]},     # [n+1 bin edges] or int number of bins
    labels=[label, ...],            # bin labels or 0, 1, 2...
    include_lowest={False | True},  # set to True if using generated bin values!
    retbins={False | True},         # function returns (DataFrame, bin_edges) if True
)
```

binning based on quantiles
```python
pandas.qcut(
    Series,
    q=number_of_quantiles  # number of quantiles (4 = quartile) or list of quartile edges
    labels=[label, ...],
)

```

## Applying Functions Across Data

transform
- must return data with same shape as original

```python
DataFrame.transform(               
    func={
      function(Series) -> Series     # function(s) to transform the data
      | "function_name"
      | {column: function, ...}
    },
    axis={0 | 1},                    # column = f(column), when axis = 0; row = f(row), when axis = 1
    args, **kwargs,                  # passed to function
)  # -> DataFrame


Series.transform(...)                # as above, but axis must be 0
```

apply
  - similar to transform but no restrictions on shape of data returned

```python
DataFrame.apply(               
    {
      function(Series) -> Series    # function to transform the data
      | "function_name"             # name of a Callable
      | {column: function, ...}
    },
    axis={0 | 1},                   # column = f(column), when axis = 0; row = f(row), when axis = 1
    raw={False | True},             # True => Series, False => numpy.array
    args, **kwargs,                 # passed to function
)  # -> DataFrame

Series.apply(
    {
      function(Series) -> Series    # function(s) to transform the data
      | "function_name"
    },
    args, **kwargs,                 # passed to function
)
```

map and replace
  -  convert values in Series according to supplied dict (or function)

```python
Series.map(
    {
        {from: to,}               # conversion of values
        |  function
        |  Series
    },
    na_action={None | 'ignore'},  # how to behave with null values
)  # -> Series

Series.replace(
    current_values,               # can be numeric, str, regex or list
    replacemant_values,           # can also be dict as for map
    regex={False | True},
)  # -> Series
# see also Series.str.replace()
```

applymap
 - apply function to every value in DataFrame
 - renamed as _DataFrame_._map_ for version 2.1.0+

```python
DataFrame.applymap(            
    lambda value: f(value),    # for every value: value = f(value)
)                              # -> DataFrame
```

## Pivot and Crosstab

crosstab
 - does not need to be a dataframe
 - defaults to "count" (no value required)
 - can be used for other agregations with value supplied

```python
pandas.crosstab(
    index=Series,              # rows
    columns=Series,            # columns
    values={None | Series},    # None or values for aggfunc
    aggfunc={None | aggfunc},  # counts values if None, else aggfunc of values
)
```

pivot table
 - needs to be a dataframe
 - requires values and aggfunc
 - can use dummy value to access count

```python
DataFrame.pivot_table(
    values={None | Series},                     # None or values for aggfunc
    index=Series,                             # rows
    columns=Series,                           # columns
    aggfunc={"mean" | aggfunc |[aggfunc, ...]},  # aggfunc, or supply list of aggfuncs to split table
) # -> DataFrame

# also available using:
pandas.pivot_table(
    dataframe,
    ... # as above
)
```

## Aggregation Methods

```python
.min()                        # minimum
.max()                        # maximum
.mean()                       # mean
.median()                     # median
.count()                      # count
.sum()                        # sum
.std()                        # standard deviation
.var()                        # variance
.prod()                       # product
.mad()                        # mean absolute deviation [DEPRACATED]

.agg(
  {
    'function_name',          # apply a named function to the data
    | ['function_name', ...]  # apply multiple named functions to the data
    | {'label': 'function'}   # specify which function(s) to apply to columns
  }
)
```

index of extremes
```python
DataFrame.idxmax()          # index of maximum
Series.idxmax()             # index of maximum
DataFrame.idxmin()          # index of minimum
Series.idxmin()             # index of minimum
# example
dataframe.iloc[dataframe["label"].idxmax()]
dataframe.iloc[dataframe["label"]==dataframe["label"].max()]
```

## Grouping Data

groupby
```python
DataFrame.groupby(
    by={
      [column_label, ...]       # ONLY by OR level
      | {label: new_label}
      | Callable[label]
    },
    level=level,                # for multiindex
    sort={True | False},
    group_keys={True | False},
    dropna={True | False},
)  # -> DataFrameGroupBy object
```


methods for grouped data
```python
# general methods work on group data
# the method is applied to each of the groups as if a DataFrame
DataFrameGroupBy.head(n)                 
DataFrameGroupBy.mean(numeric_only=True)
DataFrameGroupBy.agg(['max', 'min', 'mean', ...])
...
```

GroupBy.apply
```python
# apply function to each of the grouped DataFrames
DataFrame.groupby(column_labels).apply(
    lambda DataFrame: f(DataFrame),
)

# apply function to the Series within each of the groups
Series.groupby(column_labels).apply(
    lambda Series: f(Series),
)
```

GroupBy.transform
```python
# use function to transform the columns within each of the grouped dataframes
DataFrame.groupby(column_labels).transform(
    lambda Series: f(Series),
)

# use a function to transform the Series within each of the groups
# must return series of same shape as original
Series.groupby(column_labels).transform(
    lambda Series: f(Series),
)

```

## Window Functions and Shifting

rolling
```python
DataFrame.rolling(
    n,                    # number of rows to group together
    centre={False|True},  # roll to bottom (False) or center (True)
)
```

relative calculations
```python
# shift data by n rows in current order
DataFrame.shift(n)

# equivalent to
shifted = dataframe.iloc[:-2]  # clip data
shifted.index = dataframe.index[2:]  # shift index
dataframe.index.to_frame().join(shifted).drop(columns=[0]) # get the null data back from the origingal index
```

```python
# percentange change
Series.pct_change(n)
# equivalent to
Series/Series.shift(n) - 1

# subtract
DataFrame.diff(n)
# equivalent to
Series - Series.shift(n)
```

## Category [.cat]
```python
# convert series to categorical (or nan)
category = pd.Categorical(
    [value, ...],          
    categories=[category,...],  # default is to generate from .unique()
    ordered={False | True},
)  # -> Categorical

Series.cat.add_categories(
  [category, ...],
)  # -> Categorical
```

## String [.str]

```python
# N.B. applying with .str will skip null values instead of raising an error
Series.str
 []                                          # slicing
 .slice(start, stop, step)                   # .str[slice]
 .len()                                      # length

 .cat(series or str_to_join)                 # concatenate

 .capitalize()                               # First letter is capital
 .casefold()                                 # lower (for case insensitive matching)
 .lower()                                    # convert to lower case
 .swapcase()                                 # sWAP cASE
 .title()                                    # Convert To Title Case
 .upper()                                    # CONVERT TO UPPER CASE

 .isalpha()                                  # str is alphabetical
 .is...                                      # other str.is... methods

 .strip(chars)                               # remove chars from ends of str
 .rstrip(chars)                              # remove chars from ends of str
 .lstrip(chars)                              # remove chars from ends of str

 .contains(searchstr, regex={True | False})  # search (regex accepted)
 .count(searchstr, regex={True | False})     # count values in a str
 .extract(re, regex={True | False})          # extract match from str
 .replace(old, new, regex={True | False})    # replace
 .split(
    split=split,
    regex={True | False},
    expand={False | True},                   # split a string (and expand to new cols)
 )
 .get(n)                                     # get nth value after split

 .get_dummies()                              # one hot encoding for categories



.str.findall('\w+').apply(''.join)           # remove word breaks
```

## Datetime [.dt]

.dt
```python
Series.dt
  .hour
  .year
  .quarter
  ...
```

creation
```python
pandas.to_datetime(
    data,                # data for conversion, e.g. string
    format='%Y-%m-%d',   # dat format (omit for automatic!)
)

# useful to set as index then sort
dataframe.set_index('date_series', inplace=True)
dataframe.sort_index(inplace=True)
```

resample
```python
DataFrame.resample(
    '1hour',         # time window to up/down sample to
)
# use with .bfill() and .ffill() when upsampling
```

datetime range
```python
pandas.date_range(
    start,            # start
    periods=n,        # number of datapoints
    freq="D",         # days
)

# alternatively:
pandas.date_range(start, end)  #  inclusive date range
```

business datetime range
```python
pandas.bdate_range(
    start,
    end,
    freq='C',                   # 'C' = custom, default is 'B' = business daily
    holidays=[date, ...],       # list of holidays, see numpy.busdaycalendar
    weekmask="Mon Tue Thu Fri"  # str of business days, see numpy.busdaycalendar
)
```

timedelta
```python
pandas.timedelta("7 days")  # other examples "1 years"
# see datetime.timedelta(weeks=1)

# can be used for arithmetic operations on datetime series
# is the result of arithmetic operations on datetime series
```

## Formatting DataFrames
```python
DataFrame.style.format(
    formatter='{:0.2f}',  # supply a single value to format all or dict to format by column
)  # -> Styler (can get data back with .data)
```

[Formatting for strings](https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals)

## Pandas Options

```python
pd.options.display.max_columns = {20 | None}  # How many columns to display n or all (None)
pd.options.display.max_rows = {20 | None}     # How many rows to display n or all (None)
```
https://pandas.pydata.org/docs/user_guide/options.html

