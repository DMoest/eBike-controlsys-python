#!/usr/bin/env python3
from dependency_injector import containers, providers

from services.bike_service import BikeService
from services.routes_service import RouteService
from services.user_service import UserService

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    bike_service = providers.Singleton(
        BikeService,
        
    )

    user_service = providers.Singleton(
        UserService
    )

    routes_service = providers.Singleton(
        RouteService
    )
