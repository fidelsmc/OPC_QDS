import pandas as pd

# Extrae la lista de señales
def signals():
    signals = pd.read_excel('DataMap.xlsx',sheet_name='Signals',engine='openpyxl')
    return signals


