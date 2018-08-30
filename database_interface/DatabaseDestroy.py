#!/usr/bin/python

import MySQLdb

# open database connection
db = MySQLdb.connect( "localhost", "root", "lwgmysql" )

c = db.cursor( )
c.execute( """DROP DATABASE IF EXISTS elo""" )
