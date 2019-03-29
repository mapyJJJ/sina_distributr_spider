while true;
do
        server_main=`ps -aux|grep Master_spider.py|grep -v grep`
        server_restart=`ps -aux|grep broken_start.py|grep -v grep`
        echo "main:","$server_main"
        echo "restart","$server_restart"
        if [ "$server_main" = "" -a "$server_restart" = "" ]
        then
            echo "检测到脚本未运行"
            nohup python3 broken_start.py &
        else
            echo "pass"
        fi
        sleep 60 
done
