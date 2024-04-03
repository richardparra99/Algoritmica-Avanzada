# Tarea de Duplicados en array
class Solution:
    def duplicates(self, arr, n):
        duplicados = set()  # Almacena los elementos duplicados
        vistos = set()  # Almacena los elementos vistos

        for elemento in arr:  # Iteración sobre la matriz
            if elemento in vistos:  # verificacion de visto
                duplicados.add(elemento)  #  agregamos 
            else:
                vistos.add(elemento)  # pasamos a  vistos

        return sorted(duplicados) if duplicados else [-1]  # lista ordenada de duplicados, o [-1]
    
if(__name__ == '__main__'):
    t = int(input())
    for i in range(t):
        n = int(input())
        arr = list(map(int,input().strip().split()))
        res = Solution().duplicates(arr,n)
    for i in res:
        print(i,end =" ")
        print()