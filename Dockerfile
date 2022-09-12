FROM dvalev/xasl_base_image:latest

# Override entrypoint
ENTRYPOINT ["/bin/bash"]

# Install python
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt install -y python3.10
    
# Copy wrapper scripts
COPY xasl_wrapper.py /opt/xasl_cbrain/xasl_wrapper.py
COPY parse_arguments.py /opt/xasl_cbrain/parse_arguments.py
COPY to_json.py /opt/xasl_cbrain/to_json.py

# Ensure execute permissions
RUN chmod 755 /opt/xasl_cbrain/xasl_wrapper.py

# Add wrapper to path
ENV PATH="${PATH}:/opt/xasl_cbrain"
