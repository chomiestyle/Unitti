from Robot.Emails.Database.Manage_database import *


path_demo = '/Robot/Emails/stocktwits'

# ##Asi creo la base de datos inicial
new_database=Manage_Database()
new_database.emails_from_directory(path_directory=path_demo)
new_database.close_session()
