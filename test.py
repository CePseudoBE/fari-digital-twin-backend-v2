import dotenv

dotenv.load_dotenv()

from sources.dott import DottGeofenceCollector, DottVehiclePositionCollector, DottVehicleTypeCollector
from sources.infrabel import InfrabelLineSectionCollector, InfrabelOperationalPointsCollector, \
    InfrabelPunctualityCollector, InfrabelSegmentsCollector
from sources.lime import LimeVehiclePositionCollector, LimeVehicleTypeCollector
from sources.pony import PonyGeofenceCollector, PonyVehiclePositionCollector, PonyVehicleTypeCollector
from sources.sibelga import SibelgaCollector
from sources.stib import STIBShapeFilesCollector, STIBVehiclePositionsCollector, STIBStopsCollector

from assets_manager.assets_manager import AssetsManager, TilesetManager, PointCloudManager, WMSCollecor
from digitaltwin_dataspace import run_components

run_components([

])