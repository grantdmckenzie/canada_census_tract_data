import sys
import pandas as pd
import geopandas as gp

if len(sys.argv) == 3:
	ids = sys.argv[1].strip().split(',')
	mf = False
	outputname = sys.argv[2]
elif len(sys.argv) == 4:
	ids = sys.argv[1].strip().split(',')
	mf = True
	outputname = sys.argv[2]
else:
	print('At least argments are required:\n\t1. Comma delimited set of attribute IDs\n\t2. Name of output file\n\t3. Include male/female data (optional).\n')
	exit()


ids = [eval(i) for i in ids]

gdf = gp.read_file('canada_census_tracts.shp')

lookup = pd.read_csv('lookup.csv', header=None, encoding='latin_1',sep='\t')

data = pd.read_csv('98-401-X2021007_English_CSV_data.csv', header=0, encoding='latin_1')

cols = ['DGUID','GEO_LEVEL','CHARACTERISTIC_ID','C1_COUNT_TOTAL','C2_COUNT_MEN+','C3_COUNT_WOMEN+']
data = data[cols]

data = data.loc[data['GEO_LEVEL'] == 'Census tract']

data2 = data[['DGUID','GEO_LEVEL','CHARACTERISTIC_ID', 'C1_COUNT_TOTAL']]

# TOTAL POPULATION
newdf = data2.loc[data['CHARACTERISTIC_ID'] == 1]
newdf = newdf.rename({'C1_COUNT_TOTAL': 'Total Population'}, axis='columns')
newdf = newdf.drop('CHARACTERISTIC_ID', axis=1)
newdf = newdf.drop('GEO_LEVEL', axis=1)

#ids = [369,370,371,372,373]

for i in ids:
	tmp = data.loc[data['CHARACTERISTIC_ID'] == i]
	name = lookup[lookup[0] == i][1].item() + '.T'
	newdf[name] = tmp['C1_COUNT_TOTAL'].tolist()
	if mf:
		name = lookup[lookup[0] == i][1].item() + '.M'
		newdf[name] = tmp['C2_COUNT_MEN+'].tolist()
		name = lookup[lookup[0] == i][1].item() + '.F'
		newdf[name] = tmp['C3_COUNT_WOMEN+'].tolist()


output = gdf.merge(newdf, on='DGUID')
output.to_file(outputname, driver='GeoJSON')