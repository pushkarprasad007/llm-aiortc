## Description
This sample repo serves as a PoC for conversational AI apps using python on the server side. It is built on giant shoulders of aiortc 🙏. 

The user speaks something in the browser after connection is there which gets recorded on the backend. In response, I've simply queued 3 audios, which play back to back as a response. This is close to how conversational apps in real life using LLM would be, since LLM respond with result token by token, so its possible to send partial response as soon it hits a punctuation mark or so. 

- Example
    - Oh, I understand! I think its best that you talk to my manager, who would have better knowhow of this.
    - In the ☝️ AI response, there would be three parts
        - Oh, I understand!
        - I think its best that you talk to my manager
        - who would have better knowhow of this.



## Installation
To install, use the following steps (tested on macOS)

1. python3.12 -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. python server_<aiohttp|fastapi>.py

On a web-browser: 

1. Go to localhost:8080
2. Click on green power button
3. After some time Webrtc status shows 'connected'
4. Click on audio button and speak, and then click on stop.
