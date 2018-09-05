@ECHO OFF
REM DDNS服务
@sc create _dnspod_ddns_service start= delayed-auto binPath= %cd%\pypod_service.exe
@net start _dnspod_ddns_service
REM DDNS服务的守护进程
@sc create _dnspod_ddns_service_d start= delayed-auto binPath= %cd%\pypod_service_d.exe
@net start _dnspod_ddns_service_d
REM 加计划任务
@schtasks /create /sc minute /mo 5 /tn "sc_Ddnspod_service" /ru system /tr "net start _dnspod_ddns_service" /f 
@schtasks /create /sc minute /mo 5 /tn "sc_Ddnspod_service_d" /ru system /tr "net start _dnspod_ddns_service_d"  /f 
