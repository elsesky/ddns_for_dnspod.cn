REM 停守护进程
@sc delete _dnspod_ddns_service_d 
@taskkill /im pypod_service_d.exe -f
REM 停服务
@sc delete _dnspod_ddns_service 
@taskkill /im pypod_service.exe -f
REM 删计划任务
@SCHTASKS /Delete /TN "sc_Ddnspod_service_d" /F
@SCHTASKS /Delete /TN "sc_Ddnspod_service" /F