import os
import time
import ssl
import webbrowser
import site
import pytest
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from astropy.coordinates import SkyCoord
from astropy.coordinates import Distance
from astropy import units as u
from galaxywitness.base_complex import BaseComplex
from galaxywitness.witness_complex import WitnessComplex
from galaxywitness.alpha_complex import AlphaComplex
from galaxywitness.datasets import Dataset
from gudhi.clustering.tomato import Tomato


path = os.path.abspath('../..') +  '/data/' + 'Galaxies_1KK.csv'
df = pd.read_csv(path)

n_gal = 5000
type_of_complex = 'alpha'
first_witness = 0

column_nums = [1, 2, 3]
column_names = [list(df)[column_nums[0]], list(df)[column_nums[1]], list(df)[column_nums[2]]]

points = np.array(df[column_names].values[first_witness:n_gal + first_witness])

coord = SkyCoord(
    ra=points[:, 0] * u.degree,
    dec=points[:, 1] * u.degree,
    distance=Distance(z=points[:, 2])
)

points = np.transpose(np.array(coord.cartesian.xyz), (1, 0))
landmarks = points

complex_ = BaseComplex()
complex_.__class__ = AlphaComplex
complex_.__init__(points=landmarks)

key_complex_type = 'custom'
complex_.compute_simplicial_complex(d_max=3, r_max=7.5, custom=(key_complex_type == 'custom'))

t = Tomato(density_type = 'logDTM', graph_type='knn')
t.fit(complex_.points)

assert t.n_clusters_ != 0