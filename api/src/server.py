from flask import jsonify
from flask_restful import Api
from dotenv import load_dotenv, find_dotenv
import os

from database.db import db

# Import Controllers
from controller.user import *
from controller.event import *
from controller.type import *
from controller.role import *
from controller.auth import *
from controller.location import *
from controller.category import *
from controller.food import *
from controller.package import *
from controller.storage import *
from controller.warehouse import *
from controller.company import *
from controller.shop import *
from controller.delivery import *
from controller.roadmap import *
from controller.collect import *
from controller.demand import *
from controller.vehicle import *
from controller.ticket import *


# Import Models
from model.user import User
from model.event import Event
from model.role import Role
from model.type import Type
from model.location import Location
from model.category import Category
from model.food import Food
from model.package import Package
from model.storage import Storage
from model.warehouse import Warehouse
from model.company import Company
from model.shop import Shop
from model.delivery import Delivery
from model.collect import Collect
from model.demand import Demand
from model.vehicle import Vehicle
from model.ticket import Ticket

from app import app


# API Routes

api = Api(app)
prefix = "/api"
api.add_resource(UserListController, f'{prefix}/user')
api.add_resource(UserPageController, f'{prefix}/user/page/<int:page>')
api.add_resource(UserSearchController,
                 f'{prefix}/user/page/<int:page>/search/<string:search>')
api.add_resource(UserController, f'{prefix}/user/<int:user_id>')

api.add_resource(UserIsRoleController,
                 f'{prefix}/user/<int:user_id>/role/<int:role_id>')
api.add_resource(UserParticipatesEventController,
                 f'{prefix}/user/<int:user_id>/event/<int:event_id>')
api.add_resource(UserDeliversController,
                 f'{prefix}/user/<int:user_id>/delivery/<int:delivery_id>')
api.add_resource(UserCollectsController,
                 f'{prefix}/user/<int:user_id>/collect/<int:collect_id>')
api.add_resource(UserShopController,
                 f'{prefix}/user/<int:user_id>/shop/<int:shop_id>')

api.add_resource(EventController, f'{prefix}/event/<int:event_id>')
api.add_resource(EventListController, f'{prefix}/event')
api.add_resource(EventPageController, f'{prefix}/event/page/<int:page>')
api.add_resource(EventSearchPageController,
                 f'{prefix}/event/page/<int:page>/search/<string:search>')
api.add_resource(EventSearchController,
                 f'{prefix}/event/search/<string:search>')

api.add_resource(TypeListController, f'{prefix}/type')
api.add_resource(TypeController, f'{prefix}/type/<int:type_id>')

api.add_resource(RoleListController, f'{prefix}/role')
api.add_resource(RoleController, f'{prefix}/role/<int:role_id>')

api.add_resource(LocationListController, f'{prefix}/location')
api.add_resource(LocationController, f'{prefix}/location/<int:location_id>')

api.add_resource(CategoryListController, f'{prefix}/category')
api.add_resource(CategoryController, f'{prefix}/category/<int:category_id>')

api.add_resource(FoodController, f'{prefix}/food/<int:food_id>')
api.add_resource(FoodListController, f'{prefix}/food')
api.add_resource(FoodPageController, f'{prefix}/food/page/<int:page>')

api.add_resource(PackageController, f'{prefix}/package/<int:package_id>')
api.add_resource(PackageListController, f'{prefix}/package')
api.add_resource(PackagePageController, f'{prefix}/package/page/<int:page>')
api.add_resource(PackageSearchController,
                 f'{prefix}/package/page/<int:page>/search/<string:search>')
api.add_resource(PackageQrCodeController,
                 f'{prefix}/package/qrcode')

api.add_resource(StorageController, f'{prefix}/storage/<int:storage_id>')
api.add_resource(StorageListController, f'{prefix}/storage')
api.add_resource(StoragePageController, f'{prefix}/storage/page/<int:page>')

api.add_resource(WarehouseController, f'{prefix}/warehouse/<int:warehouse_id>')
api.add_resource(WarehouseListController, f'{prefix}/warehouse')
api.add_resource(WarehousePageController,
                 f'{prefix}/warehouse/page/<int:page>')

api.add_resource(CompanyController, f'{prefix}/company/<int:company_id>')
api.add_resource(CompanyListController, f'{prefix}/company')

api.add_resource(ShopController, f'{prefix}/shop/<int:shop_id>')
api.add_resource(ShopListController, f'{prefix}/shop')
api.add_resource(ShopPageController, f'{prefix}/shop/page/<int:page>')
api.add_resource(ShopSearchController,
                 f'{prefix}/shop/page/<int:page>/search/<string:search>')

api.add_resource(TicketController, f'{prefix}/ticket/<int:ticket_id>')
api.add_resource(TicketListController, f'{prefix}/ticket')
api.add_resource(TicketPageController, f'{prefix}/ticket/page/<int:page>')
api.add_resource(TicketSearchController,
                 f'{prefix}/ticket/page/<int:page>/search/<string:search>')
api.add_resource(TicketUserController,
                 f'{prefix}/ticket/user/<int:user_id>')

api.add_resource(DeliveryController, f'{prefix}/delivery/<int:delivery_id>')
api.add_resource(DeliveryListController, f'{prefix}/delivery')
api.add_resource(DeliveryPageController, f'{prefix}/delivery/page/<int:page>')
# api.add_resource(ShopSearchController,
#                  f'{prefix}/shop/page/<int:page>/search/<string:search>')
api.add_resource(DeliversToLocationController,
                 f'{prefix}/delivery/<int:delivery_id>/location/<int:location_id>')

api.add_resource(CollectController, f'{prefix}/collect/<int:collect_id>')
api.add_resource(CollectListController, f'{prefix}/collect')
api.add_resource(CollectPageController, f'{prefix}/collect/page/<int:page>')

api.add_resource(DemandController, f'{prefix}/demand/<int:demand_id>')
api.add_resource(DemandListController, f'{prefix}/demand')
api.add_resource(DemandPageController, f'{prefix}/demand/page/<int:page>')

api.add_resource(VehicleController, f'{prefix}/vehicle/<int:vehicle_id>')
api.add_resource(VehicleListController, f'{prefix}/vehicle')
# api.add_resource(VehiclePageController, f'{prefix}/vehicle/page/<int:page>')
# api.add_resource(ShopSearchController,
#                  f'{prefix}/shop/page/<int:page>/search/<string:search>')
# api.add_resource(DeliversToLocationController,
#                  f'{prefix}/delivery/<int:delivery_id>/location/<int:location_id>')


api.add_resource(RoadmapController, f'{prefix}/roadmap')

api.add_resource(RegisterController, f'{prefix}/register')
api.add_resource(LoginController, f'{prefix}/login')
api.add_resource(ProtectedController, f'{prefix}/protected')
api.add_resource(RefreshTokenController, f'{prefix}/token/refresh')


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    db.init_app(app)
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
