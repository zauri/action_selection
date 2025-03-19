## Scripts

A collection of scripts for data extraction and transformation (raw data -> neural network input).

### Folders
- archive: Old versions of scripts.
- data: Input data for + output data from scripts. (Output data is named \*categorized.csv, \*encoded.csv, \*transformed.csv)

### Files

- *extract*\*.ipynb/\*.py: Extraction of necessary information (spatial information, item categories) from the raw data in csv format.
- *encode*\*.ipynb/\*.py: Encodes singular items in item categories.
- *transform*\*.ipynb/\*.py: Transforms data into input format for neural networks.
- *transform\_data\_to\_single\_step\_workflow.py*: Main script to transform data from raw data to neural network input format (combines all other necessary scripts).
