# -*- coding: utf-8 -*-
"""data-cleaning-smartphone-data.ipynb
"""

import numpy as np
import pandas as pd

df = pd.read_csv('smartphones.csv')

df.head()

"""## Data Assessing

### Quality Issues

1. **model** - some brands are written diiferently like OPPO in model column `consistency`
2. **price** - has unneccesary '₹' `validity`
3. **price** - has ',' between numbers `validity`
4. **price** - phone Namotel has a price of 99 `accuracy`
5. **ratings** - missing values `completeness`
6. **processor** - has some incorrect values for some samsung phones(row # -642,647,649,659,667,701,750,759,819,859,883,884,919,927,929,932,1002) `validity`
7. There is ipod on row 756 `validity`
8. **memory** - incorrect values in rows (441,485,534,553,584,610,613,642,647,649,659,667,701,750,759,819,859,884,919,927,929,932,990,1002) `validity`
9. **battery** - incorrect values in rows(113,151,309,365,378,441,450,553,584,610,613,630,642,647,649,659,667,701,750,756,759,764,819,855,859,884,915,916,927,929,932,990,1002) `validity`
10. **display** - sometimes frequency is not available `completeness`
11. **display** - incorrect values in rows(378,441,450,553,584,610,613,630,642,647,649,659,667,701,750,759,764,819,859,884,915,916,927,929,932,990,1002) `validity`
12. certain phones are foldable and the info is scattered `validity`
13. **camera** - words like Dual, Triple and Quad are used to represent number of cameras and front and rear cameras are separated by '&'
14. **camera** - problem with rows (100,113,151,157,161,238,273,308,309,323,324,365,367,378,394,441,450,484,506,534,553,571,572,575,584,610,613,615,630,642,647,649,659,667,684,687,705,711,723,728,750,756,759,764,792,819,846,854,855,858,883,884,896,915,916,927,929,932,945,956,990,995,1002,1016
) `validity`
15. **card** - sometimes contains info about os and camera `validity`
16. **os** - sometimes contains info about bluetooth and fm radio `validity`
17. **os** - issue with rows (324,378) `validity`
18. **os** - sometimes contains os version name like lollipop `consistency`
19. missing values in camera, card and os `completeness`
20. datatype  of price and rating is incorrect `validity`



### Tidiness Issues

1. **sim** - can be split into 3 cols has_5g, has_NFC, has_IR_Blaster
2. **ram** - can be split into 2 cols RAM and ROM
3. **processor** - can be split into processor name, cores and cpu speed.
4. **battery** - can be split into battery capacity, fast_charging_available
5. **display** - can be split into size, resolution_width, resolution_height and frequency
6. **camera** - can be split into front and rear camera
7. **card** - can be split into supported, extended_upto
"""

df.info()

df.describe()

df.duplicated().sum()

# make a copy
df1 = df.copy()

df1['price'] = df1['price'].str.replace('₹','').str.replace(',','').astype('int')

df1

df1 = df1.reset_index()

df1['index'] = df1['index'] + 2

df1

processor_rows = set((642,647,649,659,667,701,750,759,819,859,883,884,919,927,929,932,1002))
ram_rows = set((441,485,534,553,584,610,613,642,647,649,659,667,701,750,759,819,859,884,919,927,929,932,990,1002))
battery_rows = set((113,151,309,365,378,441,450,553,584,610,613,630,642,647,649,659,667,701,750,756,759,764,819,855,859,884,915,916,927,929,932,990,1002))
display_rows = set((378,441,450,553,584,610,613,630,642,647,649,659,667,701,750,759,764,819,859,884,915,916,927,929,932,990,1002))
camera_rows = set((100,113,151,157,161,238,273,308,309,323,324,365,367,378,394,441,450,484,506,534,553,571,572,575,584,610,613,615,630,642,647,649,659,667,684,687,705,711,723,728,750,756,759,764,792,819,846,854,855,858,883,884,896,915,916,927,929,932,945,956,990,995,1002,1016 ))

df1[df1['index'].isin(processor_rows | ram_rows | battery_rows | display_rows | camera_rows)]

df1[df1['index'].isin(processor_rows & ram_rows & battery_rows & display_rows & camera_rows)]

df1 = df1[df1['price'] >= 3400]

df1

df1[df1['index'].isin(processor_rows)]

df1.drop([645,857,882,925],inplace=True)

df1[df1['index'].isin(ram_rows)]

df1.drop(582,inplace=True)

df1[df1['index'].isin(battery_rows)]

df1.drop([376,754],inplace=True)

temp_df = df1[df1['index'].isin(battery_rows)]

x = temp_df.iloc[:,7:].shift(1,axis=1).values

df1.loc[temp_df.index,temp_df.columns[7:]] = x

df1[df1['index'].isin(display_rows)]

len(display_rows)

len(camera_rows)

df1[df1['index'].isin(camera_rows)]
# 155 271

df1.drop([155, 271],inplace=True)

temp_df = df1[df1['index'].isin(camera_rows)]

temp_df = temp_df[~temp_df['camera'].str.contains('MP')]

df1.loc[temp_df.index, 'camera'] = temp_df['card'].values

df1['card'].value_counts()

temp_df = df1[df1['card'].str.contains('MP')]

df1.loc[temp_df.index,'card'] = 'Memory Card Not Supported'

df1['card'].value_counts()

pd.set_option('display.max_rows', None)

temp_df = df1[~df1['card'].str.contains('Memory Card')]

df1.loc[temp_df.index,'os'] = temp_df['card'].values

df1.loc[temp_df.index,'card'] = 'Memory Card Not Supported'

df1['card'].value_counts()

df1['os'].value_counts()

temp_df = df1[df1['os'] == 'Bluetooth']

df1.loc[temp_df.index,'os'] = np.nan

df1.head()

df1['display'].value_counts()

(982/1020)*100

df1

df1.info()

brand_names = df1['model'].str.split(' ').str.get(0)

df1.insert(1,'brand_name',brand_names)

df1['brand_name'] = df1['brand_name'].str.lower()

has_5g = df1['sim'].str.contains('5G')
has_nfc = df1['sim'].str.contains('NFC')
has_ir_blaster = df1['sim'].str.contains('IR Blaster')

df1.insert(6,'has_5g',has_5g)
df1.insert(7,'has_nfc',has_nfc)
df1.insert(8,'has_ir_blaster',has_ir_blaster)

processor_name = df1['processor'].str.split(',').str.get(0)

num_cores = df1['processor'].str.split(',').str.get(1)

processor_speed = df1['processor'].str.split(',').str.get(2)

df1.insert(10,'processor_name',processor_name)
df1.insert(11,'num_cores',num_cores)
df1.insert(12,'processor_speed',processor_speed)

df1['processor_name'] = df1['processor_name'].str.strip()

temp_df = df1[df1['processor_name'].str.contains('Core')][['processor_name', 'num_cores',	'processor_speed']].shift(1,axis=1)

temp_df.shape

df1.loc[temp_df.index,['processor_name', 'num_cores',	'processor_speed']] = temp_df.values

df1.loc[856]

df1.loc[856,'processor_name'] = 'Mediatek MT6739'

processor_brand = df1['processor_name'].str.split(' ').str.get(0).str.lower()

df1.insert(11,'processor_brand',processor_brand)

df1['num_cores'] = df1['num_cores'].str.strip()

df1['num_cores'] = df1['num_cores'].str.replace('Octa Core Processor','Octa Core').str.replace('Hexa Core Processor','Hexa Core')

df1['processor_speed'] = df1['processor_speed'].str.strip().str.split(' ').str.get(0).str.replace('\u2009',' ').str.split(' ').str.get(0).astype(float)

df1.head()

ram_capacity = df1['ram'].str.strip().str.split(',').str.get(0).str.findall(r'\b(\d+)\b').str.get(0)

df1.insert(16,'ram_capacity',ram_capacity)

df1.head()

internal_memory = df1['ram'].str.strip().str.split(',').str.get(1).str.strip().str.findall(r'\b(\d+)\b').str.get(0)

df1.insert(17,'internal_memory',internal_memory)

df1['ram_capacity'] = df1['ram_capacity'].astype(float)

df1.drop([486,627],inplace=True)

df1.loc[[483], ['ram_capacity','internal_memory']] = [12.0,'512']

df1['ram_capacity'].value_counts()

df1['internal_memory'] = df1['internal_memory'].astype(float)

temp_df = df1[df1['internal_memory'] == 1]

df1.loc[temp_df.index,'internal_memory'] = 1024

df1['internal_memory'].value_counts()

battery_capacity = df1['battery'].str.strip().str.split('with').str.get(0).str.strip().str.findall(r'\b(\d+)\b').str.get(0).astype(float)

df1.insert(16,'battery_capacity',battery_capacity)

fast_charging = df1['battery'].str.strip().str.split('with').str.get(1).str.strip().str.findall(r'\d{2,3}')

df1.insert(17,'fast_charging',fast_charging)

def fast_charging_extractor(item):

  if type(item) == list:
    if len(item) == 1:
      return item[0]
    else:
      return 0
  else:
    return -1

df1['fast_charging'] = df1['fast_charging'].apply(fast_charging_extractor).astype(int)

screen_size = df1['display'].str.strip().str.split(',').str.get(0).str.strip().str.split(' ').str.get(0).astype(float)

df1.insert(21,'screen_size',screen_size)

resolution = df1['display'].str.strip().str.split(',').str.get(1).str.strip().str.split('px').str.get(0)

df1.insert(22,'resolution',resolution)

refresh_rate = df1['display'].str.strip().str.split(',').str.get(2).str.strip().str.findall(r'\d{2,3}').str.get(0).apply(lambda x: 60 if pd.isna(x) else x).astype(int)

df1.insert(22,'refresh_rate',refresh_rate)

df1.head()

def camera_extractor(text):

  if 'Quad' in text:
    return '4'
  elif 'Triple' in text:
    return '3'
  elif 'Dual' in text:
    return '2'
  elif 'Missing' in text:
    return 'Missing'
  else:
    return '1'

num_rear_cameras = df1['camera'].str.strip().str.split('&').str.get(0).apply(camera_extractor)

df1.insert(25,'num_rear_cameras',num_rear_cameras)

num_front_cameras = df1['camera'].str.strip().str.split('&').str.get(1).str.strip().fillna('Missing').apply(camera_extractor)

df1.insert(26,'num_front_cameras',num_front_cameras)

df1.head()

df1[df1['num_front_cameras'] == 'Missing']

pd.set_option('display.max_columns',None)

df1.head()

#df1[df1['camera'] == 'Foldable Display, Dual Display']
df1.loc[69,'camera'] == '50 MP'

temp_df = df1[df1['camera'] == 'Foldable Display, Dual Display']

df1.loc[temp_df.index, 'camera'] = '50 MP'

df1['primary_camera_rear'] = df1['camera'].str.split(' ').str.get(0).str.replace('\u2009',' ').str.split(' ').str.get(0)

df1['primary_camera_front'] = df1['camera'].str.split('&').str.get(1).str.strip().str.split(' ').str.get(0).str.replace('\u2009',' ').str.split(' ').str.get(0)

df1.head()

df1[df1['card'] == 'Memory Card (Hybrid)']

df1.loc[temp_df.index, 'card'] = 'Not Specified'

df1['extended_memory'] = df1['card'].apply(lambda x:'0' if 'Not' in x else x.split('upto')).str.get(-1).str.strip().str.replace('Memory Card Supported','Not Specified')

df1.head()

df1[df1['os'].str.contains('Memory Card')]

df1.loc[temp_df.index, 'os'] = 'Not Specified'

df1['os'].value_counts()

def os_extractor(text):

  if 'Android' in text:
    return 'android'
  elif 'iOS' in text:
    return 'ios'
  elif 'Not Specified':
    return text
  elif 'Harmony' in text or 'Hongmeng' in text or 'EMUI' in text:
    return 'other'

df1['os'] = df1['os'].apply(os_extractor)

export_df = df1.drop(columns=['index','sim','processor','ram','battery','display','camera','card'])

export_df.to_csv('smartphone_cleaned_v2.csv',index=False)
