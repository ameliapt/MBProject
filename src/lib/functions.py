
import pandas as pd
from itertools import chain
import datetime
import matplotlib.pyplot as plt
import seaborn as sns


###### FUNCTIONS FOR SPECIFICS DATAFRAMES #######

def get_data_and_create_file(url, file_name, path):
    df = pd.read_json(url)
    df.to_excel(path+file_name)
    return df
    

def change_date_format(row):
    date = datetime.date.fromtimestamp(row//1000)
    return date


def normalize_json(initial_df):
    df = pd.DataFrame()
    
    for col in initial_df.index:
        data = pd.json_normalize(initial_df.Data[col])
        data['info'] = initial_df.Nombre[col]
        df = pd.concat([df, data])
     
    col = df.pop('info')
    df.insert(loc= 0 , column= 'info', value= col)
    df = df.drop(['Anyo', 'FK_TipoDato', 'FK_Periodo', 'Secreto'], axis=1)
    df['Fecha'] = df['Fecha'].apply(change_date_format)
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




############### FUNCTIONS TO GET DATA FROM INE AND CREATE EXCEL FILES ##############

def get_tourists_by_origin(url, file_name, path_raw, path_clean):
	
	# Request to INE API and first selection of data
	json_df = get_data_and_create_file(url, file_name, path_raw)
	json_df = json_df.loc[json_df['Nombre'].str.contains('Dato base')]

	# Unnest JSON dictionary and clean data
	df = normalize_json(json_df)
	df['destiny'] = df['info'].apply(lambda x: x.split('.')[3])
	df['destiny'] = df['destiny'].apply(lambda x: x.lstrip())
	df['category'] = df['info'].apply(lambda x: x.split('.')[2])
	df['category'] = df['category'].apply(lambda x: x.lstrip())
	df['origin'] = df['info'].apply(lambda x: x.split('.')[0])
	df['origin'] = df['origin'].apply(lambda x: x.lstrip())

	df = df.drop('info', axis=1)
	df.isna().sum()
	df = df.reindex(columns = ['origin', 'category','destiny', 'Valor','Fecha'])
	df = df.rename(columns = {'Valor': 'value', 'Fecha':'date'})

	df.to_excel(path_clean+file_name)

	return 


def get_tourist_by_expenditure(url, file_name, path_raw, path_clean):

	# Request to INE API and first selection of data
	json_df = get_data_and_create_file(url, file_name, path_raw)
	json_df = json_df.loc[json_df['Nombre'].str.contains('Dato base')]

	# Unnest JSON dictionary and clean data
	df = normalize_json(json_df)
	total_expenditure = df.loc[df['info'].str.contains('Gasto total')]
	df = df.drop(total_expenditure.index, axis=0)

	#Subset 1
	total_expenditure['expense_item'] = total_expenditure['info'].apply(lambda x: x.split('.')[2])
	total_expenditure['expense_item'] = total_expenditure['expense_item'].apply(lambda x: x.lstrip())

	total_expenditure['destiny'] = total_expenditure['info'].apply(lambda x: x.split('.')[0])

	#Subset 2
	df['expense_item'] = df['info'].apply(lambda x: x.split('.')[1])
	df['expense_item'] = df['expense_item'].apply(lambda x: x.lstrip())

	df['destiny'] = df['info'].apply(lambda x: x.split('.')[2])
	df['destiny'] = df['destiny'].apply(lambda x: x.lstrip())
	df.head()

	#Subsets combined
	df = pd.concat([total_expenditure, df])
	df = df.drop('info', axis = 1)

	rows_with_info_reversed = list(df['expense_item'].unique())
	rows_info = df.loc[df['expense_item'] == 'Otras Comunidades Autónomas']
	df['expense_item'].iloc[42:48] = 'Gasto total'
	df['destiny'].iloc[42:48] = 'Otras Comunidades Autónomas'

	df.isna().sum()
	df = df.reindex(columns = ['expense_item', 'destiny', 'Valor', 'Fecha'])
	df = df.rename(columns = {'Valor': 'value','Fecha':'date'}).reset_index(drop=True)

	df.to_excel(path_clean+file_name)

	return 


def get_tourist_by_stay(url, file_name, path_raw, path_clean):

	# Request to INE API and first selection of data
	json_df = get_data_and_create_file(url, file_name, path_raw)
	json_df = json_df.loc[json_df['Nombre'].str.contains('Dato base')]


	df = normalize_json(json_df)
	df['stay_type'] = df['info'].apply(lambda x: x.split('.')[1])
	df['stay_type'] = df['stay_type'].apply(lambda x: x.lstrip())

	df['expense_cat'] = df['info'].apply(lambda x: x.split('.')[2])
	df['expense_cat'] = df['expense_cat'].apply(lambda x: x.lstrip())

	df = df.drop('info', axis = 1)
	df.isna().sum()

	df = df.reindex(columns = ['stay_type', 'expense_cat', 'Valor', 'Fecha'])
	df = df.rename(columns = {'Valor': 'value', 'Fecha':'date'})

	df.to_excel(path_clean+file_name)

	return



def get_tourists_by_sex_gender(url, file_name, path_raw, path_clean):

	# Request to INE API and first selection of data
	json_df = get_data_and_create_file(url, file_name, path_raw)
	json_df = json_df.loc[json_df['Nombre'].str.contains('Dato base')]

	df = normalize_json(json_df)

	df['sex'] = df['info'].apply(lambda x: x.split(".")[4])
	df['sex'] = df['sex'].apply(lambda x: x.lstrip())

	df['age'] = df['info'].apply(lambda x: x.split(".")[5])
	df['age'] = df['age'].apply(lambda x: x.lstrip())

	df['expense_cat'] = df['info'].apply(lambda x: x.split(".")[1])
	df['expense_cat'] = df['expense_cat'].apply(lambda x: x.lstrip())

	df['destiny'] = df['info'].apply(lambda x: x.split(".")[2])
	df['destiny'] = df['destiny'].apply(lambda x: x.lstrip())

	df = df.drop('info', axis=1)

	df = df.reindex(columns = ['expense_cat','destiny','age','sex','Valor', 'Fecha'])
	df = df.rename(columns = {'Valor': 'value','Fecha':'date'})

	df.to_excel(path_clean+file_name)

	return
                                                                          
                                 
def tourists_by_motive(url, file_name, path_raw, path_clean):

	# Request to INE API and first selection of data
	json_df = get_data_and_create_file(url, file_name, path_raw)
	json_df = json_df.loc[json_df['Nombre'].str.contains('Dato base')]

	df = normalize_json(json_df)
	df['expense_cat'] = df['info'].apply(lambda x: x.split('.')[1])
	df['expense_cat'] = df['expense_cat'].apply(lambda x: x.lstrip())

	df['motive'] = df['info'].apply(lambda x: x.split('.')[0])

	df = df.drop('info', axis=1)
	df = df.fillna(0)

	df = df.reindex(columns= ['expense_cat', 'motive','Valor', 'Fecha'])
	df = df.rename(columns = {'Valor': 'value', 'Fecha':'date'}).reset_index(drop=True)

	df.to_excel(path_clean+file_name)

	return 


def num_tourists_destiny(url, file_name, path_raw, path_clean):

	# Request to INE API and first selection of data
	json_df = get_data_and_create_file(url, file_name, path_raw)
	json_df = json_df.loc[json_df['Nombre'].str.contains('Dato base')]

	df = normalize_json(json_df)

	df['destiny'] = df['info'].apply(lambda x: x.split('.')[0])
	df['destiny'] = df['destiny'].replace('Turista', 'Total Nacional')

	df = df.drop('info', axis = 1)

	df = df.reindex(columns=['destiny', 'Valor', 'Fecha'])
	df = df.rename(columns = {'Valor': 'value', 'Fecha':'date'})

	df.to_excel(path_clean+file_name)

	return 



def num_tourists_stay(url, file_name, path_raw, path_clean):

	# Request to INE API and first selection of data
	json_df = get_data_and_create_file(url, file_name, path_raw)
	json_df = json_df.loc[json_df['Nombre'].str.contains('Dato base')]

	df = normalize_json(json_df)
	df['stay_type'] = df['info'].apply(lambda x: x.split('.')[1])
	df['stay_type'] = df['stay_type'].apply(lambda x: x.lstrip())

	df = df.drop('info', axis = 1)

	df = df.reindex(columns = ['stay_type','Valor', 'Fecha'])
	df = df.rename(columns = {'Valor':'value', 'Fecha':'date'})

	df.to_excel(path_clean+file_name)

	return



def num_tourists_motive(url, file_name, path_raw, path_clean):

	# Request to INE API and first selection of data
	json_df = get_data_and_create_file(url, file_name, path_raw)
	json_df = json_df.loc[json_df['Nombre'].str.contains('Dato base')]

	df = normalize_json(json_df)
	df['motive'] = df['info'].apply(lambda x: x.split('.')[1])
	df['motive'] = df['motive'].apply(lambda x: x.lstrip())

	df = df.drop('info', axis=1)
	df = df.reindex(columns = ['motive', 'Valor', 'Fecha'])
	df = df.rename(columns = {'Valor':'value', 'Fecha': 'date'})

	df.to_excel(path_clean+file_name)

	return 



def num_tourists_origin(url, file_name, path_raw, path_clean):

	# Request to INE API and first selection of data
	json_df = get_data_and_create_file(url, file_name, path_raw)
	json_df = json_df.loc[json_df['Nombre'].str.contains('Dato base')]

	df = normalize_json(json_df)
	df['origin'] = df['info'].apply(lambda x: x.split('.')[0])
	df = df.fillna(0)

	df = df.reindex(columns = ['origin', 'Valor', 'Fecha'])
	df = df.rename(columns = {'Valor':'value', 'Fecha': 'date'}).reset_index(drop=True)

	df.to_excel(path_clean+file_name)

	return


def hotel_nights(url, file_name, path_raw, path_clean):

	# Request to INE API and first selection of data
	json_df = get_data_and_create_file(url, file_name, path_raw)
	json_df = json_df.loc[json_df['Nombre'].str.contains('Pernoctaciones')]
	df = normalize_json(json_df)


	#Subset 1
	city_first = df.loc[~df['info'].str.contains('Nacional')]
	city_first['tourist_point'] = city_first['info'].apply(lambda x: x.split('.')[0])
	city_first['origin'] = city_first['info'].apply(lambda x: x.split('.')[3])
	city_first['origin'] = city_first['origin'].apply(lambda x: x.lstrip())

	city_first = city_first[city_first['tourist_point'] != 'Pernoctaciones']
	city_first_idx = city_first.index

	#Subset 2
	city_w_num = df.loc[df['info'].str.contains('[0-9]')]
	city_w_num_idx = city_w_num.index
	df = df.drop(city_w_num_idx)

	city_w_num['origin'] = city_w_num['info'].apply(lambda x: x.split('.')[4])
	city_w_num['origin'] = city_w_num['origin'].apply(lambda x: x.lstrip())

	city_w_num['tourist_point'] = city_w_num['info'].apply(lambda x: x.split('.')[3])
	city_w_num['tourist_point'] = city_w_num['tourist_point'].apply(lambda x: x.lstrip())
	city_w_num['tourist_point'] = city_w_num['tourist_point'].apply(lambda x: x.split('-')[1])

	#Subset 3
	df = df.drop(city_first_idx)
	df['origin'] = df['info'].apply(lambda x: x.split('.')[3])
	df['origin'] = df['origin'].apply(lambda x: x.lstrip())

	df['tourist_point'] = df['info'].apply(lambda x: x.split('.')[2])
	df['tourist_point'] = df['tourist_point'].apply(lambda x: x.lstrip())

	df2 = pd.concat([df, city_w_num, city_first]).reset_index(drop=True)

	df2 = df2.drop(['info', 'Notas'], axis= 1)
	df2 = df2.fillna(0)
	df2 = df2.reindex(columns = ['tourist_point', 'Valor', 'origin', 'Fecha'])
	df2 = df2.rename(columns = {'Valor':'value', 'Fecha':'date'})
	df2.reset_index(drop=True).head()

	df2['origin'] = df2['origin'].apply(change_value)

	df2 = df2.replace({'tourist_point': {'Arcos De La Frontera': 'Arcos de la Frontera', 'Elche/Elx':'Elche', 'Palma De Mallorca':'Palma de Mallorca', 'Castellón De La Plana':'Castellón de la Plana', 'El Puerto De Santa María':'El Puerto de Santa María', 'Jerez De La Frontera':'Jerez de la Frontera', 'Las Palmas De Gran Canaria':'Las Palmas de Gran Canaria', 'Pajara':'Pájara', 'Puerto De La Cruz':'Puerto de la Cruz', 'San Bartolomé De Tirajana':'San Bartolomé de Tirajana', 'Santa Cruz De Tenerife':'Santa Cruz de Tenerife', 'Santiago De Compostela':'Santiago de Compostela', 'Tias':'Tías', }})
	
	df2.to_excel(path_clean+file_name)

	return


def hotel_overview(url, file_name, path_raw, path_clean):

	# Request to INE API and first selection of data
	json_df = get_data_and_create_file(url, file_name, path_raw)
	df = normalize_json(json_df)
	df = df.drop('Notas', axis = 1)

	#Subset 1
	rows_no_national_first = df.loc[~df['info'].str.contains('Nacional')]
	rows_no_nat_city_first = extract_rows(rows_no_national_first, 'info')
	rows_no_nat_city_first = rows_no_national_first.iloc[rows_no_nat_city_first]
	rows_no_national_first = rows_no_national_first.drop(rows_no_nat_city_first.index)
	rows_extra_value = df[df['info'].str.contains('hoteleros')]

	index_lst = list(rows_extra_value.index) + list(rows_no_nat_city_first.index) + list(rows_no_national_first.index)
	df = df.drop(index_lst, axis = 0)

	df['tourist_point'] = df['info'].apply(lambda x: x.split('.')[2])
	df['tourist_point'] = df['tourist_point'].apply(lambda x: x.lstrip())

	df['category'] = df['info'].apply(lambda x: x.split('.')[1])
	df['category'] = df['category'].apply(lambda x: x.lstrip())

	df = df.drop('info', axis = 1)

	#Identifying cells with numbers
	num_cities = df.loc[df['tourist_point'].str.contains('[0-9]')]
	#Spliting cells values and storing the name part
	num_cities['tourist_point'] = num_cities['tourist_point'].apply(lambda x: x.split('-', 1)[1])
	df['tourist_point'].loc[num_cities['tourist_point'].index] = num_cities['tourist_point']

	# Deleting blank spaces
	df['tourist_point'] = df['tourist_point'].apply(lambda x: x.lstrip())
	df['tourist_point'].unique()

	rows_no_national_first['tourist_point'] = rows_no_national_first['info'].apply(lambda x: x.split('.')[0])
	rows_no_national_first['category'] = rows_no_national_first['info'].apply(lambda x: x.split('.')[1])
	rows_no_national_first['category'] = rows_no_national_first['category'].apply(lambda x: x.lstrip())

	rows_no_national_first = rows_no_national_first.drop('info', axis = 1)


	#Subset 2
	rows_no_nat_city_first['tourist_point'] = rows_no_nat_city_first['info'].apply(lambda x: x.split('.')[2])
	rows_no_nat_city_first['tourist_point'] = rows_no_nat_city_first['tourist_point'].apply(lambda x: x.lstrip())

	rows_no_nat_city_first['category'] = rows_no_nat_city_first['info'].apply(lambda x: x.split('.')[0])
	rows_no_nat_city_first = rows_no_nat_city_first.drop('info', axis = 1)

	#Subset 3
	rows_extra_value['tourist_point'] = rows_extra_value['info'].apply(lambda x: x.split('.')[3])
	rows_extra_value['tourist_point'] = rows_extra_value['tourist_point'].apply(lambda x: x.lstrip())

	rows_extra_value['category'] = rows_extra_value['info'].apply(lambda x: x.split('.')[2])
	rows_extra_value['category'] = rows_extra_value['category'].apply(lambda x: x.lstrip())

	rows_extra_value = rows_extra_value.drop('info', axis = 1)

	num_rows_extra_value = rows_extra_value.loc[rows_extra_value['tourist_point'].str.contains('[0-9]')]
	num_rows_extra_value['tourist_point'] = num_rows_extra_value['tourist_point'].apply(lambda x: x.split('-', 1)[1])
	rows_extra_value['tourist_point'].loc[num_rows_extra_value['tourist_point'].index] = num_rows_extra_value['tourist_point']
	rows_extra_value['tourist_point'] = rows_extra_value['tourist_point'].apply(lambda x: x.lstrip())
	rows_extra_value['tourist_point'].unique()

	df = pd.concat([df,rows_no_nat_city_first, rows_no_national_first, rows_extra_value])

	df = df.replace({'tourist_point': {'Palmas De Gran Canaria, Las': 'Las Palmas de Gran Canaria', 'Las Palmas De Gran Canaria':'Las Palmas de Gran Canaria', 'Palmas de Gran Canaria, Las': 'Las Palmas de Gran Canaria', 'San Bartolomé De Tirajana': 'San Bartolomé de Tirajana', 'València': 'Valencia', 'Vitoria-Gasteiz':'Vitoria-Gastéiz', 'Tias':'Tías', 'Santiago De Compostela':'Santiago de Compostela', 'Santa Cruz De Tenerife':'Santa Cruz de Tenerife', 'Roquetas de Mar':'Roquetas De Mar', 'Pajara':'Pájara', 'Puerto De la Cruz':'Puerto de La Cruz', 'El Puerto De Santa María':'El Puerto de Santa María', 'Puerto de Santa María, El':'El Puerto de Santa María', 'Peníscola/Peñíscola':'Peñiscola', 'Pamplona/Iruña':'Pamplona', 'Palma':'Palma de Mallorca', 'Palma De Mallorca': 'Palma de Mallorca', 'Naut Aran':'Naut Arant', 'Jerez De la Frontera':'Jerez de la Frontera', 'Jerez De La Frontera':'Jerez de la Frontera', 'Grove, O':'Grove (O)', 'Gandia':'Gandía', 'Dénia':'Denia','Donostia/San Sebastián':'Donostia-San Sebastián', 'Coruña, A':'Coruña', 'Castelló de la Plana':'Castellón de la Plana', 'Castellón De La Plana': 'Castellón de la Plana', 'Calvià':'Calviá', 'Arcos De la Frontera':'Arcos de la Frontera', 'Arcos De La Frontera':'Arcos de la Frontera', 'Alicante/Alacant':'Alicante', 'Elche/Elx':'Elche'}})

	df = df.fillna(0)
	df = df.reindex(columns = ['tourist_point', 'category', 'Valor', 'Fecha'])
	df = df.rename(columns = {'Valor': 'value', 'Fecha':'date'})
	df.reset_index(drop=True).head()

	df.to_excel(path_clean+file_name)

	return 



def hotel_adr(url, file_name, path_raw, path_clean):

	# Request to INE API and first selection of data
	json_df = get_data_and_create_file(url, file_name, path_raw)
	df = normalize_json(json_df)

	df = df.loc[df['info'].str.contains('Dato base.')]
	df['tourist_point'] = df['info'].apply(lambda x: x.split('.')[0])
	df = df.drop('info', axis=1)
	df = df.fillna(0)

	df = df.reindex(columns = ['tourist_point', 'Valor', 'Fecha'])
	df = df.rename(columns = {'Valor': 'value', 'Fecha':'date'})
	df.reset_index(drop=True).head()

	df = df.replace({'tourist_point':{'Alicante/Alacant':'Alicante', 'Vitoria-Gasteiz':'Vitoria-Gastéiz', 'Elche/Elx':'Elche', 'Calvià':'Calviá', 'Palma':'Palma de Mallorca', 'Puerto de Santa María, El':'El Puerto de Santa María', 'Castelló de la Plana':'Castellón de la Plana', 'Peníscola/Peñíscola':'Peñiscola', 'Coruña, A':'Coruña', 'Pamplona/Iruña':'Pamplona', 'Palmas de Gran Canaria, Las':'Las Palmas de Gran Canaria', 'Grove, O':'Grove (O)', 'Naut Aran':'Naut Arant', 'Donostia/San Sebastián':'Donostia-San Sebastián', 'València':'Valencia', 'Roquetas de Mar':'Roquetas De Mar', 'Dénia':'Denia'}})

	df.to_excel(path_clean+file_name)

	return 


def apartments_nights(url, file_name, path_raw, path_clean):

	# Request to INE API and first selection of data
	json_df = get_data_and_create_file(url, file_name, path_raw)
	df = normalize_json(json_df)

	#Subset 1
	df = df.loc[df['info'].str.contains('Pernoctaciones')]

	#Subset 2
	rows_no_national_first = df.loc[~df['info'].str.contains('Nacional')]
	rows_no_national_first['tourist_point'] = rows_no_national_first['info'].apply(lambda x:x.split('.')[0])
	rows_no_national_first['origin'] = rows_no_national_first['info'].apply(lambda x:x.split('.')[3])
	rows_no_national_first['origin'] = rows_no_national_first['origin'].apply(lambda x: x.lstrip())

	rows_no_national_first = rows_no_national_first.drop(['info', 'Notas'], axis=1)


	df = df.drop(rows_no_national_first.index)

	df['tourist_point'] = df['info'].apply(lambda x:x.split('.')[2])
	df['tourist_point'] = df['tourist_point'].apply(lambda x: x.lstrip())

	df['origin'] = df['info'].apply(lambda x:x.split('.')[3])
	df['origin'] = df['origin'].apply(lambda x: x.lstrip())

	df = df.drop(['info', 'Notas'], axis = 1).reset_index(drop=True)

	df = pd.concat([df, rows_no_national_first]).reset_index(drop=True)

	df = df.fillna(0)
	df['origin'] = df['origin'].apply(change_value)

	df = df.reindex(columns = ['tourist_point', 'origin', 'Valor', 'Fecha'])
	df = df.rename(columns = {'Valor': 'value', 'Fecha':'date'})
	df.reset_index(drop=True).head()

	df = df.replace({'tourist_point':{'Calpe/Calp':'Calp', 'Javea/Xabia':'Javea', 'Palma De Mallorca':'Palma de Mallorca', 'Iruela (La)':'La Iruela', 'Segura De La Sierra':'Segura de la Sierra', 'Pajara':'Pájara', 'San Bartolomé De Tirajana':'San Bartolomé de Tirajana', 'Tias':'Tías', 'Paso (El)':'El Paso', 'Puerto De La Cruz':'Puerto de la Cruz', 'San Miguel De Abona':'San Miguel de Abona', 'San Sebastian De La Gomera':'San Sebastián de la Gomera', 'Santa Cruz De La Palma':'Santa Cruz de la Palma', 'Santiago Del Teide':'Santiago del Teide', 'Vitoria-Gasteiz':'Vitoria-Gastéiz', 'Alicante/Alacant':'Alicante', 'Pamplona/Iruña':'Pamplona'}})

	df.to_excel(path_clean+file_name)
	return 


def apartments_overview(url, file_name, path_raw, path_clean):

	# Request to INE API and first selection of data
	json_df = get_data_and_create_file(url, file_name, path_raw)
	df = normalize_json(json_df)

	#Subset 1
	rows_w_num = df.loc[df['info'].str.contains('[0-9]')]

	rows_w_num['tourist_point'] = rows_w_num['info'].apply(lambda x: x.split('.')[3])
	rows_w_num['tourist_point'] = rows_w_num['tourist_point'].apply(lambda x: x.split('-', 1)[1])

	rows_w_num['category'] = rows_w_num['info'].apply(lambda x: x.split('.')[2])
	rows_w_num['category'] = rows_w_num['category'].apply(lambda x: x.lstrip())

	rows_w_num = rows_w_num.drop(['info', 'Notas'], axis=1)
	rows_w_num.head()

	#Subset 2
	rows_with_national = df.loc[df['info'].str.contains('Nacional')]
	rows_with_national = rows_with_national.drop(rows_w_num.index)

	rows_with_national['tourist_point'] = rows_with_national['info'].apply(lambda x: x.split('.')[2])
	rows_with_national['tourist_point'] = rows_with_national['tourist_point'].apply(lambda x: x.lstrip())

	rows_with_national['category'] = rows_with_national['info'].apply(lambda x: x.split('.')[1])
	rows_with_national['category'] = rows_with_national['category'].apply(lambda x: x.lstrip())

	rows_with_national = rows_with_national.drop(['info', 'Notas'], axis=1)

	#Subset 3
	info_reversed = df.loc[~df['info'].str.contains('Nacional')]

	string = ['Málaga', 'Zaragoza', 'Cuenca']
	lst_cities = []

	for s in string:
	    res = find_string(info_reversed, 'info', s)
	    lst_cities.append(res[1])

	lst_idx_cities = list(chain(*lst_cities))
	info_reversed_cities = info_reversed.loc[lst_idx_cities, :]
	info_reversed = info_reversed.drop(info_reversed_cities.index)

	info_reversed['tourist_point'] = info_reversed['info'].apply(lambda x: x.split('.')[2])
	info_reversed['tourist_point'] = info_reversed['tourist_point'].apply(lambda x: x.lstrip())

	info_reversed['category'] = info_reversed['info'].apply(lambda x: x.split('.')[0])
	info_reversed['category'] = info_reversed['category'].apply(lambda x: x.lstrip())

	info_reversed = info_reversed.drop(['info', 'Notas'], axis=1)

	#Subset 4
	info_reversed_cities['tourist_point'] = info_reversed_cities['info'].apply(lambda x: x.split('.')[0])

	info_reversed_cities['category'] = info_reversed_cities['info'].apply(lambda x: x.split('.')[1])
	info_reversed_cities['category'] = info_reversed_cities['category'].apply(lambda x: x.lstrip())

	info_reversed_cities = info_reversed_cities.drop(['info', 'Notas'], axis=1)

	df = pd.concat([rows_w_num, rows_with_national, info_reversed, info_reversed_cities]).reset_index(drop=True)
	df = df.fillna(0)

	df = df.replace({'tourist_point': {'Pajara': 'Pájara', 'Oliva (La)': 'Oliva'}})

	df = df.reindex(columns = ['tourist_point', 'category', 'Valor', 'Fecha'])
	df = df.rename(columns = {'Valor': 'value', 'Fecha':'date'})
	df = df.reset_index()

	df = df.replace({'tourist_point':{'Calpe/Calp':'Calp','Javea/Xabia':'Javea','Palma De Mallorca':'Palma de Mallorca','Iruela (La)':'La Iruela','Segura De La Sierra':'Segura de la Sierra','San Bartolomé De Tirajana':'San Bartolomé de Tirajana','Tias':'Tías','Paso (El)':'El Paso','Puerto De La Cruz':'Puerto de la Cruz', 'San Miguel De Abona':'San Miguel de Abona', 'San Sebastian De La Gomera':'San Sebastián de la Gomera', 'Santa Cruz De La Palma':'Santa Cruz de la Palma', 'Santiago Del Teide':'Santiago del Teide', 'Vitoria-Gasteiz':'Vitoria-Gastéiz', 'Alicante/Alacant':'Alicante','Pamplona/Iruña':'Pamplona'}})

	df.to_excel(path_clean+file_name)

	return


def ipap_mod(url, file_name, path_raw, path_clean):

	# Request to INE API and first selection of data
	json_df = get_data_and_create_file(url, file_name, path_raw)
	df = normalize_json(json_df)

	df = df.loc[df['info'].str.contains('Dato base')]
	df['category'] = df['info'].apply(lambda x: x.split('.')[1])
	df['category'] = df['category'].apply(lambda x: x.lstrip())
	df = df.drop(['info', 'Notas'], axis= 1)

	df = df.fillna(0)

	df = df.reindex(columns = ['category', 'Valor', 'Fecha'])
	df = df.rename(columns = {'Valor': 'value', 'Fecha':'date'})
	df = df.reset_index(drop=True)

	df.to_excel(path_clean+file_name)

	return


def ipap_rate(url, file_name, path_raw, path_clean):

    # Request to INE API and first selection of data
    json_df = get_data_and_create_file(url, file_name, path_raw)
    df = normalize_json(json_df)

    df = df.loc[df['info'].str.contains('Dato base')]
    df['category'] = df['info'].apply(lambda x: x.split('.')[1])
    df['category'] = df['category'].apply(lambda x: x.lstrip())
    df = df.drop(['info', 'Notas'], axis= 1)

    df = df.fillna(0)
    df = df.reindex(columns = ['category', 'Valor', 'Fecha'])
    df = df.rename(columns = {'Valor': 'value', 'Fecha':'date'})
    df = df.reset_index(drop=True)

    return df.to_excel(path_clean+file_name)



######### MACROFUNCTION TO CALL ALL THE SPECIFIC DATASET FUNCTIONS, GET DATA FROM INE AND STORE IT AT ONCE #############

def get_data_INE_and_create_excel_files(path_raw, path_clean):

    get_tourists_by_origin('https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/24746?nult=10', 'turism_expenditure_by_ccaa_origin.xlsx', path_raw, path_clean)
        
    get_tourist_by_expenditure('https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/24745?nult=10','turism_expenditure_by_ccaa_item.xlsx',path_raw, path_clean)

    get_tourist_by_stay('https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/23993?date=20150101:20220601', 'turism_expenditure_by_stay.xlsx', path_raw, path_clean)
        

    get_tourists_by_sex_gender('https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/24744?date=20150101:20220601', 'turism_expenditure_by_sex_and_age.xlsx', path_raw, path_clean)

    tourists_by_motive('https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/23995?nult=10', 'turism_expenditure_by_trip_motive.xlsx', path_raw, path_clean)

    num_tourists_destiny('https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/10823?date=20151001:20220601', 'num_turists_by_ccaa.xlsx', path_raw, path_clean)

    num_tourists_stay('https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/10826?date=20151001:20220601', 'num_turists_by_stay.xlsx', path_raw, path_clean)

    num_tourists_motive('https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/23985?nult=10', 'num_turists_by_motive.xlsx', path_raw, path_clean)

    num_tourists_origin('https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/10822?date=20151001:20220601', 'num_turists_by_origin.xlsx', path_raw, path_clean)

    hotel_nights('https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/49370?date=20050101:20220701', 'hotels_nights.xlsx', path_raw, path_clean)

    hotel_overview('https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/49372?date=20050101:20220701', 'hotels_overview.xlsx', path_raw, path_clean)

    hotel_adr('https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/46298?date=20050101:20220701', 'hotels_adr.xlsx', path_raw, path_clean)

    apartments_nights('https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/49376?date=20050101:20220816', 'apart_nights.xlsx', path_raw, path_clean)

    apartments_overview('https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/49378?date=20050101:20220816', 'apart_overview.xlsx', path_raw, path_clean)

    ipap_mod('https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/1989?date=20050101:20220816', 'ipap_mod.xlsx', path_raw, path_clean)

    ipap_rate('https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/2050?date=20050101:20220816', 'ipap_rate.xlsx', path_raw, path_clean)

    return 


################# FUNCTIONS FOR EXPLORATORY DATA ANALYSIS #################



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
