import pandas as pd
from sklearn.datasets import load_iris

data = load_iris()
X = pd.DataFrame(data.data, columns=data.feature_names)
Y = pd.DataFrame(data.target, columns=["Species"])
df = pd.concat([X, Y], axis=1)
df.head()

from sklearn.datasets import load_breast_cancer
data = load_breast_cancer()