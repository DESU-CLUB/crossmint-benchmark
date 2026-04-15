FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-venv bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Node.js 20.x
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install pytest

RUN mkdir -p /home/user && chmod 0755 /home/user

# Install node-fetch in /home/user npm project
RUN cd /home/user && \
    npm init -y && \
    npm install node-fetch@2

LABEL Author="any-task-builder"
LABEL Description="Node.js environment with node-fetch installed for Crossmint NFT minting API task."

# Container contents:
#   - Node.js 20.x with npm
#   - /home/user — npm project with node-fetch v2 installed
#   - Python venv at /opt/venv with pytest

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
