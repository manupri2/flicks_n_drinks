import sqlalchemy

eng = sqlalchemy.create_engine('mysql://cs411ccsquad_admin:password;uiuc@localhost/cs411ccsquad_FlicksNDrinks')

def get_roles():
   with eng.connect() as con:
       cur = con.execute('SELECT * FROM Role')
       roles = []
       for elem in cur:
           roles.append(elem)
       return roles
   return None

print(get_roles())
	
