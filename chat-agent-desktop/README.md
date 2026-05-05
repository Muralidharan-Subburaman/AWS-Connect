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
Customer initiates chat (StartChatContact API) →
Connect routes via contact flow →
Contact attributes set (CustomerName, AccountNumber, Tier, ContractID) →
Transfer to Queue →
Streams API fires onIncoming → profile panel populated →
Agent accepts → onConnected fires →
ChatJS getMediaController() → WebSocket established →
onMessage subscribed → real time messages render →
Typing events handled → typing indicator shown →
Customer disconnects → onParticipantDisconnected fires →
Contact ends → onEnded fires → desktop resets

## Key Technical Decisions

**Why ChatJS loads after Streams:** ChatJS depends on the AWS SDK bundled by Streams. Loading order prevents SDK conflicts.

**Why CCP container is hidden not deleted:** The CCP iframe maintains the WebSocket connection and audio handling in background. Removing it kills all contact events.

**Why region is mandatory:** Chat uses Connect Participant Service regional endpoints. Wrong region causes silent chat failure.

**Why textContent not innerHTML:** Prevents XSS attacks. Customer input is never interpreted as HTML.

**Why chatController is global:** sendMessage() lives outside onContact scope. Global state allows access across function boundaries.

## Production Patterns Demonstrated

- Fail safe routing — DefaultQueue fallback on any error
- Persistent chat — full transcript loaded on customer reconnect  
- Screen pop — customer profile loaded on onIncoming before agent accepts
- AHT tracking — timer starts on connect, stops on ACW
- Defensive coding — optional chaining prevents null reference crashes