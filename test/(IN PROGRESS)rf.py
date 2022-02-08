import numpy as np
from osgeo import gdal
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn import utils

#######define inputs#######
inpRaster = '/home/pedro/IC/RGB.tiff' 
outRaster = '/home/pedro/IC/RGB_RF.tiff'
df = pd.read_csv('/home/pedro/IC/dados_secchi.csv', sep=',')

########end of inputs#####

#read training data
#enter training data bands according to your csv columns name
data = df[['secchi']]
#enter training label according to your csv column name
label = df['secchi']
del df

####no need to modify the code below###
#######################################


#open raster
ds = gdal.Open(inpRaster, gdal.GA_ReadOnly)

#get raster info
rows = ds.RasterYSize
cols = ds.RasterXSize
bands = ds.RasterCount
geo_transform = ds.GetGeoTransform()
projection = ds.GetProjectionRef()

#read as array
array = ds.ReadAsArray()
ds = None

#modify structure
array = np.stack(array,axis=2)
array = np.reshape(array, [rows*cols,bands])
test = pd.DataFrame(array, dtype='f4')
del array


#set classifier parameters and train classifier
lab_enc = preprocessing.LabelEncoder()
label_encoded = lab_enc.fit_transform(label)
clf = RandomForestClassifier(n_estimators=50,n_jobs=-1)
clf.fit(data,label_encoded)
del data
del label


#predict classes
y_pred = clf.predict(test)
del test
classification = y_pred.reshape((rows,cols))
del y_pred

def createGeotiff(outRaster, data, geo_transform, projection):
    # Create a GeoTIFF file with the given data
    driver = gdal.GetDriverByName('GTiff')
    rows, cols = data.shape
    rasterDS = driver.Create(outRaster, cols, rows, 1, gdal.GDT_Int32)
    rasterDS.SetGeoTransform(geo_transform)
    rasterDS.SetProjection(projection)
    band = rasterDS.GetRasterBand(1)
    band.WriteArray(data)
    rasterDS = None


#export classified image
createGeotiff(outRaster,classification,geo_transform,projection)

