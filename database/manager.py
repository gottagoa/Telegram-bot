from sqlalchemy import select, update

from database.models import User, UserOrder, CafeOrder, StatusChoices
from db import async_session



class UserManager():

    def __init__(self):
        self.model = User
        

    async def register_user(self, data):
        async with async_session() as session:
            user = await session.execute(select(self.model).filter_by(tg_id=data["tg_id"]))
            user = user.scalars().first()
            if user:
                return user
            else: 
                user = self.model(
                        tg_id=data["tg_id"],
                        username=data["username"],
                        name=data["first_name"],
                    )
                session.add(user)
                await session.commit()
                return user

user_manager = UserManager()



class CafeOrderManager():

    def __init__(self):
        self.model = CafeOrder

    async def create_new_order(self,data):
        async with async_session() as session:

            order = self.model(
                cafe_url = data["url"],
                notice = data["notice"]
            )
            session.add(order)
            await session.commit()
            await session.refresh(order)
            return order
    
    async def check_order(self):
        query = select(self.model).filter_by(status=StatusChoices.active)
        async with async_session() as session:
            result = await session.execute(query)
            order = result.scalars().first()
            print(order)
            if order:
                return True
            else:
                return False

    async def get_orders(self):
        query = select(self.model).filter(self.model.status.in_(
            [StatusChoices.active, StatusChoices.ordering]
            ))
        async with async_session() as session:
            result = await session.execute(query)
            orders = result.scalars()
            return orders
        
    async def change_order_status(self,event,order_id):
        query = update(self.model).where(self.model.id==int(order_id))
        if event == "reject":
            query = query.values({self.model.status:StatusChoices.rejected})
        elif event == "close":
            query = query.values({self.model.status:StatusChoices.ordering})
        elif event == "complete":
            query = query.values({self.model.status:StatusChoices.completed})
        
        async with async_session() as session:
            await session.execute(query)
            await session.commit()


        
            

order_manager = CafeOrderManager()