import pandas as pd
import numpy as np

df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': [4, 5, 6]
})

print(df)
sumaA = df['a'].sum()
sumaB = df['b'].sum()

print(sumaA)
print(sumaB)

arr = np.array([1, 2, 3, 4, 5])
print(arr)
print(arr[-3:])