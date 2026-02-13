#Setup
import time
import fs
import logging
import subprocess
from pymongo.mongo_client import MongoClient
import os
from os import load_dotenv
load_dotenv()

client = MongoClient('localhost', 27017)
db = client.UDAADB
users = db.users
incidentreports = db.incidents
currency = db.currency
ranks = {'L1','L2','L3','L4','Clearance Delta','Bot Creator'}

#Base Functions
def dbping():
    pingres = client.admin.command("ping")
    if pingres.get('ok') == 1.0:
        print('Ping Success')
        logging.INFO('Ping Success')
        return('Ping Responded')
    else:
        print('!! Ping Failure')
        logging.WARN('Ping Failure')
        return('Ping Failed')

def UpdateCheck():
    subprocess.call('wget -P ~/N_Plasa.DEV/UDAADB -O GitVer.txt raw.githubusercontent.com/N-Plasma/TIoS_UDAADB/refs/heads/main/UDAADB_Ver.txt')
    
    with open('GitVer.txt', 'r') as file:
        GitVer = file.read().rstrip()
    
    with open('UDAADB_Ver.txt', 'r') as file:
        LocalVer = file.read().rstrip()

    if LocalVer != GitVer:
        print('UDAADB Version Outdated, run Quick Setup and confirm with "x" to reinstall')
    subprocess.call('rm ~/N_Plasma.DEV/UDAADB/GitVer.txt')

def RankCalc(ownrank,comparedrank):
    if ownrank == ranks[1]: ownrank = 1
    if ownrank == ranks[2]: ownrank = 2
    if ownrank == ranks[3]: ownrank = 3
    if ownrank == ranks[4]: ownrank = 4
    if ownrank == ranks[5]: ownrank = 5
    if ownrank == ranks[6]: ownrank = 99

    if comparedrank == ranks[1]: comparedrank = 1
    if comparedrank == ranks[2]: comparedrank = 2
    if comparedrank == ranks[3]: comparedrank = 3
    if comparedrank == ranks[4]: comparedrank = 4
    if comparedrank == ranks[5]: comparedrank = 5
    if comparedrank == ranks[6]: comparedrank = 99

    if ownrank<comparedrank:
        return(False)
    elif ownrank>comparedrank:
        return(True)
    
def makeusr(id,user,display,role,rank,own_id):
    users.insert_one({'user':user,'name':display,'id':id,'role':role,'rank':rank,'note':'no note'})
    currency.insert_one({'id':id,'xp':0,'money':0})
    print(own_id,' created user entry. ID : ',id,' Username : ',user,' Display Name : ',display,' Role : ',role,' Rank : ',rank)
    logging.INFO(own_id,' created user entry. ID : ',id,' Username : ',user,' Display Name : ',display,' Role : ',role,' Rank : ',rank)

#Basic Functions
def OnJoin(id,user,display):
    logging.INFO('User Joined, id : ',id,' Username : ',user,' Displayname : ',display)
    print('User Joined, id : ',id,' Username : ',user,' Displayname : ',display)
    if users.find_one({"id":id}) == True:
        print('User is already in Database')
        logging.INFO('User is already in Database')
    else:
        print('User not in Database, Creating entries')
        logging.INFO('User not in Database, Creating entries')
        makeusr(id,user,display)

def OnLeave(id,user,display):
    logging.INFO('User left, id : ',id,' Username : ',user,' Displayname : ',display)
    print('User left, id : ',id,' Username : ',user,' Displayname : ',display)

def ManipulateUserEntry(own_id,own_rank,source_id,source_rank,user_to,display_to,role_to,rank_to,note_to):
    logging.INFO('User Entry Manipulation Started by ',own_id,' Fetching manipulated Data...')
    print('User Entry Manipulation Started by ',own_id,' Fetching manipulated Data...')

    if source_id == None or own_id == None or source_rank == None or own_rank == None or users.find_one({"id":source_id}) == False:
        print('User Entry Manipulation Canceled - Incomplete Command')
        logging.INFO('User Entry Manipulation Canceled - Incomplete Command')
        Response = ('User Entry Manipulation Canceled - Incomplete Command')
    
    elif RankCalc(own_rank,source_rank) == False or RankCalc(own_rank, rank_to) == False:
        print('User Entry Manipulation Canceled - User who ran command has too low of a role, user is ',own_id,' ',own_rank,' source is ',source_id,source_rank)
        logging.INFO('User Entry Manipulation Canceled - User who ran command has too low of a role, user is ',own_id,' ',own_rank,' source is ',source_id,' ',source_rank)
        Response = ('You are too low ranked to perform this action.')
    else:
        print('Checks passed, Changing the following for ',source_id)
        logging.INFO('Checks passed, Changing the following for ',source_id)
        if user_to != None:
            print('User To : ',user_to)
            logging.INFO('User To : ',user_to)
            users.update_one({'id':source_id},{})
        if display_to != None:
            print('Display To : ',display_to)
            logging.INFO('Display To : ',display_to)
            users.update_one({'id':source_id},{})
        if role_to != None:
            print('Role To : ',role_to)
            logging.INFO('Role To : ',role_to)
            users.update_one({'id':source_id},{})
        if rank_to != None:
            print('Rank To : ',rank_to)
            logging.INFO('Rank To : ',rank_to)
            users.update_one({'id':source_id},{})
        if note_to != None:
            print('Note To : ',note_to)
            logging.INFO('Note To : ',note_to)
            users.update_one({'id':source_id},{})
            Response = 'Entry Updated'
    return(Response)

def xpauto(event,id,own_id):
    axpget = currency.find_one({"id":id})
    xp = axpget[2]

    if axpget != None and event != None and id != None and own_id != None:
        if event == 'Training': event_conv = 15
        elif event == 'Soc_Event': event_conv = 12
        elif event == 'React_Check': event_conv = 10
        xp_out = xp + event_conv
        currency.update_one({'id':id},{'xp':xp_out})
        print(own_id,' set ',id,'s XP to ',xp_out)
        logging.INFO(own_id,' set ',id,'s XP to ',xp_out)

def curedit(id,own_id,cur,select,amount):
    ceget = currency.find_one({"id":id})

    if ceget != None and own_id != None and cur != None and select != None and amount != None:
        
        if cur == 'xp':
            amounto = ceget[2]
        elif cur == 'money':
            amounto = ceget[3]
        
        if select == 'a':
            amount_cur = amount + amounto
        elif select == 'm':
            amount_cur = amount - amounto
        elif select == 'w':
            amount_cur = 0
        elif select == 's':
            amount_cur = amount
            currency.update_one({'id':id}, {cur:amount_cur})
            print(own_id,'Changed ',id,'s ',cur,' to ',amount_cur)
            logging.INFO(own_id,' Changed ',id,'s ',cur,' to ',amount_cur)

def inciedit(name,name_to,public_to,involved_to,body_to,own_id):
    inciget = incidentreports.find_one({'name':name})
    if inciget != None and own_id != None:
        if name_to != None or public_to != None or involved_to != None or body_to != None:
            print(own_id,' edited entry ',name,' with the following')
            logging.INFO(own_id,' edited entry ',name,' with the following')
            if name_to != None:
                print('Name To : ',name_to)
                logging.INFO('Name To : ',name_to)
                incidentreports.update_one({'name':name},{'name':name_to})
            if public_to != None:
                print('Public To : ',public_to)
                logging.INFO('Public To : ',public_to)
                incidentreports.update_one({'name':name},{'public':public_to})
            if involved_to != None:
                print('Involved To : ',involved_to)
                logging.INFO('Involved To : ',involved_to)
                incidentreports.update_one({'name':name},{'involved':involved_to})
            if body_to != None:
                print('Body To : ',body_to)
                logging.INFO('Body To : ',body_to)
                incidentreports.update_one({'name':name},{'body':body_to})

def xpview(id, own_id):
    xpget = currency.find_one({"id":id})
    if xpget != None and own_id != None:
        xp = xpget[2]
        print(own_id,' read XP of ',id)
        logging.INFO(own_id,' read XP of ',id)
        return(xp)
    else: return('Entry Not Found')

def incimake(name,public,involved,body,own_id):
    if name != None and public != None and involved != None and body != None and own_id != None:
        print('Incident report created with the following information, Name : ',name,' Is Public? : ',public,' Involved : ',involved,' Body : ',body)
        logging.INFO('Incident report created by ',own_id,' with the following information, Name : ',name,' Is Public? : ',public,' Involved : ',involved,' Body : ',body)
        incidentreports.insert_one({'name':name,'public':public,'involved':involved,'body':body})

def inciread(repname,own_id):
    inci = incidentreports.find_one({'name':repname})
    if inci != None and own_id != None:
        print(own_id,' read incident log ',repname)
        logging.INFO(own_id,' read incident log ',repname)
        return(inci)
    else: return('Entry Not Found')

def userread(id,own_id):
    usr = users.find_one({'id':id})
    if usr != None and own_id != None:
        print(own_id,' read user entry of ',id)
        logging.INFO(own_id,' read user entry of ',id)
        return(usr)
    else: return('Entry Not Found')

def curread(id,own_id):
    cur = currency.find_one({'id':id})
    if cur != None and own_id != None:
        print(own_id,' read currency entry of ',id)
        logging.INFO(own_id,' read currency entry of ',id)
        return(cur)
    else: return('Entry Not Found')

def updateroles(id,role):
    upgget = users.find_one({'id':id})
    if upgget != None and role != None:
        if role == 'drone': None
        elif role == 'commander' and upgget[4] != 'commander': users.update_one({'id':id},{'role':'commander'})

        elif role == 'science' and upgget[4] != 'science': users.update_one({'id':id},{'role':'science'})
        elif role == 'gaurd' and upgget[4] != 'gaurd': users.update_one({'id':id},{'role':'gaurd'})

        elif role == 'gaurdlead' and upgget[4] != 'gaurdlead': users.update_one({'id':id},{'role':'gaurdlead'})
        elif role == 'sciencelead' and upgget[4] != 'sciencelead': users.update_one({'id':id},{'role':'sciencelead'})