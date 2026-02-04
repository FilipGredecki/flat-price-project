import pandas as pd
import sys
import os
from sklearn.preprocessing import LabelEncoder
import joblib 


flat_data_frame = pd.read_csv(r'csv_folder/basic.csv',sep=';')

"""
delating records with wrong price
preparing good dtype
"""
flat_data_frame = flat_data_frame[(flat_data_frame['price'] // flat_data_frame['home_area'] >= 5000) & (flat_data_frame['price'] // flat_data_frame['home_area'] <= 40000)]
flat_data_frame = flat_data_frame.dropna(subset=['price', 'home_area'])
flat_data_frame['price'] = flat_data_frame['price'].astype('int')
flat_data_frame['home_area'] = flat_data_frame['home_area'].astype('float')
# print(f'price: {flat_data_frame['price'].dtype}')
# print(f'home_area: {flat_data_frame['home_area'].dtype}')

"""
rooms_count: prepraing and dtype
"""
# print(flat_data_frame['rooms_count'].unique())
flat_data_frame['rooms_count'] = flat_data_frame['rooms_count'].replace({'10+ pokoi': 15})
flat_data_frame['rooms_count'] = flat_data_frame['rooms_count'].astype(int)
# print(flat_data_frame['rooms_count'].unique())
# print(f'rooms_count: {flat_data_frame['rooms_count'].dtype}')

"""
floor: preparing values and dtype
"""
# print(flat_data_frame['floor'].unique())
flat_data_frame['floor'] = flat_data_frame['floor'].replace({'suterena' : -1, 'parter': 0, 'brak informacji': -99, '> 10':15})
flat_data_frame['floor'] = flat_data_frame['floor'].fillna(-99)
flat_data_frame['floor'] = flat_data_frame['floor'].astype(int)
# print(flat_data_frame['floor'].unique())
# print(f'floor: {flat_data_frame['rooms_cfloorount'].dtype}')

"""
building_height: preparing values and dtype
"""
# print(flat_data_frame['building_height'].unique())
flat_data_frame['building_height'] = flat_data_frame['building_height'].replace({'-':-99})
flat_data_frame['building_height'] = flat_data_frame['building_height'].astype(int)
flat_data_frame.loc[flat_data_frame['building_height'] > 55, 'building_height'] = -99
# print(flat_data_frame['building_height'].unique())
# print(f'building_height: {flat_data_frame['building_height'].dtype}')


""""
finishing_standard: encoding and changing dtype
"""
# print(flat_data_frame['finishing_standard'].unique())
finishing_standar_encoder = LabelEncoder()
finishing_standar_encoder.fit(flat_data_frame['finishing_standard'])
flat_data_frame['finishing_standard'] = finishing_standar_encoder.transform(flat_data_frame['finishing_standard'])
flat_data_frame['finishing_standard'] = flat_data_frame['finishing_standard'].astype(int)
joblib.dump(finishing_standar_encoder, 'encoders/finishing_standar_encoder.pkl')
# print(flat_data_frame['finishing_standard'].unique())
# print(f'finishing_standard: {flat_data_frame['finishing_standard'].dtype}')

"""
ownership_type: encoding and changing dtype
"""
# print(flat_data_frame['ownership_type'].unique())
ownership_type_encoder = LabelEncoder()
ownership_type_encoder.fit(flat_data_frame['ownership_type'])
flat_data_frame['ownership_type'] = ownership_type_encoder.transform(flat_data_frame['ownership_type'])
flat_data_frame['ownership_type'] = flat_data_frame['ownership_type'].astype(int)
joblib.dump(ownership_type_encoder,'encoders/ownership_type_encoder.pkl')
# print(flat_data_frame['ownership_type'].unique())
# print(f'ownership_type: {flat_data_frame['ownership_type'].dtype}')

"""
building_type: encoding and changing dtype
"""
# print(flat_data_frame['building_type'].unique())
building_type_encoder = LabelEncoder()
building_type_encoder.fit(flat_data_frame['building_type'])
flat_data_frame['building_type'] = building_type_encoder.transform(flat_data_frame['building_type'])
flat_data_frame['building_type'] = flat_data_frame['building_type'].astype(int)
joblib.dump(building_type_encoder,'encoders/building_type_encoder.pkl')
# print(flat_data_frame['building_type'].unique())
# print(f'building_type: {flat_data_frame['building_type'].dtype}')

"""
elevator: encoding and changing dtype
"""
# print(flat_data_frame['elevator'].unique())
flat_data_frame['elevator'] = flat_data_frame['elevator'].replace({'nie': 0,'tak': 1})
flat_data_frame['elevator'] = flat_data_frame['elevator'].astype(int)
# print(flat_data_frame['elevator'].unique())
# print(f'elevator: {flat_data_frame['elevator'].dtype}')
flat_data_frame.to_csv('csv_folder/half_prepared.csv', sep=';',index=False)