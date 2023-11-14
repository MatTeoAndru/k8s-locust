#!/bin/bash
set -e

locustMode=${locustMode:-standalone}
locustMasterBindPort=${locustMasterBindPort:-5557}
locustFile=${locustFile:-basic.py}
LOCUST_LOCUSTFILE_PATH=${LOCUST_LOCUSTFILE_PATH:="/locust-tasks/basic.py"}
targetHost=${targetHost:-"https://servizipasshub.passstage.cloud"}


#[ -z ${targetHost+x} ] && (echo 'variable targetHost not set' ; exit 1)
[ $(echo ${locustMode} | tr 'a-z' 'A-Z') == "WORKER" ] && [ -z ${locustMaster+x} ] && \
    (echo 'variable locustMaster must be set if locustMode=="WORKER"'; exit 1)

locustOptions="-f ${locustFile} --host=${targetHost} $locustOptions --class-picker --modern-ui"


[ $(echo ${locustMode} | tr 'a-z' 'A-Z') == "MASTER" ] && locustOptions="--master --master-bind-port=${locustMasterBindPort} $locustOptions"

[ $(echo ${locustMode} | tr 'a-z' 'A-Z') == "WORKER" ] && locustOptions="--worker --master-host=${locustMaster} --master-port=${locustMasterBindPort} $locustOptions"

cd /locust-tasks
locust ${locustOptions}


