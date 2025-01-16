# PS-MLAI

Basic template for complex machine learning/AI projects. 

---

### Why use it?

For those who are beginners or intermediates in data science, you might have experienced starting a complex project and ending up with a tangled .py file full of variables, functions, and objects due to the numerous analyses, treatments, and models required.

To avoid this, this repository aims to create a basic framework for ML/AI projects. With this structure, we achieve better organization, well-defined processes, easy code maintenance, and process monitoring through logs.

```
app
├── analysis
│   └── [your analysis here]
├── bin
│   └── [serialization files (cache)]
├── config
│   └── [your config variables here]
├── data
│   └── [your data or connection with database here]
├── graphs
│   └── [your graphs here]
├── log
├── models
│   └── [your models here]
├── resources
│   └── [your resources here]
├── treatment
│   └── [your data treatment here]
├── __init__.py
└── __main__.py
```
---

## The 3 Basic Features

By using this framework, you will have access to three useful features for your project:

| Feature | Description | Location |
|---------|-------------|----------|
| Logs | Monitor where, when, and for how long a process was executed | [log/genlog.py](/app/log/genlog.py) |
| Config | Set project variables, such as batch size and dataset split, facilitating variable changes for testing | [config/config_files.py](/app/config/config_files.py) |
| Bin | Data serialization to serve as a cache or to free up memory | [resources/bin_manager.py](/app/resources/bin_manager.py) |

### (1) Logs

By using a log from `genlog`, we can monitor the executed process. To implement it, consider the following example:

```python
from resources.genlog import genlog

class SVM(object):
    def __init__(self, data: np.ndarray) -> None:
        ...
    
    def fit(self) -> None:
        # your model fit
        genlog.log(status=True, info="fitting the SVM model", v=True)

```
The response will be:

```
[2024-05-24 15:25:59.772359] [SVM (fit)] [SUCCESS] | fitting the SVM model
```

Above, we implemented a log entry for when an SVM model is executed. For more information on how to implement logging, read [link here]().

### (2) Config

The config feature centralizes your project variables in one place. To implement this, follow these steps:

1. Create an `.ini` file in the `app/config` directory. For example, `dataset.ini`.
2. Define the variables in this file:

```
[dataset:split]
split_ratio = 0.60

[dataset:t_sne]
dimensions = 2
```

3. Use these variables in your project:

```python
from treatment.spliter import SplitDataset
from analysis.dim_reduction import TSNE
from config.config_files import configfiles

split_ratio: float = float(configfiles.dot_ini['dataset']['dataset:split']['split_ratio'])
df_train, df_test = SplitDataset(split_ratio).split()

tsne_dimensions: int = int(configfiles.dot_ini['dataset']['dataset:t_sne']['dimensions'])
df_tsne: np.ndarray = TSNE(tsne_dimensions)
```

To access these variables in your project, use `configfiles.dot_ini["name of the .ini file (without extension)"]["main key"]["variable"]`.

You can create numerous `.ini` files to organize your variables. For more information on configuration files, read [link here]().

### (3) Bin

File serialization serves to avoid unnecessary reprocessing or to free up virtual memory in extreme cases. An example of its use to prevent reprocessing:

```python
from resources.bin_manager import BinManager

bin_manager = BinManager()

df_normalized: pd.DataFrame = NormalizationTakes2Long(df)
bin_manager.post("df_normalized", df_normalized)
```

In the example above, the pandas DataFrame will be saved to a `.bin` file in `app/bin/`. This way, you can retrieve the file if you need to reprocess your model.

```python
from resources.bin_manager import BinManager

bin_manager = BinManager()

#df_normalized: pd.DataFrame = NormalizationTakes2Long(df)
#bin_manager.post("df_normalized", df_normalized)
df_normalized: pd.DataFrame = bin_manager.get("df_normalized")
```

This approach is useful when no changes have been made prior to the data serialization. If any changes have been made, you will need to reprocess everything again.
