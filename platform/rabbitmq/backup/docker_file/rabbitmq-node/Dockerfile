# Author: YanHua <it-yanh@all-reach.com>

FROM index.boxlinker.com/boxlinker/centos-rabbitmq-base:1.0.1

RUN echo 'rabbitmq-server -detached' >> /run.sh
RUN echo 'sleep 1s' >> /run.sh
RUN echo 'rabbitmqctl stop_app' >> /run.sh
RUN echo 'sleep 1s' >> /run.sh
RUN echo 'rabbitmqctl reset' >> /run.sh
RUN echo 'sleep 1s' >> /run.sh
RUN echo 'rabbitmqctl join_cluster --ram rabbit@rabbitmq01' >> /run.sh
RUN echo 'sleep 1s' >> /run.sh
RUN echo 'rabbitmqctl start_app' >> /run.sh
RUN echo 'sleep 1s' >> /run.sh
RUN echo 'rabbitmqctl set_policy ha-all "^" '{"ha-mode":"all"}'' >> /run.sh

RUN echo 'while true' >> /run.sh
RUN echo 'do' >> /run.sh
RUN echo '    sleep 1h' >> /run.sh
RUN echo 'done' >> /run.sh
RUN chmod +x /run.sh

CMD /run.sh
