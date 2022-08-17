import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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


def change_value(row):
    if row == 'Residentes en el Extranjero':
        row = 'Residentes en el extranjero'
        return row
    else:
        return row

    
def find_string(df, col_name, string):
    df = df.loc[df[col_name].str.contains(string)]
    return df, df.index


def describe_df(df):
    print('Shape of dataframe is:')
    print(df.shape)
    print('')
    print('Data types of dataframe are:') 
    print(df.dtypes)
    print('')
    print('Summary of numeric data is:')
    print(df.describe().T)
    print('')
    print('Summary of categorical data is:')
    print(df.describe(include='object').T)
    print('')
    print('Does it contain missing values?')
    print(df.isna().sum())
    print('')
    print('Value counts:')
    for col in df:
        print(df[col].value_counts(),'\n')
        
        
def create_histograms(df, col_name_category, col_name_values):
    fig, ax = plt.subplots(dpi=100)
    for i in df[col_name_category].unique():
        item = df[col_name_values].loc[(df[col_name_category] == i) == True]
        ax = sns.histplot(item, palette= 'colorblind')
        ax.set_title('Histogram of {}'.format(i))
        plt.show()
        
        
def create_boxplots(df, col_name_category, col_name_values):
    fig, ax = plt.subplots(dpi=100)
    for i in df[col_name_category].unique():
        item = df[col_name_values].loc[(df[col_name_category] == i) == True]
        ax = sns.boxplot(item, palette= 'colorblind')
        ax.set_title('Boxplot of {}'.format(i))
        plt.show()
        
        
def detect_outliers(df, col_name):
    q1 = df[col_name].quantile(q= 0.25)
    q3 = df[col_name].quantile(q= 0.75)
    iqr = q3 - q1

    # Upper and lower limit
    lower_limit = q1 - 1.5*iqr
    upper_limit = q3 + 1.5*iqr
    
    outliers_lst = df[col_name][(df[col_name] >= upper_limit) | (df[col_name] <= lower_limit)]
    outliers_idx = df[col_name][(df[col_name] >= upper_limit) | (df[col_name] <= lower_limit)].index

    print('Q1 is:', q1)
    print('Q3 is:', q3)
    print('IQR is:', iqr)
    print('Upper limit is:', upper_limit)
    print('Lower limit is:', lower_limit)
    
    return outliers_lst, outliers_idx
    