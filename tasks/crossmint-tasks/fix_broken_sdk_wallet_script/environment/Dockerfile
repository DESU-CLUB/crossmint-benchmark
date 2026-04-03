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

# Install @crossmint/wallets-sdk
RUN cd /home/user && \
    npm init -y && \
    npm install @crossmint/wallets-sdk

# Pre-create the broken wallet script with 4 deliberate bugs
RUN cat >/home/user/broken_wallet.js <<'EOF'
const fs = require('fs');

// Bug 1: Wrong import - using .default instead of destructuring
const crossmintSdk = require('@crossmint/wallets-sdk').default;
const createCrossmint = crossmintSdk && crossmintSdk.createCrossmint;
const CrossmintWallets = crossmintSdk && crossmintSdk.CrossmintWallets;

async function main() {
    try {
        const crossmint = createCrossmint({ apiKey: process.env.CROSSMINT_API_KEY || 'sk_staging_placeholder' });
        const wallets = CrossmintWallets.from(crossmint);

        // Bug 2: Wrong chain name - underscore instead of hyphen
        // Bug 3: Wrong recovery type - email instead of server
        const wallet = wallets.createWallet({
            chain: 'base_sepolia',
            recovery: { type: 'email' }
        });

        // Bug 4: Missing await on createWallet call - wallet is a Promise not a result
        const address = wallet.address || 'mock-address';

        const result = {
            chain: 'base-sepolia',
            type: 'evm-smart-wallet',
            address: address
        };
        fs.writeFileSync('/home/user/wallet_debug_result.json', JSON.stringify(result, null, 2));
    } catch (err) {
        fs.writeFileSync('/home/user/wallet_debug_result.json', JSON.stringify({
            chain: 'base-sepolia',
            type: 'evm-smart-wallet',
            error: err.message
        }, null, 2));
    }
}

main();
EOF

LABEL Author="any-task-builder"
LABEL Description="Node.js environment with @crossmint/wallets-sdk and a broken wallet script with 4 bugs to debug."

# Container contents:
#   - Node.js 20.x with npm and @crossmint/wallets-sdk
#   - /home/user/broken_wallet.js — script with 4 deliberate SDK usage bugs
#   - Python venv at /opt/venv with pytest

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
