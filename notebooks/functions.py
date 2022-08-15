
import datetime
import pandas as pd

def normalize_json(initial_df):
    
    # Function to change date format
    def change_date_format(row):
        date = datetime.date.fromtimestamp(row//1000)
        return date

    # Create new df
    df = pd.DataFrame()
    
    # Normalize json nested dictionary from original dataset
    for col in initial_df.index:
        data = pd.json_normalize(initial_df.Data[col])
        data['Origin'] = initial_df.Nombre[col]
        df = pd.concat([df, data])
     
    # Change column order
    col = df.pop('Origin')
    df.insert(loc= 0 , column= 'Origin', value= col)
    
    # Drop innecesary columns
    df = df.drop(['Anyo', 'FK_TipoDato', 'FK_Periodo', 'Secreto'], axis=1)
    
    # Change dateformat
    df['Fecha'] = df['Fecha'].apply(change_date_format)
    
    # Reset index
    df = df.reset_index(drop=True)

    return df

