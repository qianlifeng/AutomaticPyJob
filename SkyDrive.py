#coding=gbk

from __future__ import unicode_literals

from skydrive import api_v5 as api


auth = api.SkyDriveAuth(client_id='00000000480D1D0D',client_secret='5QFkuwb3Pfp4y-ZdrW52j0kPJMvDSnaB')
auth.auth_refresh_token = 'abed2ff6-8212-8904-b669-b5e510affdcf'
print auth.auth_get_token()
#print api.SkyDriveAPI(auth).listdir()
#print api.SkyDriveAPI().auth_user_get_url()

