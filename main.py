import importlib
import inspect
import os
import pkgutil
from digitaltwin_dataspace import Collector, Harvester, Handler, run_components
import dotenv
dotenv.load_dotenv()

from assets_manager.assets_manager import AssetsManager, TilesetManager, PointCloudManager, WMSCollecor

SOURCE_PACKAGE = "sources"

def discover_classes_from_package(package: str, base_class):
    components = []
    package_path = os.path.join(os.path.dirname(__file__), package.replace('.', '/'))

    for finder, name, ispkg in pkgutil.iter_modules([package_path]):
        module_name = f"{package}.{name}"
        module = importlib.import_module(module_name)

        for member_name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, base_class) and obj not in (base_class,):
                components.append(obj())
    return components

collectors = discover_classes_from_package(SOURCE_PACKAGE, Collector)
harvesters = discover_classes_from_package(SOURCE_PACKAGE, Harvester)
handlers = discover_classes_from_package(SOURCE_PACKAGE, Handler)

run_components([
    *collectors,
    *harvesters,
    *handlers,
    AssetsManager(),
    TilesetManager(),
    PointCloudManager(),
    WMSCollecor(),
])
