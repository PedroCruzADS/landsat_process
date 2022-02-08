import glob
import pathlib
from datetime import datetime
from re import L
from typing import OrderedDict

import rasterio as rio
from shapely.geometry import box

DATETIME_FORMAT="%Y-%m-%d %H:%M:%S"

def check_missing_keys(data, required_keys):
    if data:
        data_keys = set(data.keys())
        missing_keys =  required_keys - data_keys
        if missing_keys:
            raise AttributeError(f"Missing keys: {missing_keys}")

class RemoteScene(dict):
    """The Remote Scene object."""
    
    __required_keys = {'id', 'base_url','sensing_time', 'platform', 'instrument'}
    def __init__(self, data, validate=True):
        """Initialize instance with dictionary data.

        :param data: Dict with RemoteScene metadata.
        """
        
        if validate:
            check_missing_keys(data, RemoteScene.__required_keys)

        super(RemoteScene, self).__init__(data or {})

    @property
    def id(self):
        """:return: the Scene id"""
        return self['id']
    
    @property
    def base_url(self):
        """:return: the Scene base url."""
        return self['base_url']
    
    @property
    def sensing_time(self):
        """:return: the Scene sensing_time."""
        return self['sensing_time']

    @property
    def platform(self):
        """:return: the Scene platform."""
        return self['platform']

    @property
    def instrument(self):
        """:return: the Scene instrument."""
        return self['instrument']

class LocalScene(dict):
    """The Local Scene object."""
    
    __required_keys = {'remote_id', 'path', 'sensing_time', 'platform', 'instrument', 'lineage'}
    def __init__(self, data, validate=True):
        """Initialize instance with dictionary data.

        :param data: Dict with LocalScene metadata.
        """
        
        if validate:
            check_missing_keys(data, LocalScene.__required_keys)

        super(LocalScene, self).__init__(data or {})
    
    @property
    def remote_id(self):
        """:return: the Scene remote_id."""
        return self['remote_id']
    
    @property
    def path(self):
        """:return: the Scene path."""
        return self['path']
    
    @property
    def sensing_time(self):
        """:return: the Scene sensing_time."""
        return self['sensing_time']

    @property
    def platform(self):
        """:return: the Scene platform."""
        return self['platform']

    @property
    def instrument(self):
        """:return: the Scene instrument."""
        return self['instrument']

    @property
    def measurements(self):
        """:return: the Scene measurements."""
        return self['measurements'] if 'measurements' in self else {}

    def add_measurement(self, name, path):
        if 'measurements' not in self:
            self['measurements'] = dict()
        self['measurements'][name] = {
                "path": path
            }

    def load_measurements_metadata(self):
        downloaded_files = glob.glob(f"{self.path}/*.TIF")
        for file_path in downloaded_files:
            fp=pathlib.Path(file_path)
            m_name = fp.stem.split("_")[-1]
            self.add_measurement(m_name, file_path)
    
    @property
    def lineage(self):
        """:return: the Scene lineage."""
        return self['lineage']

class IndexedScene(dict):
    """The Indexed Scene object."""
    
   
    def __init__(self, data):
        """Initialize instance with dictionary data.

        :param data: Dict with metadata_doc from ODC Datase).
        """
        super(IndexedScene, self).__init__(data or {})

    @property
    def id(self):
        return self['id']

    @property
    def crs(self):
        return self['crs']

    @property
    def grids(self):
        return self['grids']
    
    @property
    def extent(self):
        return self['extent']
    
    @property
    def lineage(self):
        return self['lineage']

    @property
    def schema(self):
        return self['$schema']
    
    @property
    def lineage(self):
        return self['lineage']

    @property
    def product(self):
        return self['product']

    @property
    def geometry(self):
        return self['geometry']

    @property
    def properties(self):
        return self['properties']

    @property
    def grid_spatial(self):
        return self['grid_spatial']

    @property
    def measurements(self):
        return self['measurements']

def localscene_to_odc_item(local_scene: LocalScene, dc_product) -> dict:
        import uuid
        dc_item = OrderedDict()
        dc_item["$schema"] = "https://schemas.opendatacube.org/dataset"
        
        dc_item['id'] = str(uuid.uuid5(uuid.NAMESPACE_URL, local_scene.path))

        # product signature        

        dc_item["product"] = OrderedDict({
            "name": dc_product['name']
        })
        
        dc_item["crs"] = dc_product['storage']['crs']

        dc_item["properties"] = OrderedDict({
            "datetime": local_scene.sensing_time,
            "eo:platform": "Landsat",
            "eo:instrument": local_scene.instrument,
            'mq:local_scene': dict(local_scene)
        })

        dc_item["measurements"] = OrderedDict()
                 
        for key in local_scene.measurements.keys():
            dc_item["measurements"][key] = OrderedDict({
                "path": local_scene.measurements[key]['path']
            })
            # just for the first item, collect some geo metatada
            if "grids" not in dc_item:
                datasource = rio.open(local_scene.measurements[key]['path'])

                dc_item["grids"] = OrderedDict({
                    "default": {
                    "shape": list(datasource.shape),
                    "transform": list(datasource.transform)
                    }
                })
                bounds = datasource.bounds
                
                dc_item["geometry"] = OrderedDict({
                    "type": "Polygon",
                    "coordinates": [[
                     [bounds.left, bounds.top],     # left, top
                     [bounds.right, bounds.top],    # right, top
                     [bounds.right, bounds.bottom], # right, bottom
                     [bounds.left, bounds.bottom],  # left, bottom
                     [bounds.left, bounds.top]      # left, top
                    ]]
                })
        
        dc_item["lineage"] = dict(local_scene.lineage)
        
        return dc_item

class LandsatScene(dict):
    """The LandsatScene object."""
    
    required_keys = {'scene_id', 'product_id', 'spacecraft_id', 'sensor_id', 'date_acquired', 'collection_number', 'collection_category', 'sensing_time', 'data_type', 'wrs_path', 'wrs_row', 'cloud_cover', 'north_lat', 'south_lat', 'west_lon', 'east_lon', 'total_size', 'base_url'}
    optional_keys = {'download_path', 'measurements', 'odc_dataset'}
    def __init__(self, data, validate=True):
        """Initialize instance with dictionary data.

        :param data: Dict with RemoteScene metadata.
        """
        
        if validate:
            check_missing_keys(data, LandsatScene.required_keys)

        data = LandsatScene.__datetime_fields_to_string(data)

        super(LandsatScene, self).__init__(data or {})


    @staticmethod
    def __datetime_fields_to_string(data):
        for key in ['sensing_time', 'date_acquired']:
            if type(data[key]) is not str:
                data[key] = data[key].strftime(DATETIME_FORMAT)
        return data

    @property
    def id(self):
        """:return: the Scene id."""
        return self['scene_id']

    @property
    def product_id(self):
        """:return: the Scene product id."""
        return self['product_id']

    @property
    def spacecraft_id(self):
        """:return: the Scene spacecraft id."""
        return self['spacecraft_id']

    @property
    def sensor_id(self):
        """:return: the Scene sensor id."""
        return self['sensor_id']

    @property
    def date_acquired(self):
        """:return: the Scene date acquired."""
        return datetime.strptime(self["date_acquired"], DATETIME_FORMAT)

    @property
    def collection_number(self):
        """:return: the Scene collection number."""
        return self['collection_number']

    @property
    def collection_category(self):
        """:return: the Scene collection category."""
        return self['collection_category']

    @property
    def sensing_time(self):
        """:return: the Scene sensing time."""
        return datetime.strptime(self["sensing_time"], DATETIME_FORMAT)

    @property
    def data_type(self):
        """:return: the Scene data type."""
        return self['data_type']

    @property
    def wrs_path(self):
        """:return: the Scene wrs path."""
        return self['wrs_path']

    @property
    def wrs_row(self):
        """:return: the Scene wrs row."""
        return self['wrs_row']

    @property
    def cloud_cover(self):
        """:return: the Scene cloud cover."""
        return self['cloud_cover']

    @property
    def north_lat(self):
        """:return: the Scene north lat."""
        return self['north_lat']

    @property
    def south_lat(self):
        """:return: the Scene south lat."""
        return self['south_lat']

    @property
    def west_lon(self):
        """:return: the Scene west lon."""
        return self['west_lon']

    @property
    def east_lon(self):
        """:return: the Scene east lon."""
        return self['east_lon']

    @property
    def total_size(self):
        """:return: the Scene total size."""
        return self['total_size']

    @property
    def base_url(self):
        """:return: the Scene base url."""
        return self['base_url']

    @property
    def download_path(self):
        """:return: the Scene download path."""
        return self['download_path'] if 'download_path' in self else None
    
    @property
    def is_dowloaded(self):
        return 'download_path' in self

    @download_path.setter
    def download_path(self, value):
        self['download_path'] = value

    @property
    def measurements(self) -> dict:
        """:return: the Scene measurements."""
        return self['measurements'] if 'measurements' in self else {}

    @property
    def odc_dataset(self):
        return self['odc_dataset'] if 'odc_dataset' in self else {}
    
    @odc_dataset.setter
    def odc_dataset(self, value):
        self['odc_dataset'] = value



    

    

