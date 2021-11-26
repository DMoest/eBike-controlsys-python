#!/usr/bin/env python3
from dependency_injector import containers, providers

from services.bike_service import BikeService
from services.routes_service import RouteService
from services.user_service import UserService
from db.db import Api

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    api_client = providers.Singleton(
        Api
    )

    bike_service = providers.Singleton(
        BikeService,
        api = api_client
    )

    user_service = providers.Singleton(
        UserService,
        api = api_client
    )

    routes_service = providers.Singleton(
        RouteService,
    )
