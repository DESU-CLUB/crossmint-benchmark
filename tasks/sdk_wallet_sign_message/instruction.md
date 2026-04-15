You are working in an environment with the Crossmint Wallets Node.js SDK installed.

Using the `@crossmint/wallets-sdk`, write a Node.js script at `/home/user/sign_message.js` that:
1. Initializes the Crossmint client using the `createCrossmint` function with the server API key from the `CROSSMINT_API_KEY` environment variable
2. Creates a `CrossmintWallets` instance
3. Attempts to get or create an EVM smart wallet on `base-sepolia` — use wallet locator `userId:demo-user-001` and server-side recovery
4. Signs the message `"Hello from Crossmint"` using the wallet's signing capabilities
5. Writes a JSON log to `/home/user/sign_result.json` with these fields:
   - `chain`: `"base-sepolia"`
   - `message`: `"Hello from Crossmint"`
   - `signature`: the hex signature string returned by the SDK (or `"mock-signature"` if credentials are unavailable)
   - `wallet_type`: `"evm-smart-wallet"`

Handle errors gracefully — if signing fails due to missing credentials, write the log with the above fields plus an `error` field describing the failure.

Run with `node /home/user/sign_message.js` to produce the output.