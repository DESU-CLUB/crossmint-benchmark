You are building infrastructure for an AI agent that can autonomously manage funds. Your environment has Node.js and the `@crossmint/wallets-sdk` installed.

Create a complete treasury orchestration module at `/home/user/treasury.js` that an AI agent could use as a tool. The module must export (using CommonJS `module.exports`) a single async function `executeTreasuryAction(action)` where `action` is an object with a `type` field.

The module must handle these action types:
- `{ type: 'create_wallet', userId: string, chain: string }` — creates a Crossmint EVM smart wallet for the given userId on the specified chain; returns `{ success: true, address, chain, userId }`
- `{ type: 'check_balance', walletAddress: string, chain: string }` — queries the Crossmint API for the wallet balance; returns `{ success: true, walletAddress, chain, balance: string }`  
- `{ type: 'mint_receipt', email: string, purchaseId: string }` — mints a "Purchase Receipt" NFT to the given email on `polygon-amoy` via the Crossmint minting API; returns `{ success: true, email, purchaseId, actionId: string }`

For any action type not in the above list, return `{ success: false, error: 'Unknown action type' }`.

Also write a test harness at `/home/user/run_treasury_tests.js` that:
1. Imports `executeTreasuryAction` from `./treasury.js`
2. Runs all three action types with mock inputs
3. Writes results to `/home/user/treasury_test_results.json` as an array of result objects, each with `action_type` and `result` fields
4. Exits 0 regardless of whether API calls succeed (graceful error handling required)

All API credentials should be read from environment variables (`CROSSMINT_API_KEY`, `SIGNER_SECRET`).