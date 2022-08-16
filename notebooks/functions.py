import datetime
import pandas as pd

def get_data_and_create_excel_file(url, file_name, path):
    df = pd.read_json(url)
    df.to_excel(path+file_name)
    return df
    

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
        data['info'] = initial_df.Nombre[col]
        df = pd.concat([df, data])
     
    # Change column order
    col = df.pop('info')
    df.insert(loc= 0 , column= 'info', value= col)
    
    # Drop innecesary columns
    df = df.drop(['Anyo', 'FK_TipoDato', 'FK_Periodo', 'Secreto'], axis=1)
    
    # Change dateformat
    df['Fecha'] = df['Fecha'].apply(change_date_format)
    
    # Reset index
    df = df.reset_index(drop=True)

    return df


def extract_rows(df, col_name):
    index_lst = []
    for i,v in enumerate(df[col_name]):
        v_splited = v.split('.')
        if 'Personal' in v_splited[0]:
            index_lst.append(i)
        if 'Número de ' in v_splited[0]:
            index_lst.append(i)
        elif 'Grado' in v_splited[0]:
            index_lst.append(i)
    return index_lst