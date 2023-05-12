# AI Battler
## Installation
1. Generate Mastodon push notification key
```bash
python scripts/generate_key.py
```

2. Deploy
```bash
sls deploy
```

3. Register Endpoint
```bash
python scripts/subscribe.py <AWS Lambda endpoint>
```