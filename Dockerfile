FROM dvalev/xasl_base_image:latest

ENTRYPOINT ["/bin/bash"]

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt install -y python3.10
    
    
COPY xasl_wrapper.py /opt/xasl_wrapper.py
COPY parse_arguments.py /opt/parse_arguments.py
COPY to_json.py /opt/to_json.py

#RUN chmod a+x /opt/xasl_wrapper.py
