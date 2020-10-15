python3 model_server.py -model_path ${SAVEDMODEL_LOCAL} $@
cd ${SAVEDMODEL_LOCAL} && /bin/bash ./docker_build.sh
