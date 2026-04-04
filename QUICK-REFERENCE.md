# BTC-Hack Quick Reference Card

## Installation
```bash
git clone https://github.com/DavidMGilbert/btc-hack.git
cd btc-hack
pip install -r requirements.txt
```

## Launch Commands

| Version | Command | Best For |
|---------|---------|----------|
| **v3 Dashboard** ⭐ | `python3 btc-hack-v3-dashboard.py` | Everyone - Full featured |
| v2.1 Mnemonic | `python3 btc-hack-v2.1-mnemonic.py` | Mnemonic testing |
| v2 Basic GUI | `python3 btc-hack-v2.py` | Simple GUI |
| v1 CLI | `python3 btc-hack.py` | Command line |

## v3 Dashboard Quick Start

### 1. Launch
```bash
python3 btc-hack-v3-dashboard.py
```

### 2. Choose Mode
- **Private Key**: Random key generation (faster)
- **Mnemonic**: BIP39 phrase generation (matches real wallets)

### 3. Control
- **Start**: Begin searching (green button)
- **Stop**: End search (turns red)
- **Pause**: Temporarily pause (preserves stats)

### 4. Monitor
- **Dashboard**: Real-time statistics
- **Activity Log**: See all attempts
- **API Health**: Monitor API status

### 5. Settings (Optional)
- Menu → Settings
- Choose theme, API delay, provider
- Click Save

## Dashboard Overview

```
┌─────────────────────────────────────────────────────────┐
│                    STATISTICS                           │
├─────────────────────────────────────────────────────────┤
│ Session Started:    2026-02-03 14:00:00                │
│ Elapsed Time:       01:23:45                            │
│ Total Attempts:     12,543                              │
│ Wallets Found:      0                                   │
│ Success Rate:       0.00000000%                         │
├─────────────────────────────────────────────────────────┤
│               PERFORMANCE METRICS                       │
├─────────────────────────────────────────────────────────┤
│ Current Rate:       2.85/sec                            │
│ Est. Hourly:        10,260                              │
│ API Calls:          12,543                              │
│ API Errors:         12                                  │
│ API Health:         Healthy                             │
└─────────────────────────────────────────────────────────┘
```

## Menu Options

| Option | Function |
|--------|----------|
| Settings | Configure theme, API, delays |
| Export Stats | Save session data to JSON |
| Clear Stats | Reset all counters |
| About | App information |
| Documentation | Quick help |

## File Outputs

| File | Contains |
|------|----------|
| `found.txt` | Wallets with positive balance |
| `btc_hack_stats_*.json` | Exported statistics |
| `settings_file.cfg` | User preferences |

## Search Modes

### Private Key Mode
- Generates random 256-bit keys
- Faster processing
- Standard BTC addresses

**Setup**: Select "Private Key Generation" → Start

### Mnemonic Mode
- BIP39 phrase generation
- 12-24 word phrases
- Optional passphrase support

**Setup**: 
1. Select "Mnemonic Phrase"
2. Choose word count (12, 15, 18, 21, 24)
3. Browse to passphrase file (optional)
4. Start

## API Providers

### BlockCypher (Default)
- Free tier: 200 req/hour
- Reliable and fast
- No registration needed

### Blockchain.info (Alternative)
- Variable rate limits
- Good backup option
- Switch in Settings

## Performance Tips

1. **Start Simple**: Use Private Key mode first
2. **Monitor Health**: Watch API health indicator
3. **Adjust Delay**: Increase if seeing errors
4. **Export Regularly**: Save stats periodically
5. **Stable Network**: Use wired connection

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Start/Stop | Click button |
| Pause | Click pause button |
| Settings | Menu → Settings |
| Exit | Menu → Exit |

## Status Indicators

| Color | Meaning |
|-------|---------|
| 🟢 Green | Running, wallet found |
| 🟡 Yellow | Ready, searching |
| 🔴 Red | Stopped, error |
| 🟠 Orange | Paused |

## Activity Log Symbols

| Symbol | Meaning |
|--------|---------|
| 🔍 | Checking address |
| 💰 | Wallet found! |
| ⚠️ | Warning/Error |
| ⏹️ | Stopped |
| ⏸️ | Paused |
| ▶️ | Started/Resumed |
| 📊 | Stats cleared |

## Common Commands

### Check Installation
```bash
python3 -c "import base58, ecdsa, requests, PySimpleGUI; print('✓ Ready')"
```

### View Found Wallets
```bash
cat found.txt
```

### Background Run (CLI v1 only)
```bash
nohup python3 btc-hack.py > output.log 2>&1 &
```

### Check Logs
```bash
tail -f output.log
```

## Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Module not found | `pip install -r requirements.txt` |
| BIP0039.txt missing | Check file in same directory |
| API errors | Increase delay in Settings |
| Slow performance | Close other apps, check network |
| GUI won't start | Try CLI version or reinstall PySimpleGUI |

## Expected Results

- **Empty wallets**: Normal (most addresses are empty)
- **Success rate**: ~0% is expected
- **API errors**: Occasional OK, frequent = increase delay
- **Rate**: 2-5 per second typical with API limits

## Important Notes

⚠️ **Educational Purpose Only**
- Success probability is astronomically low (~10^-48)
- Most addresses will be empty
- Learning tool for cryptography

⚠️ **Legal**
- Don't access wallets you don't own
- Comply with local laws
- Use responsibly

⚠️ **API Limits**
- Respect free tier limits
- Don't spam requests
- Switch providers if needed

## Support

- **Documentation**: README-v3.md, USAGE-GUIDE.md
- **Issues**: GitHub repository
- **Updates**: Check CHANGELOG.md

## Quick Stats Interpretation

```
Total Attempts: 10,000
├─ This is good (you're searching)
Wallets Found: 0
├─ This is normal (expected)
Success Rate: 0.00%
├─ This is expected (realistic)
Current Rate: 3.2/sec
├─ This is typical (API limited)
API Health: Healthy
└─ This is good (keep going)
```

## One-Line Install & Run
```bash
git clone https://github.com/DavidMGilbert/btc-hack.git && cd btc-hack && pip install -r requirements.txt && python3 btc-hack-v3-dashboard.py
```

---

**TIP**: Bookmark this file for quick reference during searches!

**Remember**: The journey is the reward. Learn about Bitcoin cryptography! 🎓
