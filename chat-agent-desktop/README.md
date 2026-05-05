# Amazon Connect — Chat Agent Desktop

A production-ready chat agent desktop built on Amazon Connect Streams API.
Demonstrates real-world chat handling patterns used in financial services contact centers.

## What This Shows

- CCP initialisation with chat configuration
- Chat contact event handling — incoming, connected, ACW, ended, missed
- Real time message rendering — customer, agent, system messages
- Typing indicator
- Persistent chat — transcript loaded on reconnect
- Customer profile populated from contact flow attributes
- AHT timer
- Enter key to send message

## Contact Attributes Expected From Connect Flow

Set these in your contact flow before transferring to queue:

| Attribute      | Example Value     |
|---------------|-------------------|
| CustomerName  | John Smith        |
| AccountNumber | ACC-001234        |
| Tier          | Premium           |
| Intent        | CheckBalance      |
| ContractID    | C042              |
| Verified      | true              |

## Setup

1. Download Streams: https://github.com/amazon-connect/amazon-connect-streams
2. Build: `npm run release` → copy `connect-streams-min.js` here
3. Download ChatJS: https://github.com/amazon-connect/amazon-connect-chatjs
4. Copy `amazon-connect-chat.js` here
5. Update `CONFIG.instanceUrl` and `CONFIG.region` in the HTML file
6. Allowlist your domain in Connect console → Approved Origins
7. Open in browser — login popup appears — agent desktop loads

## Architecture