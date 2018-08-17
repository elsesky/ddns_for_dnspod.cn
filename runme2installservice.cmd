@ECHO OFF
@sc create _dnspod_ddns_service start= delayed-auto binPath= %cd%\pypod_service.exe
@net start _dnspod_ddns_service