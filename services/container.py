#!/usr/bin/env python3
from dependency_injector import containers, providers
from services.bike_service import BikeService
from services.routes_service import RouteService
from services.user_service import UserService
from services.parking_service import ParkingService
from db.db import Api

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    api_client = providers.Singleton(
        Api
    )

    parkings_service = providers.ThreadSafeSingleton(
        ParkingService,
        api = api_client,
    )

    bike_service = providers.ThreadSafeSingleton(
        BikeService,
        api = api_client,
        parkings = parkings_service
    )

    user_service = providers.ThreadSafeSingleton(
        UserService,
        api = api_client
    )

    routes_service = providers.ThreadSafeSingleton(
        RouteService,
    )
