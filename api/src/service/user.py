from model.user import User
from repository.user import UserRepo
from exception.user import *
from exception.event import EventIdNotFoundException
from exception.role import RoleIdNotFoundException
from exception.delivery import DeliveryIdNotFoundException
from exception.collect import CollectIdNotFoundException
from service.role import RoleService
from service.event import EventService
from service.delivery import DeliveryService
from service.collect import CollectService
from service.shop import ShopService
from repository.ticket import TicketRepo


class UserService:

    def __init__(self) -> None:
        self.user_repo = UserRepo()
        self.role_service = RoleService()
        self.event_service = EventService()
        self.delivery_service = DeliveryService()
        self.collect_service = CollectService()
        self.shop_service = ShopService()
        self.ticket_repo = TicketRepo()

    def select_one_by_id(self, user_id: int) -> User:
        user = self.user_repo.select_one_by_id(user_id=user_id)
        if user:
            return user
        else:
            raise UserIdNotFoundException(user_id=user_id)

    def select_one_by_email(self, email: str) -> User:
        user = self.user_repo.select_one_by_email(email=email.lower())
        if user:
            return user
        else:
            raise UserEmailNotFoundException(email=email.lower())

    def select_per_page(self, page: int) -> list[User]:
        users = self.user_repo.select_per_page(page=page)
        return users

    def select_by_search(self, page: int, search: str) -> list[User]:
        users = self.user_repo.select_by_search(page=page, search=search)
        return users

    def select_all(self) -> list[User]:
        users = self.user_repo.select_all()
        return users

    def insert(self, args: dict, method: str) -> None:
        if method == "register" and args["role_id"] == 1:
            raise UserRoleInvalidException(role_id=args["role_id"])

        new_user = User(
            first_name=args["first_name"],
            last_name=args["last_name"],
            email=args["email"].lower(),
            phone=args["phone"],
            password=args["password"],
            status=0 if method == "register" else args["status"],
            shop_id=None,
        )
        if self.user_repo.select_one_by_email(email=new_user.email.lower()):
            raise UserAlreadyExistsException(new_user.email.lower())
        if not self.role_service.select_one_by_id(args["role_id"]):
            raise RoleIdNotFoundException(args["role_id"])
        new_user_id = self.user_repo.insert(new_user=new_user, role_id=args["role_id"])
        return new_user_id

    def insert_event(self, user_id: int, event_id: int) -> None:
        user = self.select_one_by_id(user_id=user_id)
        if not user:
            raise UserIdNotFoundException(user_id=user_id)
        if user.events:
            for event in user.events:
                if event.id == event_id:
                    raise UserParticipatesEventAlreadyExistsException(
                        user_id=user_id, event_id=event_id
                    )
        if not self.event_service.select_one_by_id(event_id=event_id):
            raise EventIdNotFoundException
        self.user_repo.insert_event(user_id=user_id, event_id=event_id)

    def insert_role(self, user_id: int, role_id: int) -> None:
        user = self.select_one_by_id(user_id=user_id)
        if not user:
            raise UserIdNotFoundException(user_id=user_id)
        if user.roles:
            for role in user.roles:
                if role.id == role_id:
                    raise UserIsRoleAlreadyExistsException(
                        user_id=user_id, role_id=role_id
                    )
        if not self.role_service.select_one_by_id(role_id=role_id):
            raise RoleIdNotFoundException
        self.user_repo.insert_role(user_id=user_id, role_id=role_id)

    def insert_delivery(self, user_id: int, delivery_id: int) -> None:
        user = self.select_one_by_id(user_id=user_id)
        if not user:
            raise UserIdNotFoundException(user_id=user_id)
        if user.deliveries:
            for delivery in user.deliveries:
                if delivery.id == delivery_id:
                    raise UserDeliversAlreadyExistsException(
                        user_id=user_id, delivery_id=delivery_id
                    )
        if not self.delivery_service.select_one_by_id(delivery_id=delivery_id):
            raise DeliveryIdNotFoundException
        self.user_repo.insert_delivery(user_id=user_id, delivery_id=delivery_id)

    def insert_collect(self, user_id: int, collect_id: int) -> None:
        user = self.select_one_by_id(user_id=user_id)
        if not user:
            raise UserIdNotFoundException(user_id=user_id)
        if user.collects:
            for collect in user.collects:
                if collect.id == collect_id:
                    raise UserCollectsAlreadyExistsException(
                        user_id=user_id, collect_id=collect_id
                    )
        if not self.collect_service.select_one_by_id(collect_id=collect_id):
            raise CollectIdNotFoundException
        self.user_repo.insert_collect(user_id=user_id, collect_id=collect_id)

    def insert_shop(self, user_id: int, shop_id: int) -> None:
        user = self.select_one_by_id(user_id=user_id)
        if user.shop_id:
            raise UserShopAlreadyExistsException(user_id=user_id)

        self.shop_service.select_one_by_id(shop_id=shop_id)
        self.user_repo.insert_shop(user_id=user_id, shop_id=shop_id)

    def update(self, user_id: int, args: dict) -> None:
        update_user = User(
            first_name=args["first_name"],
            last_name=args["last_name"],
            email=args["email"].lower(),
            phone=args["phone"],
            password=args["password"] if args["password"] else None,
            status=args["status"],
        )
        user = self.user_repo.select_one_by_id(user_id=user_id)
        if not user:
            raise UserIdNotFoundException(user_id=user_id)

        users_with_email = self.user_repo.select_by_email(email=update_user.email.lower())

        if len(users_with_email) == 2 or users_with_email[0].id != user_id:
            raise UserAlreadyExistsException(email=update_user.email.lower())

        self.user_repo.update(user_id=user_id, update_user=update_user)

    def delete(self, user_id: int) -> None:
        self.select_one_by_id(user_id=user_id)
        tickets = self.ticket_repo.select_all_by_user_id(user_id=user_id)
        if tickets:
            for ticket in tickets['tickets']:
                if ticket.author_id == user_id:
                    self.ticket_repo.delete(ticket_id=ticket.id)
        self.user_repo.delete(user_id=user_id)

    def delete_event(self, user_id: int, event_id: int) -> None:
        user = self.select_one_by_id(user_id=user_id)
        if not user:
            raise UserIdNotFoundException(user_id=user_id)
        event_exist = False
        if user.events:
            for event in user.events:
                if event.id == event_id:
                    event_exist = True
        if not event_exist:
            raise UserParticipatesEventNotFoundException(
                user_id=user_id, event_id=event_id
            )
        self.user_repo.delete_event(user_id=user_id, event_id=event_id)

    def delete_role(self, user_id: int, role_id: int) -> None:
        user = self.select_one_by_id(user_id=user_id)
        if not user:
            raise UserIdNotFoundException(user_id=user_id)
        role_exist = False
        if user.roles:
            for role in user.roles:
                if role.id == role_id:
                    role_exist = True
        if len(user.roles) == 1:
            raise UserRoleNotEmptyException(user_id=user_id)
        if not role_exist:
            raise UserIsRoleNotFoundException(user_id=user_id, role_id=role_id)
        self.user_repo.delete_role(user_id=user_id, role_id=role_id)

    def delete_delivery(self, user_id: int, delivery_id: int) -> None:
        user = self.select_one_by_id(user_id=user_id)
        if not user:
            raise UserIdNotFoundException(user_id=user_id)
        delivery_exist = False
        if user.deliveries:
            for delivery in user.deliveries:
                if delivery.id == delivery_id:
                    delivery_exist = True
        if not delivery_exist:
            raise UserDeliversNotFoundException(
                user_id=user_id, delivery_id=delivery_id
            )
        self.user_repo.delete_delivery(user_id=user_id, delivery_id=delivery_id)

    def delete_collect(self, user_id: int, collect_id: int) -> None:
        user = self.select_one_by_id(user_id=user_id)
        if not user:
            raise UserIdNotFoundException(user_id=user_id)
        collect_exist = False
        if user.collects:
            for collect in user.collects:
                if collect.id == collect_id:
                    collect_exist = True
        if not collect_exist:
            raise UserCollectsNotFoundException(user_id=user_id, collect_id=collect_id)
        self.user_repo.delete_collect(user_id=user_id, collect_id=collect_id)

    def delete_shop(self, user_id: int, shop_id: int) -> None:
        user = self.select_one_by_id(user_id=user_id)
        if not user.shop_id or user.shop_id != shop_id:
            raise UserShopsNotFoundException(user_id=user_id, shop_id=shop_id)

        self.user_repo.delete_shop(user_id=user_id)
