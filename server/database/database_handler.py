#!/usr/bin/env python

################################################################################
# file      database_handler.py
#           This script provides the helper functions to update mysql database
#
# author    Glide Technology Pvt. Ltd. <www.glidemtech.com>
# version   1.0
# date      29, Jul, 2017
################################################################################

################################################################################
# dependencies
################################################################################

import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'server'))
from time import gmtime, strftime
import MySQLdb
import traceback
import database_schema

################################################################################
# constants
################################################################################

DB_NAME = 'owb_server_database'
DB_GATEWAY_TABLE="owb_gateway_table"
DB_PDM_TABLE="owb_pdm_table"
DB_USER_TABLE="owb_user_table"
TABLE_SCHEMA_GATEWAY='(filename varchar(25), \
major_version varchar(5), \
minor_version varchar(5), \
modified_date datetime, \
commit_number varchar(25), \
commit_date datetime, \
remarks varchar(50), \
latest varchar(5), \
UNIQUE (filename) \
)'

TABLE_SCHEMA_PDM='(filename varchar(25), \
major_version varchar(5), \
minor_version varchar(5), \
modified_date datetime, \
commit_number varchar(25), \
commit_date datetime, \
remarks varchar(50), \
latest varchar(5), \
UNIQUE (filename) \
)'

TABLE_SCHEMA_USER='(username varchar (25), \
password varchar (25), \
firstname varchar(25), \
lastname varchar(25), \
emailid varchar (25), \
UNIQUE (username)  \
)'

GATEWAY_TABLE_FIELDS='(filename,major_version,minor_version,modified_date,commit_number,commit_date,remarks,latest)'
PDM_TABLE_FIELDS='(filename,major_version,minor_version,modified_date,commit_number,commit_date,remarks,latest)'
USER_TABLE_FIELDS='(username,password,firstname,lastname,emailid)'

################################################################################
# private variables
################################################################################

# none

################################################################################
# public variables
################################################################################

#none

################################################################################
# private classes
################################################################################

# none

################################################################################
# public classes
################################################################################

class DatabaseHandler():
    def __init__(self):
        self._db = self._db_connect()
        self._db_create()
        self._db_table_create(DB_GATEWAY_TABLE, TABLE_SCHEMA_GATEWAY)
        self._db_table_create(DB_PDM_TABLE, TABLE_SCHEMA_PDM)
        self._db_table_create(DB_USER_TABLE, TABLE_SCHEMA_USER)
        self.db_add_default_user()


    def _db_execute_command(self, command):
        cursor = self._db.cursor()
        cursor.execute(command)
        data=cursor.fetchall()
        self._db.commit()
        return data


    def _db_connect(self):
        db = MySQLdb.connect(host="localhost",user="root",passwd="root")
        return db

    def _db_disconnect():
        self._db.close()

    def _db_create(self):
        cmd = 'CREATE DATABASE IF NOT EXISTS ' + DB_NAME
        self._db_execute_command(cmd)

    def _db_table_create(self, table_name, schema):
        try:
            cmd = 'USE ' + DB_NAME
            self._db_execute_command(cmd)
            cmd = 'CREATE TABLE  IF NOT EXISTS '+  table_name+schema
            self._db_execute_command(cmd)
        except:
            return False
        return True

    def _db_add(self, table_name, fields, values):
        try:
            cmd = 'show tables like "'+table_name+'"'
            data = self._db_execute_command(cmd)
            if data:
                cmd = 'REPLACE INTO '+table_name+' '+fields+'  VALUES'+values
                self._db_execute_command(cmd)
                return True
            else:
                print "Table doesn't exist!"
                return False
        except:
            print str(traceback.format_exc())
            return False

    def _db_delete(self, table_name, field, value):
        try:
            cmd = 'show tables like "'+table_name+'"'
            data = self._db_execute_command(cmd)
            if data:
                cmd = 'DELETE from '+table_name+' where '+field+'="'+value+'"'
                self._db_execute_command(cmd)
                return True
            else:
                print "Table doesn't exist!"
                return False
        except:
            print str(traceback.format_exc())
            return False

    def _db_deleteall(self, table_name):
        try:
            cmd = 'show tables like "'+table_name+'"'
            data = self._db_execute_command(cmd)
            if data:
                cmd = 'DELETE from '+table_name
                self._db_execute_command(cmd)
                return True
            else:
                print "Table doesn't exist!"
                return False
        except:
            print str(traceback.format_exc())
            return False

    def _db_update(self, table_name, search_field, search_value, field, value):
        try:
            cmd = 'show tables like "'+table_name+'"'
            data = self._db_execute_command(cmd)
            if data:
                cmd = 'UPDATE '+table_name+' SET '+field+'="'+value+'" where '+search_field+'="'+search_value+'"'
                self._db_execute_command(cmd)
                return True
            else:
                print "Table doesn't exist!"
                return False
        except:
            print str(traceback.format_exc())
            return False

    def _db_get(self, table_name, field, value):
        try:
            cmd = 'show tables like "'+table_name+'"'
            data = self._db_execute_command(cmd)
            if data:
                cmd = sql='select * from '+table_name+' where '+field+'="'+value+'"'
                data = self._db_execute_command(cmd)
                return data
            else:
                print "Table doesn't exist!"
                return None
        except:
            print str(traceback.format_exc())
            return None

    def _db_getall(self, table_name):
        try:
            cmd = 'show tables like "'+table_name+'"'
            data = self._db_execute_command(cmd)
            if data:
                cmd = sql='select * from '+table_name
                data = self._db_execute_command(cmd)
                return data
            else:
                print "Table doesn't exist!"
                return None
        except:
            print str(traceback.format_exc())
            return None


####################### Gateway table helper functions ############################

    def db_gateway_schema(self):
        return database_schema.DB_SCHEMA_GATEWAY.copy()

    def db_add_gateway_file(self, gateway_schema):
        try:
            gateway_values='('+'"'+gateway_schema['filename']+'"'+',' \
            +gateway_schema['major_version']+','+gateway_schema['minor_version'] \
            +',"'+str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))+'",'+gateway_schema['commit_number'] \
            +',"'+gateway_schema['commit_date']+'","-",false )'
        except:
            print str(traceback.format_exc())
        return self._db_add(DB_GATEWAY_TABLE, GATEWAY_TABLE_FIELDS, gateway_values)

    def db_delete_gateway_file(self, filename):
        return self._db_delete(DB_GATEWAY_TABLE, 'filename', filename)

    def db_delete_all_gateway_files(self):
        return self._db_deleteall(DB_GATEWAY_TABLE)

    def db_update_gateway_file(self, filename, field, value):
        return self._db_update(DB_GATEWAY_TABLE, 'filename', filename, field, value)


    def db_get_gateway_file(self, filename):
        return self._db_get(DB_GATEWAY_TABLE, 'filename', filename)

    def db_get_all_gateway_files(self):
        return self._db_getall(DB_GATEWAY_TABLE)

    def db_get_latest_gateway_file(self):
        try:
            filename=None
            data = self._db_getall(DB_GATEWAY_TABLE)
            for row in data:
                if row[7] == '1':
                    filename = row[0]
                    break
        except:
            print str(traceback.format_exc())
        return filename

####################### PDM table helper functions ############################

    def db_pdm_schema(self):
        return database_schema.DB_SCHEMA_PDM.copy()

    def db_add_pdm_file(self, pdm_schema):
        try:
            pdm_values='('+'"'+pdm_schema['filename']+'"'+',' \
            +pdm_schema['major_version']+','+pdm_schema['minor_version'] \
            +',"'+str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))+'",'+pdm_schema['commit_number'] \
            +',"'+pdm_schema['commit_date']+'","-",false )'
        except:
            print str(traceback.format_exc())
        return self._db_add(DB_PDM_TABLE, PDM_TABLE_FIELDS, pdm_values)

    def db_delete_pdm_file(self, filename):
        return self._db_delete(DB_PDM_TABLE, 'filename', filename)

    def db_delete_all_pdm_files(self):
        return self._db_deleteall(DB_PDM_TABLE)

    def db_update_pdm_file(self, filename, field, value):
        return self._db_update(DB_PDM_TABLE, 'filename', filename, field, value)

    def db_get_pdm_file(self, filename):
        return self._db_get(DB_PDM_TABLE, 'filename', filename)

    def db_get_all_pdm_files(self):
        return self._db_getall(DB_PDM_TABLE)

    def db_get_latest_pdm_file(self):
        try:
            filename=None
            data = self._db_getall(DB_PDM_TABLE)
            for row in data:
                if row[7] == '1':
                    filename = row[0]
                    break
        except:
            print str(traceback.format_exc())
        return filename


########################## USER table helper functions ##########################

    def db_user_schema(self):
        return database_schema.DB_SCHEMA_USER.copy()

    def db_add_default_user(self):
        try:
            data = self._db_getall(DB_USER_TABLE)
            for row in data:
                if len(row) == 0:
                    user_values='("admin","admin","test","test","test@gmail.com")'
                    self._db_add(DB_USER_TABLE, USER_TABLE_FIELDS, user_values)
                    break
        except:
            print str(traceback.format_exc())

    def db_add_user(self, user_schema):
        try:
            user_values='(admin, \
            admin,'+'"'+user_schema['first_name']+'"'+', \
            '+'"'+user_schema['last_name']+'"'+','+'"'+user_schema['email_id']+'"'+',)'
        except:
            print str(traceback.format_exc())
        return self._db_add(DB_USER_TABLE, USER_TABLE_FIELDS, user_values)

    def db_delete_user(self, user_name):
        return self._db_delete(DB_USER_TABLE, 'user_name', user_name)

    def db_delete_all_users(self):
        return self._db_deleteall(DB_USER_TABLE)

    def db_update_user(self, user_name, field, value):
        return self._db_update(DB_USER_TABLE, 'user_name', user_name, field, value)

    def db_get_user(self, user_name):
        return self._db_get(DB_USER_TABLE, 'user_name', user_name)

    def db_get_all_users(self):
        return self._db_getall(DB_USER_TABLE)

    def db_get_latest_user(self):
        try:
            user_name=None
            data = self._db_getall(DB_USER_TABLE)
            for row in data:
                if row[7] == '1':
                    user_name = row[0]
                    break
        except:
            print str(traceback.format_exc())
        return user_name

################################################################################
# private methods
################################################################################

#none

################################################################################
# public methods
################################################################################

#none

################################################################################
# script
################################################################################

# none

################################################################################
# end of file
################################################################################
