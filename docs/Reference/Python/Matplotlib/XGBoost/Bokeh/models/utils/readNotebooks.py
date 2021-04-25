import matplotlib.pyplot as plt
import nbformat
import json
from toolz import pipe, juxt
import pandas as pd
import seaborn
from toolz import curry

from bokeh.io import show, output_notebook
from bokeh.charts import Bar
from bokeh.models.renderers import GlyphRenderer
from bokeh.models.glyphs import Rect
from bokeh.models import Range1d
from toolz import curry
from bokeh.io import export_svgs
from IPython.display import SVG, display
import warnings
warnings.filterwarnings("ignore")
%matplotlib inline
 
/anaconda/envs/strata/lib/python3.5/site-packages/bokeh/util/deprecation.py:34: BokehDeprecationWarning: 
The bokeh.charts API has moved to a separate 'bkcharts' package.

This compatibility shim will remain until Bokeh 1.0 is released.
After that, if you want to use this API you will have to install
the bkcharts package explicitly.

  warn(message)
 
In [2]:
output_notebook()
 
Loading BokehJS ...
We are going to read the results from the following notebooks
In [3]:
notebooks = {
    'Airline':'01_airline.ipynb',
    'Airline_GPU': '01_airline_GPU.ipynb',
    'BCI': '02_BCI.ipynb',
    'BCI_GPU': '02_BCI_GPU.ipynb',
    'Football': '03_football.ipynb',
    'Football_GPU': '03_football_GPU.ipynb',
    'Planet': '04_PlanetKaggle.ipynb',
    'Plannet_GPU': '04_PlanetKaggle_GPU.ipynb',
    'Fraud': '05_FraudDetection.ipynb',
    'Fraud_GPU': '05_FraudDetection_GPU.ipynb',
    'HIGGS': '06_HIGGS.ipynb',
    'HIGGS_GPU': '06_HIGGS_GPU.ipynb'
}
 
In [4]:
def read_notebook(notebook_name):
    with open(notebook_name) as f:
        return nbformat.read(f, as_version=4)
 
In [5]:
def results_cell_from(nb):
    for cell in nb.cells:
        if cell['cell_type']=='code' and cell['source'].startswith('# Results'):
            return cell
 
In [6]:
def extract_text(cell):
    return cell['outputs'][0]['text']
 
In [7]:
@curry
def remove_line_with(match_str, json_string):
    return '\n'.join(filter(lambda x: match_str not in x, json_string.split('\n')))
 
In [8]:
def process_nb(notebook_name):
    return pipe(notebook_name,
                read_notebook,
                results_cell_from,
                extract_text,
                remove_line_with('total RAM usage'),
                json.loads)
