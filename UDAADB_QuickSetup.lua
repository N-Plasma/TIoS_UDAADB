path = '~/N_Plasma.DEV/UDAADB'
aggrees = {'Y','y','YES','Yes','yes'}

print('WARNING : FOLLOW MONGODB SETUP FOR YOUR DISTRO BEFORE RUNNING THIS')
print('QS installs files in ',path)
print()
print('Project UDAADB is developed by N_Plasma for use in TIoS and TIoSDT related servers, many features of this bot are connected to Whitelisted users')
print()
print('Confirm Application installation [Y/N]')
Conf = io.read()

if Conf == 'Y' or Conf == 'y' or Conf == 'YES' or Conf == 'Yes' or Conf == 'yes' then
    print('Installation Comfirmed, Attempting to Install')
    os.execute('mkdir ',path,' && echo > ',path)
    os.execute('wget -P ',path,' raw.githubusercontent.com/N-Plasma/TIoS_UDAADB/refs/heads/main/UDAADB_Core.py')
    os.execute('wget -P ',path,' raw.githubusercontent.com/N-Plasma/TIoS_UDAADB/refs/heads/main/UDAADB_Func.py')
    os.execute('wget -P ',path,' raw.githubusercontent.com/N-Plasma/TIoS_UDAADB/refs/heads/main/UDAADB_Ver.txt')
    os.execute('wget -P ',path,' raw.githubusercontent.com/N-Plasma/TIoS_UDAADB/refs/heads/main/UDAADB_Variables.env')
    os.execute('pip install dnspython')
    os.execute('python3 -m venv venv')
    os.execute('source venv/bin/activate')
    os.execute('python -m pip install "pymongo[srv]')
    os.execute('echo > ',path,'/logging.txt' )
    print('Installation Complete')
elseif Conf == 'x' or Conf == 'X' then
    print ('UDAADB Reinstallation confirmed, make sure to check changelogs if anything stops working')
    os.execute('rm ',path,'/UDAADB_Core.py')
    os.execute('rm ',path,'/UDAADB_Currency.py')
    os.execute('rm ',path,'/UDAADB_Func.py')
    os.execute('rm ',path,'/UDAADB_Ver.txt')
    os.execute('wget -P ',path,' raw.githubusercontent.com/N-Plasma/TIoS_UDAADB/refs/heads/main/UDAADB_Core.py')
    os.execute('wget -P ',path,' raw.githubusercontent.com/N-Plasma/TIoS_UDAADB/refs/heads/main/UDAADB_Func.py')
    os.execute('wget -P ',path,' raw.githubusercontent.com/N-Plasma/TIoS_UDAADB/refs/heads/main/UDAADB_Currency.py')
    os.execute('wget -P ',path,' raw.githubusercontent.com/N-Plasma/TIoS_UDAADB/refs/heads/main/UDAADB_Ver.txt')
else
    print('Installation Cancelled, Quiting QuickSetup')
end