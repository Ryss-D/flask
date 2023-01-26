"""
bloclist.py

This file jsut contains the blocklist of the JWT tokens.
 It will be imported by app and the logout resource so that tokens 
 canbe added to the bloslist when the users logs out.

"""

##this can be improved with a more eficcient stragevgi
##to persist data other tan a set, ieg a DB
BLOCKLIST = set()