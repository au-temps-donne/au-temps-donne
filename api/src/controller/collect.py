from flask_restful import Resource, reqparse, inputs, abort
from service.collect import CollectService
from exception.collect import *
from exception.vehicle import *
from exception.demand import *
from exception.storage import StorageIdNotFoundException
from exception.demand import CollectsDemandAlreadyExistsException
from flask import jsonify
from flask_jwt_extended import jwt_required
from function.roles_required import roles_required

class CollectCheckArgs:

    pattern = {'datetime': r'\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\b'}  # format : YYYY-MM-DD.
        
    
    def get_collect_args(self) -> dict:
        parser = reqparse.RequestParser()
        parser.add_argument('datetime', type=inputs.regex(self.pattern['datetime']), required=True, help="Invalid or missing parameter 'datetime'.")
        parser.add_argument('status', type=int, required=True, help="Invalid or missing parameter 'status'.")
        parser.add_argument('demands', type=int, required=True, action='append', help="Invalid or missing parameter 'demands'.")
        parser.add_argument('vehicle_id', type=int, required=True, help="Invalid or missing parameter 'vehicle_id.")
        parser.add_argument('storage_id', type=int, required=True, help="Invalid or missing parameter 'storage_id.")
        
        args = parser.parse_args(strict=True)
        return args


class CollectController(Resource):

    def __init__(self) -> None:
        self.check_args = CollectCheckArgs()
        self.collect_service = CollectService()

    @jwt_required()
    def get(self, collect_id: int):
        try:
            collect = self.collect_service.select_one_by_id(collect_id=collect_id)
            return jsonify(collect.json())
        except CollectIdNotFoundException as e:
            abort(http_status_code=404, message=str(e))
        except CollectAccessDbException as e:
            abort(http_status_code=500, message=str(e))
        except VehicleAccessDbException as e:
            abort(http_status_code=500, message=str(e))
   
    @jwt_required()
    @roles_required([1])
    def put(self, collect_id: int):
        try:
            args = self.check_args.get_collect_args()
            self.collect_service.update(collect_id=collect_id, args=args)
            return jsonify({'message': f"Collect '{collect_id}' successfully updated."})
        except CollectIdNotFoundException as e:
            abort(http_status_code=404, message=str(e))
        except VehicleIdNotFoundException as e:
            abort(http_status_code=404, message=str(e))
        except CollectAccessDbException as e:
            abort(http_status_code=500, message=str(e)) 
        except StorageIdNotFoundException as e:
            abort(http_status_code=404, message=str(e))       
   
    @jwt_required()
    @roles_required([1])
    def delete(self, collect_id: int):
        try:
            self.collect_service.delete(collect_id=collect_id)
            return jsonify({'message': f"Collect '{collect_id}' successfully deleted."})
        except CollectIdNotFoundException as e:
            abort(http_status_code=404, message=str(e))
        except CollectAccessDbException as e:
            abort(http_status_code=500, message=str(e)) 
            
   
    
class CollectListController(Resource):
    def __init__(self) -> None:
        self.check_args = CollectCheckArgs()
        self.collect_service = CollectService()
    
    @jwt_required()
    def get(self):
        try:
            collects = self.collect_service.select_all()
            if collects:
                return jsonify([collect.json() for collect in collects])
            else:
                return jsonify({'message': "No collects found."})
        except CollectAccessDbException as e:
            abort(http_status_code=500, message=str(e))
        
    @jwt_required()
    @roles_required([1])
    def post(self):
        try:
            args = self.check_args.get_collect_args()
            self.collect_service.insert(args=args)
            return jsonify({'message': f"Collect successfully created."})
        except CollectAccessDbException as e:
            abort(http_status_code=500, message=str(e))
        except CollectsDemandAlreadyExistsException as e:
            abort(http_status_code=400, message=str(e))
        except VehicleIdNotFoundException as e:
            abort(http_status_code=404, message=str(e))
        except DemandIdNotFoundException as e:
            abort(http_status_code=404, message=str(e))
        except VehicleAccessDbException as e:
            abort(http_status_code=500, message=str(e))
        except StorageIdNotFoundException as e:
            abort(http_status_code=404, message=str(e))



class CollectPageController(Resource):
    def __init__(self) -> None:
        self.collect_service = CollectService()
    
    @jwt_required()
    def get(self, page: int):
        try:
            collects = self.collect_service.select_per_page(page=page)
            if collects:
                return jsonify({'max_pages': collects['max_pages'], 'collects': [collect.json() for collect in collects['collects']]})
            else:
                return jsonify({'message': "No collects found."})
        except CollectAccessDbException as e:
            abort(http_status_code=500, message=str(e))
        

class CollectSearchController(Resource):
    def __init__(self) -> None:
        self.collect_service = CollectService()

    @jwt_required()
    def get(self, page: int, search: str):
        try:
            collects = self.collect_service.select_by_search(page=page, search=search)
            if collects:
                return jsonify({'max_pages': collects['max_pages'], 'collects': [collect.json() for collect in collects['collects']]})
            else:
                return jsonify({'message': "No collects found."})
        except CollectAccessDbException as e:
            abort(http_status_code=500, message=str(e))
        
