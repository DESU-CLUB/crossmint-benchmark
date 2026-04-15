You are working in an environment with Node.js and `node-fetch` installed.

A common challenge with Crossmint is that NFT minting is asynchronous. When you POST to the minting API, you get back an `actionId` immediately, but the actual mint may take seconds to complete. Developers who fail to poll for the final status leave their UIs hanging.

Write a Node.js script at `/home/user/mint_and_poll.js` that:
1. Initiates an NFT mint to `email:demo@example.com:polygon-amoy` via `POST https://staging.crossmint.com/api/2022-06-09/collections/default/nfts` with metadata `name: "Poll Test NFT"`, `description: "Testing async polling"`, `image: "https://example.com/poll.png"`, using `CROSSMINT_API_KEY` for auth
2. Extracts the `actionId` from the mint response
3. Polls `GET https://staging.crossmint.com/api/2022-06-09/actions/<actionId>` every 2 seconds, up to a maximum of 5 attempts, until the action status is not `"pending"`
4. Writes the final result to `/home/user/poll_result.json` with these fields:
   - `actionId`: the ID string (or `"mock-action-id"` if credentials are absent)
   - `final_status`: the last observed status string (or `"unknown"` if not retrieved)
   - `poll_attempts`: number of polling attempts made (integer)
   - `mint_chain`: `"polygon-amoy"`

Handle errors gracefully — if any API call fails, write the log with whatever fields are available plus an `error` field.