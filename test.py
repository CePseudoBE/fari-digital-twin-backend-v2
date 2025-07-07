import dotenv

dotenv.load_dotenv()

from sources.stib import STIBGTFSCollector, STIBShapeFilesCollector, STIBVehiclePositionsCollector, STIBStopsCollector
from sources.tec import TECGTFSStaticCollector, TECGTFSRealtimeCollector

from assets_manager.assets_manager import AssetsManager, TilesetManager, PointCloudManager, WMSCollecor
from digitaltwin_dataspace import run_components

run_components([

])