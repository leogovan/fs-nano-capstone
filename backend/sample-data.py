from os import abort
from sqlalchemy import insert, create_engine
from models import db, RoleType

#----------------------------------------------------------------------------#
# Setup
#----------------------------------------------------------------------------#


# role_types_value_list = [
#     {'role_type':'star'},
#     {'role_type':'co-star'}
#     ]


 
data = insert(RoleType.__table__).values(role_type='star')
print(data)
db.session.add(data)
db.session.commit