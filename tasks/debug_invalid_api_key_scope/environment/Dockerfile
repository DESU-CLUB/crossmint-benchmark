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

# Set up npm project with node-fetch
RUN cd /home/user && \
    npm init -y && \
    npm install node-fetch@2

# Pre-create the broken script with all 4 bugs
RUN cat >/home/user/broken_mint.js <<'EOF'
const fetch = require('node-fetch');
const fs = require('fs');

// Bug 1: Wrong API key type (client key ck_ instead of server key sk_)
const apiKey = process.env.CROSSMINT_API_KEY || 'ck_staging_placeholder';

// Bug 2: Wrong recipient format (pipe separators instead of colons)
const recipient = 'email|test@example.com|polygon-amoy';

// Bug 3: Missing image in metadata
const metadata = {
    name: 'Debug NFT',
    description: 'A test NFT for debugging'
};

// Bug 4: Wrong URL (missing staging subdomain)
const url = 'https://crossmint.com/api/2022-06-09/collections/default/nfts';

async function main() {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'x-api-key': apiKey,
                'content-type': 'application/json'
            },
            body: JSON.stringify({ recipient, metadata })
        });
        const data = await response.json().catch(() => ({ error: 'Non-JSON response', status: response.status }));
        fs.writeFileSync('/home/user/fixed_mint_response.json', JSON.stringify(data, null, 2));
    } catch (err) {
        fs.writeFileSync('/home/user/fixed_mint_response.json', JSON.stringify({ error: err.message }));
    }
}

main();
EOF

LABEL Author="any-task-builder"
LABEL Description="Node.js environment with a broken Crossmint minting script containing 4 deliberate bugs."

# Container contents:
#   - Node.js 20.x with npm and node-fetch v2
#   - /home/user/broken_mint.js — script with 4 deliberate Crossmint API bugs
#   - Python venv at /opt/venv with pytest

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
