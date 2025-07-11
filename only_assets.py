import dotenv
dotenv.load_dotenv()

from sources.bolt import BoltGeofenceCollector, BoltVehiclePositionCollector, BoltVehicleTypeCollector
from sources.brussels_mobility import BrusselsMobilityBikeCountersCollector, BrusselsMobilityBikeCountsCollector, BrusselsMobilityTrafficDevicesCollector
from sources.de_lijn import DeLijnGTFSStaticCollector, DeLijnGTFSRealtimeCollector
from sources.dott import DottGeofenceCollector, DottVehiclePositionCollector, DottVehicleTypeCollector
from sources.energy import EnergyCollector
from sources.fixmystreet import FixMyStreetIncidentsCollector, FixMyStreetHistoryHarvester
from sources.infrabel import InfrabelLineSectionCollector, InfrabelOperationalPointsCollector, InfrabelPunctualityCollector, InfrabelSegmentsCollector
from sources.irceline import IrcelineSOSCollector
from sources.lime import LimeVehiclePositionCollector, LimeVehicleTypeCollector
from sources.opensky import OpenSkyCollector
from sources.pony import PonyGeofenceCollector, PonyVehiclePositionCollector, PonyVehicleTypeCollector
from sources.sensor_community import SensorCommunityCollector
from sources.sibelga import SibelgaCollector
from sources.sncb import SNCBGTFSStaticCollector, SNCBGTFSRealtimeCollector
from sources.stib import STIBGTFSCollector, STIBShapeFilesCollector, STIBVehiclePositionsCollector, STIBStopsCollector
from sources.tec import TECGTFSStaticCollector, TECGTFSRealtimeCollector
from sources.telraam import TelraamTrafficCollector

from assets_manager.assets_manager import AssetsManager, TilesetManager, PointCloudManager, WMSCollecor, DigitalTerrainManager
from digitaltwin_dataspace import run_components

run_components([
    AssetsManager(),
    TilesetManager(),
    PointCloudManager(),
    WMSCollecor(),
    DigitalTerrainManager(),
])
