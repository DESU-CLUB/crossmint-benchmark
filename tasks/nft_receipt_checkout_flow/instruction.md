You are building a backend service that automatically mints an NFT receipt when a user completes a purchase. Your environment has Node.js installed with `express` and `node-fetch`.

Create a complete Express.js webhook handler at `/home/user/webhook_server.js` that:
1. Listens on port `3000`
2. Exposes a `POST /webhook/purchase` endpoint that accepts a JSON body with `{ purchaseId, customerEmail, productName, amount }`
3. On receiving a valid purchase event:
   a. Mints an NFT receipt via `POST https://staging.crossmint.com/api/2022-06-09/collections/default/nfts` to `email:<customerEmail>:polygon-amoy`
   b. NFT metadata: `name` = `"Receipt: <productName>"`, `description` = `"Proof of purchase for order <purchaseId>"`, `image` = `"https://example.com/receipt.png"`
   c. Responds with `{ status: "receipt_minted", purchaseId, actionId }` (use the `id` field from the Crossmint API response as `actionId`, or `"mock-action"` if unavailable)
4. Exposes a `GET /health` endpoint returning `{ status: "ok" }`
5. On missing required fields, returns HTTP 400 with `{ error: "Missing required fields", required: ["purchaseId", "customerEmail", "productName", "amount"] }`

Also write a test script at `/home/user/test_webhook.js` that:
- Starts the server as a child process
- Sends a test POST request to `http://localhost:3000/webhook/purchase` with a sample purchase payload
- Sends a GET request to `http://localhost:3000/health`
- Saves a report to `/home/user/webhook_test_report.json` with `health_check` (boolean) and `webhook_response` (the response body) fields
- Exits 0 regardless of API call outcomes

Use `CROSSMINT_API_KEY` from the environment for the API key.