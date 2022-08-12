FROM exploreasl/xasl:1.9.0

ENTRYPOINT ["/bin/bash"]

RUN apt-get update
RUN apt-get install -y python3.10

WORKDIR /opt/

COPY xasl_wrapper.py xasl_wrapper.py
