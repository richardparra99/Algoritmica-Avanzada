import pandas as pd
import numpy as np

nombre = ['Empleado' + str(1) for i in range(1, 11)]
salario = np.random.uniform(2360, 5000, 10)
antiguedad = np.random.randint(1 , 10, 10)
cargos = np.random.choice(['Gerente', 'Frontend', 'Backend', 'Devops', 'Designer'], 10)

df = pd.DataFrame({
    'Nombre': nombre,
    'Salario': salario,
    'Antiguedad': antiguedad,
    'Cargos': cargos
})
print(df)