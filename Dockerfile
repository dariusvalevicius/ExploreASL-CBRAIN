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
COPY run_xasl.py /opt/xasl_cbrain/run_xasl.py
COPY parse_arguments.py /opt/xasl_cbrain/parse_arguments.py
COPY to_json.py /opt/xasl_cbrain/to_json.py

# Ensure execute permissions
RUN chmod 755 /opt/xasl_cbrain/run_xasl.py

# Add wrapper to path
ENV PATH="${PATH}:/opt/xasl_cbrain"

# Run as non-root user
RUN useradd cbrain_user
USER cbrain_user
