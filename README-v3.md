# BTC-Hack v3 - Enhanced Dashboard Edition 🚀

> **⚠️ IMPORTANT:** This tool is for educational and research purposes only. Always comply with applicable laws and regulations.

## 🎉 What's New in v3

### Enhanced Dashboard
- **Real-time Statistics**: Live monitoring of attempts, successes, and performance metrics
- **Session Analytics**: Track session duration, success rates, and API health
- **Performance Metrics**: Monitor search rate, estimated hourly attempts, and API status
- **Modern UI**: Clean, professional interface with dark theme support

### Upgraded Features
- **Dual Search Modes**: 
  - Private Key Generation (random 256-bit keys)
  - BIP39 Mnemonic Phrase Generation (12-24 word phrases)
- **Multi-API Support**: 
  - BlockCypher (default)
  - Blockchain.info (alternative)
- **Advanced Controls**:
  - Start/Stop/Pause functionality
  - Configurable API delays
  - Auto-save found wallets
  - Export statistics to JSON
- **Enhanced Logging**: 
  - Timestamped activity log
  - Color-coded status indicators
  - Detailed error reporting
- **Better Error Handling**: Graceful API error recovery and reporting

## 📋 Version Comparison

| Feature | v1 (CLI) | v2 (Basic GUI) | v2.1 (Mnemonic) | v3 (Dashboard) |
|---------|----------|----------------|-----------------|----------------|
| Private Key Search | ✅ | ✅ | ❌ | ✅ |
| Mnemonic Search | ❌ | ❌ | ✅ | ✅ |
| GUI Interface | ❌ | ✅ | ✅ | ✅ |
| Real-time Dashboard | ❌ | ❌ | ❌ | ✅ |
| Performance Metrics | ❌ | ❌ | ❌ | ✅ |
| API Health Monitor | ❌ | ❌ | ❌ | ✅ |
| Multi-API Support | ❌ | ❌ | ❌ | ✅ |
| Export Statistics | ❌ | ❌ | ❌ | ✅ |
| Pause/Resume | ❌ | ❌ | ❌ | ✅ |
| Configurable Settings | ❌ | ✅ | ✅ | ✅ |

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- Internet connection (for API calls)

### Installation

```bash
# Clone the repository
git clone https://github.com/DavidMGilbert/btc-hack.git
cd btc-hack

# Install dependencies
pip install -r requirements.txt
```

### Running v3 Dashboard

```bash
python3 btc-hack-v3-dashboard.py
```

### Running Other Versions

```bash
# CLI version (multiprocessing)
python3 btc-hack.py

# GUI v2 (private keys)
python3 btc-hack-v2.py

# GUI v2.1 (mnemonics)
python3 btc-hack-v2.1-mnemonic.py
```

## 📖 Usage Guide

### Dashboard Overview

The v3 dashboard is divided into three main sections:

#### 1. Statistics Panel (Left)
- **Session Information**: Start time and elapsed time
- **Progress Metrics**: Total attempts, wallets found, success rate
- **Performance Data**: Current rate, estimated hourly attempts
- **API Monitoring**: API calls, errors, and health status

#### 2. Control Panel (Right)
- **Search Mode Selection**: Choose between Private Key or Mnemonic mode
- **Mnemonic Options**: Configure word count (12-24) and passphrase file
- **Action Buttons**: Start/Stop search and Pause/Resume

#### 3. Activity Log (Bottom)
- Real-time log of all search activities
- Timestamped entries with status indicators
- Shows checked addresses and found wallets

### Search Modes

#### Private Key Mode
Generates random 256-bit private keys and checks corresponding Bitcoin addresses.

**Best for**: Fast, simple brute-force searches

#### Mnemonic Mode
Generates BIP39 mnemonic phrases (12-24 words) and derives Bitcoin addresses.

**Best for**: Testing mnemonic-based wallets

**Requirements**: 
- BIP0039.txt file must be present
- Optional: Passphrase dictionary file

### Settings

Access via **Menu → Settings**:

- **Theme**: Choose from 150+ PySimpleGUI themes
- **API Delay**: Adjust delay between API calls (0.1-1.0 seconds)
- **Auto Save**: Automatically save found wallets
- **API Provider**: Select between BlockCypher or Blockchain.info

### Menu Options

- **Export Stats**: Save current session statistics to JSON
- **Clear Stats**: Reset all counters and start fresh
- **About**: View application information
- **Documentation**: Quick help guide

## 🔍 How It Works

### Private Key Generation
1. Generate random 32-byte hexadecimal string using `os.urandom()`
2. Convert to public key using ECDSA SECP256k1 curve
3. Convert public key to Bitcoin address (P2PKH format)
4. Query blockchain API for address balance
5. Save if balance > 0

### Mnemonic Generation
1. Generate random BIP39 mnemonic phrase (12-24 words)
2. Optionally combine with passphrase
3. Convert to seed using SHA256
4. Derive private key from seed
5. Follow steps 2-5 from above

### API Integration
- **BlockCypher**: 200 requests/hour free tier, reliable
- **Blockchain.info**: Alternative with different rate limits
- Automatic error handling and retry logic
- Balance returned in BTC (converted from satoshis)

## 📊 Output Files

### found.txt
Contains all discovered wallets with positive balances:
```
============================================================
Found at: 2026-02-03 14:30:45
Mode: private_key
Address: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
Private key: 0000000000000000000000000000000000000000000000000000000000000001
WIF: 5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf
Public key: 0479BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798...
Balance: 0.001 BTC
============================================================
```

### btc_hack_stats_[timestamp].json
Exported statistics file:
```json
{
  "session_start": "2026-02-03T14:00:00",
  "session_end": "2026-02-03T15:30:00",
  "total_attempts": 18234,
  "total_successes": 0,
  "api_calls": 18234,
  "api_errors": 12,
  "mode": "private_key"
}
```

### settings_file.cfg
User preferences (auto-generated):
```json
{
  "theme": "DarkBlue3",
  "api_delay": 0.2,
  "auto_save": true,
  "api_provider": "blockcypher"
}
```

## 🎯 Expected Performance

Based on API rate limits:

| API Provider | Free Tier Limit | Addresses/Hour | Addresses/Day |
|-------------|----------------|----------------|---------------|
| BlockCypher | 200 req/hour | ~200 | ~4,800 |
| Blockchain.info | Variable | ~300 | ~7,200 |

**Note**: Actual performance depends on:
- Network latency
- API response time
- Configured delay settings
- System resources

## ⚙️ Advanced Configuration

### Custom API Delay
Adjust in settings or modify `DEFAULT_SETTINGS` in code:
```python
DEFAULT_SETTINGS = {
    'api_delay': 0.2,  # seconds between API calls
    ...
}
```

### Custom Passphrase Dictionary
Create a text file with one passphrase per line:
```
password123
mySecret2024
bitcoin2026
```

Use "Passphrase file" browse button to select it.

## 🛡️ Security & Privacy

- All processing is done locally on your machine
- No data is sent to third parties except blockchain API queries
- Found wallets are saved locally in `found.txt`
- API providers only see Bitcoin addresses (not private keys)

## ⚠️ Limitations & Disclaimers

### Technical Limitations
- **Search Space**: 2^160 possible Bitcoin addresses (practically infinite)
- **Success Probability**: Astronomically low (~1 in 10^48)
- **API Constraints**: Free tier limits apply
- **Speed**: Limited by API rate limits, not processing power

### Legal & Ethical
- **Educational Purpose**: This tool is for learning about Bitcoin cryptography
- **Not for Theft**: Accessing wallets you don't own is illegal
- **No Warranty**: Use at your own risk
- **Responsible Use**: Always comply with local laws and regulations

## 🔧 Troubleshooting

### Common Issues

**Problem**: "BIP0039.txt file not found"
- **Solution**: Ensure BIP0039.txt is in the same directory as the script

**Problem**: "API Error" messages
- **Solution**: 
  - Check internet connection
  - Increase API delay in settings
  - Switch to alternative API provider
  - Wait if rate limit exceeded

**Problem**: Slow performance
- **Solution**:
  - Reduce API delay (but watch for rate limits)
  - Use faster internet connection
  - Close other network-heavy applications

**Problem**: GUI doesn't appear
- **Solution**:
  - Ensure PySimpleGUI is installed: `pip install PySimpleGUI`
  - Try different theme in settings
  - Check Python version (3.6+ required)

## 📚 Dependencies

All dependencies with version requirements:

```
base58>=2.1.1       # Base58 encoding/decoding
ecdsa>=0.19.0       # Elliptic curve cryptography
requests>=2.31.0    # HTTP requests for API calls
PySimpleGUI>=5.0.0  # GUI framework
```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Additional API providers
- More cryptocurrency support (ETH, LTC, etc.)
- Database integration for tracking
- Machine learning optimizations
- Multi-threading improvements
- Custom address pattern matching

## 📜 License

This project is provided as-is for educational purposes. See the LICENSE file for details.

## 🙏 Credits

- **Original Author**: David Gilbert
- **v3 Enhancements**: Modern dashboard, multi-API support, enhanced features
- **Libraries**: Python community for excellent crypto libraries

## 🔗 Links

- **GitHub**: https://github.com/DavidMGilbert/btc-hack
- **Website**: https://www.davidmgilbert.com
- **Offline Version**: https://github.com/DavidMGilbert/btc-hack-offline

## 💰 Support

If you find this project useful, consider supporting:

**Bitcoin**: `1LKKJE62ygo2c9K2Xc8GxuGwpVDnvyRFRD`

---

**Remember**: This is a proof-of-concept for educational purposes. The probability of finding a wallet with balance is astronomically low. The real value is in learning about Bitcoin cryptography, key generation, and blockchain technology.

Happy learning! 🎓
