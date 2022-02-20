from sqlalchemy import insert, create_engine
from models import db, RoleType

#----------------------------------------------------------------------------#
# Setup
#----------------------------------------------------------------------------#


# role_types_value_list = [
#     {'role_type':'star'},
#     {'role_type':'co-star'}
#     ]

# def insert_role_types():
#     insert_data = insert(RoleType.__table__).values(role_type='star')
#     return insert_data
    
# insert(RoleType.__table__).values(role_type='star')
    

# insert_role_types()