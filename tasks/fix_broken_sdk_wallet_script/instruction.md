You are working in an environment with the Crossmint Wallets Node.js SDK installed. A broken script exists at `/home/user/broken_wallet.js` that attempts to create an EVM wallet using the SDK, but it has bugs that prevent it from running correctly.

Run the script to observe its errors:
```
node /home/user/broken_wallet.js
```

Diagnose and fix ALL bugs in `/home/user/broken_wallet.js`. The correct behavior is:
- Import `createCrossmint` and `CrossmintWallets` from `@crossmint/wallets-sdk`
- Create a wallet on `base-sepolia` with server-side recovery
- Write a JSON result to `/home/user/wallet_debug_result.json` with `chain`, `type`, and either `address` or `error` fields

After fixing the bugs, the script must run with `node /home/user/broken_wallet.js`, exit 0, and produce `/home/user/wallet_debug_result.json`.

Write a brief diagnosis to `/home/user/debug_notes.txt` listing each bug you found and how you fixed it (one line per bug, format: `BUG: <description> | FIX: <what you changed>`).