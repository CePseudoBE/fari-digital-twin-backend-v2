from digitaltwin_dataspace import run_components, AssetsManager, TilesetManager, ComponentConfiguration, servable_endpoint, Collector

class AssetsManager(AssetsManager):
    def get_configuration(self) -> ComponentConfiguration:
        return ComponentConfiguration(
            name="assets_manager",
            tags=["Assets"],
            description="Manages assets",
            content_type="model/gltf-binary",
        )
    
class PointCloudManager(AssetsManager):
    def get_configuration(self) -> ComponentConfiguration:
        return ComponentConfiguration(
            name="pointcloud_manager",
            tags=["PointCloud"],
            description="Manages point clouds",
            content_type="application/octet-stream",
        )

class TilesetManager(TilesetManager):
    def get_configuration(self) -> ComponentConfiguration:
        return ComponentConfiguration(
            name="tileset_manager",
            tags=["Tileset"],
            description="Manages tilesets",
            content_type="application/json",
        )

class DigitalTerrainManager(TilesetManager):
    def get_configuration(self) -> ComponentConfiguration:
        return ComponentConfiguration(
            name="digital_terrain_manager",
            tags=["DigitalTerrain"],
            description="Manages digital terrain",
            content_type="application/json",
        )
    
class WMSCollecor(Collector): 
    def __init__(self):
        self._layer: dict = {}

    def get_schedule(self) -> str:
        return "1d"

    def get_configuration(self) -> ComponentConfiguration:
        return ComponentConfiguration(
            name="maps_manager",
            tags=["Google"],
            description="Collects data from Google APIs",
            content_type="text/html",
        )
    
    @servable_endpoint(path="/add_layer", method="POST", response_model=str)
    def add_layer(self, layer: dict) -> str:
        self._layer = layer
        self.run()
        return "ok"
    
    
    

    def collect(self) -> bytes:
        return self._layer
