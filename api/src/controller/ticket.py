from flask_restful import Resource, reqparse, inputs, abort
from service.ticket import TicketService
from exception.ticket import *
from exception.user import *
from flask import jsonify
from flask_jwt_extended import jwt_required
from function.roles_required import roles_required

class TicketCheckArgs:

    pattern = {'description': r'\b[A-Za-zÀ-ÖØ-öø-ÿ\s\d\-,.#]{1,500}\b'}
        
    
    def get_ticket_args(self, method=None) -> dict:
        parser = reqparse.RequestParser()
        if method == "put":
            parser.add_argument('status', type=int, required=True, help="Invalid or missing parameter 'status'.")
            parser.add_argument('admin_id', type=int, required=True, help="Invalid or missing parameter 'admin_id'.")
        else:
            parser.add_argument('subject', type=str, required=True, help="Invalid or missing parameter 'subject'.")
            parser.add_argument('description', type=inputs.regex(self.pattern['description']), required=True, help="Invalid or missing parameter 'description'.")
            parser.add_argument('type', type=int, required=True, help="Invalid or missing parameter 'type'.")
            parser.add_argument('author_id', type=int, required=True, help="Invalid or missing parameter 'author_id'.")
        args = parser.parse_args(strict=True)
        return args


class TicketController(Resource):

    def __init__(self) -> None:
        self.check_args = TicketCheckArgs()
        self.ticket_service = TicketService()

    @jwt_required()
    def get(self, ticket_id: int):
        try:
            ticket = self.ticket_service.select_one_by_id(ticket_id=ticket_id)
            return jsonify(ticket.json())
        except TicketIdNotFoundException as e:
            abort(http_status_code=404, message=str(e))
        except TicketAccessDbException as e:
            abort(http_status_code=500, message=str(e))
 
    @jwt_required()
    def put(self, ticket_id: int):
        try:
            args = self.check_args.get_ticket_args(method="put")
            self.ticket_service.update(ticket_id=ticket_id, args=args)
            return jsonify({'message': f"Ticket '{ticket_id}' successfully updated."})
        except TicketIdNotFoundException as e:
            abort(http_status_code=404, message=str(e))
        except UserIdNotFoundException as e:
            abort(http_status_code=404, message=str(e))
        except TicketAccessDbException as e:
            abort(http_status_code=500, message=str(e))        
   
    @jwt_required()
    def delete(self, ticket_id: int):
        try:
            self.ticket_service.delete(ticket_id=ticket_id)
            return jsonify({'message': f"Ticket '{ticket_id}' successfully deleted."})
        except TicketIdNotFoundException as e:
            abort(http_status_code=404, message=str(e))
        except TicketAccessDbException as e:
            abort(http_status_code=500, message=str(e)) 
            
   
    
class TicketListController(Resource):
    def __init__(self) -> None:
        self.check_args = TicketCheckArgs()
        self.ticket_service = TicketService()
    
    @jwt_required()
    def get(self):
        try:
            tickets = self.ticket_service.select_all()
            if tickets:
                return jsonify([ticket.json() for ticket in tickets])
            else:
                return jsonify({'message': "No tickets found."})
        except TicketAccessDbException as e:
            abort(http_status_code=500, message=str(e))
        
    @jwt_required()
    def post(self):
        try:
            args = self.check_args.get_ticket_args()
            self.ticket_service.insert(args=args)
            return jsonify({'message': f"Ticket '{args['subject']}' successfully created."})
        except TicketAccessDbException as e:
            abort(http_status_code=500, message=str(e))
        except UserIdNotFoundException as e:
            abort(http_status_code=404, message=str(e))


class TicketPageController(Resource):
    def __init__(self) -> None:
        self.ticket_service = TicketService()
    
    @jwt_required()
    def get(self, page: int):
        try:
            tickets = self.ticket_service.select_per_page(page=page)
            if tickets:
                return jsonify({'max_pages': tickets['max_pages'], 'tickets': [ticket.json() for ticket in tickets['tickets']]})
            else:
                return jsonify({'message': "No tickets found."})
        except TicketAccessDbException as e:
            abort(http_status_code=500, message=str(e))
        

class TicketSearchController(Resource):
    def __init__(self) -> None:
        self.ticket_service = TicketService()

    @jwt_required()
    def get(self, page: int, search: str):
        try:
            tickets = self.ticket_service.select_by_search(page=page, search=search)
            if tickets:
                return jsonify({'max_pages': tickets['max_pages'], 'tickets': [ticket.json() for ticket in tickets['tickets']]})
            else:
                return jsonify({'message': "No tickets found."})
        except TicketAccessDbException as e:
            abort(http_status_code=500, message=str(e))
      
        
class TicketUserController(Resource):
    def __init__(self) -> None:
        self.ticket_service = TicketService()

    @jwt_required()
    def get(self, user_id: int):
        try:
            tickets = self.ticket_service.select_all_by_user_id(user_id=user_id)
            if tickets:
                return jsonify({'tickets': [ticket.json() for ticket in tickets['tickets']]})
            else:
                return jsonify({'message': "No tickets found."})
        except TicketAccessDbException as e:
            abort(http_status_code=500, message=str(e))
        