FROM dvalev/xasl_base_image:latest

ENTRYPOINT ["/bin/bash"]

RUN apt-get update
RUN apt-get install -y python3.10

COPY xasl_wrapper.py /opt/xasl_wrapper.py
RUN chmod a+x /opt/xasl_wrapper.py
