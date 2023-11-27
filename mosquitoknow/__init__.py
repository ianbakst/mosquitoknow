import logging as log
from os.path import basename, dirname, isfile
from typing import Optional

import connexion
from connexion import FlaskApp
from connexion.options import SwaggerUIOptions
from connexion.resolver import RestyResolver
from pkg_resources import resource_filename

from . import api
from . import demo


LOGGER = log.getLogger(__name__)
LOGGER.addHandler(log.NullHandler())

from .log import enable as enable_logging


def create_app(api_spec: Optional[str] = None) -> FlaskApp:
    swagger_ui_options = SwaggerUIOptions(
        swagger_ui=True,
        swagger_ui_path="docs",
    )
    LOGGER.info("Assembling app.")
    if api_spec is None:
        LOGGER.info("Using default api spec")
        api_spec = resource_filename("mosquitoknow", "data/openapi.yaml")
    api_spec_dir = dirname(api_spec)
    app = connexion.App(
        __name__,
        specification_dir=api_spec_dir,
        swagger_ui_options=swagger_ui_options,
    )
    api_spec_file = basename(api_spec) if isfile(api_spec) else "openapi.yaml"
    app.add_api(api_spec_file, resolver=RestyResolver("mosquitoknow.api"))
    return app
