import numpy as np

np.array([1,2,3])
np.zeros((2,3))
ar = np.ones((2,2,1))
ar.shape
np.arange(3,7)
np.linspace(0,1,5)

ar1 = np.random.rand(2,3)
ar1.dtype
ar2 = np.random.rand(2,3)
ar2.dtype

ar1 + ar2
ar1 - ar2
ar1 * ar2
ar1 / ar2
ar1 % ar2

ar1.min()
ar2.max()

np.sin(ar1)

ar1.dot(ar2)

np.pow(ar1, 3)

np.sqrt(ar1)

ar1.sort()
ar1.sum()


ar1 + 1
ar1 - 1
ar1 * 2
ar1 / 2
ar1 % 2




np.zeros((2,3),dtype=np.int32)

np.int8
np.int16
np.int32
np.int64

np.uint8
np.uint16
np.uint32
np.uint64

np.float32
np.float64
bool
str

