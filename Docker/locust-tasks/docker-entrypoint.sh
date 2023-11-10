#!/bin/bash

# LOCUST_MODE=${LOCUST_MODE:="standalone"}
# LOCUST_MASTER=${LOCUST_MASTER:=""}
# LOCUST_LOCUSTFILE_PATH=${LOCUST_LOCUSTFILE_PATH:="/locust-tasks/basic.py"}
# LOCUST_LOCUSTFILE_URL=${LOCUST_LOCUSTFILE_URL:=""}
# LOCUST_TARGET_HOST=${LOCUST_TARGET_HOST:="https://servizipasshub.passstage.cloud"}

# if [ ! -z "$LOCUST_LOCUSTFILE_URL" ]; then
#     LOCUST_LOCUSTFILE_PATH="/locust-tasks/locustfile.py"
#     curl $LOCUST_LOCUSTFILE_URL -o $LOCUST_LOCUSTFILE_PATH
# fi

# LOCUST_PATH="/usr/local/bin/locust"
# LOCUST_FLAGS="-f $LOCUST_LOCUSTFILE_PATH --host=$LOCUST_TARGET_HOST"

# if [[ "$LOCUST_MODE" = "master" ]]; then
#     LOCUST_FLAGS="$LOCUST_FLAGS --master"
# elif [[ "$LOCUST_MODE" = "slave" ]]; then
#     LOCUST_FLAGS="$LOCUST_FLAGS --slave --master-host=$LOCUST_MASTER"
# fi

# exec $LOCUST_PATH $LOCUST_FLAGS


set -e

locustMode=${locustMode:-standalone}
locustMasterBindPort=${locustMasterBindPort:-5557}
locustFile=${locustFile:-basic.py}
LOCUST_TARGET_HOST=${LOCUST_TARGET_HOST:="https://servizipasshub.passstage.cloud"}
LOCUST_LOCUSTFILE_PATH=${LOCUST_LOCUSTFILE_PATH:="/locust-tasks/basic.py"}
targetHost=${targetHost:-"https://servizipasshub.passstage.cloud"}


#[ -z ${targetHost+x} ] && (echo 'variable targetHost not set' ; exit 1)
[ $(echo ${locustMode} | tr 'a-z' 'A-Z') == "WORKER" ] && [ -z ${locustMaster+x} ] && \
    (echo 'variable locustMaster must be set if locustMode=="WORKER"'; exit 1)

locustOptions="-f ${locustFile} --host=${targetHost} $locustOptions"

[ $(echo ${locustMode} | tr 'a-z' 'A-Z') == "MASTER" ] && locustOptions="--master --master-bind-port=${locustMasterBindPort} $locustOptions"

[ $(echo ${locustMode} | tr 'a-z' 'A-Z') == "WORKER" ] && locustOptions="--worker --master-host=${locustMaster} --master-port=${locustMasterBindPort} $locustOptions"

cd /locust-tasks
locust ${locustOptions}


