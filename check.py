import random
import string
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pylab as plt

filename = ('final_dataset.csv')
df = pd.read_csv(filename)
df.info()
df.describe().T
print(df)

