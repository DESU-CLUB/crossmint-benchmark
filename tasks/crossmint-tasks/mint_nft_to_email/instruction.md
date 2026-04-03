You are working in an environment with Node.js and the `node-fetch` library installed.

Using the Crossmint Minting REST API, write a Node.js script at `/home/user/mint_nft.js` that mints a single NFT and delivers it to an email address.

The script must:
1. Use the Crossmint Minting API endpoint: `https://staging.crossmint.com/api/2022-06-09/collections/default/nfts`
2. Send a `POST` request with the API key from the environment variable `CROSSMINT_API_KEY` in the `x-api-key` header
3. Set the recipient to `email:test@example.com:polygon-amoy`
4. Include NFT metadata: `name` set to `"Welcome NFT"`, `description` set to `"A welcome gift"`, and `image` set to `"https://example.com/nft.png"`
5. Write the full API response (as JSON) to `/home/user/mint_response.json`
6. Handle errors gracefully — if the API call fails (network error or HTTP error), write a JSON object with an `error` field to `/home/user/mint_response.json` instead of throwing

Run the script with `node /home/user/mint_nft.js` to produce the output file.