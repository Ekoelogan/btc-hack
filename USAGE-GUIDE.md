# BTC-Hack Usage Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Version Comparison](#version-comparison)
3. [Step-by-Step Tutorials](#step-by-step-tutorials)
4. [Best Practices](#best-practices)
5. [Troubleshooting](#troubleshooting)
6. [FAQ](#faq)

## Getting Started

### System Requirements
- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.6 or higher
- **RAM**: Minimum 512MB
- **Internet**: Active connection for API calls
- **Disk Space**: 100MB free space

### Installation Steps

1. **Install Python**
   ```bash
   # Check if Python is installed
   python3 --version
   
   # If not installed, download from https://www.python.org/downloads/
   ```

2. **Clone Repository**
   ```bash
   git clone https://github.com/DavidMGilbert/btc-hack.git
   cd btc-hack
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   # or
   pip3 install base58 ecdsa requests PySimpleGUI
   ```

4. **Verify Installation**
   ```bash
   python3 -c "import base58, ecdsa, requests, PySimpleGUI; print('✓ All dependencies installed')"
   ```

## Version Comparison

### BTC-Hack v1 (CLI)
**Best for**: Command-line users, automation, server environments

**Features**:
- ✅ Multi-threaded processing
- ✅ Minimal resource usage
- ✅ Easy to automate
- ❌ No GUI
- ❌ Basic output

**Run**: `python3 btc-hack.py`

### BTC-Hack v2 (Basic GUI)
**Best for**: Desktop users wanting simple interface

**Features**:
- ✅ Graphical interface
- ✅ Real-time counter
- ✅ Theme selection
- ✅ Private key generation
- ❌ No mnemonic support
- ❌ Limited statistics

**Run**: `python3 btc-hack-v2.py`

### BTC-Hack v2.1 (Mnemonic)
**Best for**: Users testing BIP39 mnemonic phrases

**Features**:
- ✅ All v2 features
- ✅ BIP39 mnemonic generation
- ✅ Custom passphrase support
- ✅ Configurable word count
- ❌ Limited dashboard

**Run**: `python3 btc-hack-v2.1-mnemonic.py`

### BTC-Hack v3 (Dashboard) ⭐ RECOMMENDED
**Best for**: Everyone - most feature-rich version

**Features**:
- ✅ Comprehensive dashboard
- ✅ Both private key AND mnemonic modes
- ✅ Real-time statistics
- ✅ Performance metrics
- ✅ API health monitoring
- ✅ Multiple API providers
- ✅ Export/Import data
- ✅ Pause/Resume functionality
- ✅ Professional UI

**Run**: `python3 btc-hack-v3-dashboard.py`

## Step-by-Step Tutorials

### Tutorial 1: Basic Search with v3

1. **Launch the Application**
   ```bash
   python3 btc-hack-v3-dashboard.py
   ```

2. **Configure Settings (Optional)**
   - Click **Menu → Settings**
   - Choose your preferred theme
   - Adjust API delay (0.2s recommended)
   - Select API provider
   - Click **Save**

3. **Select Search Mode**
   - Choose **Private Key Generation** (default)
   - This will generate random 256-bit keys

4. **Start Searching**
   - Click the green **Start** button
   - Watch the dashboard update in real-time
   - Monitor: attempts, rate, API health

5. **Monitor Progress**
   - **Total Attempts**: Number of addresses checked
   - **Current Rate**: Addresses per second
   - **API Health**: Status of blockchain API
   - **Activity Log**: Real-time search results

6. **Stop When Done**
   - Click **Stop** button (turns red)
   - Your session stats are preserved
   - Export stats if needed

### Tutorial 2: Mnemonic Search with v3

1. **Ensure BIP0039.txt Exists**
   ```bash
   ls BIP0039.txt  # Should be in same directory
   ```

2. **Launch Application**
   ```bash
   python3 btc-hack-v3-dashboard.py
   ```

3. **Select Mnemonic Mode**
   - Click **Mnemonic Phrase** radio button
   - Options become enabled

4. **Configure Mnemonic Settings**
   - **Number of words**: Select 12, 15, 18, 21, or 24
     - 12 words: Standard, faster
     - 24 words: More secure, slower
   - **Passphrase file**: Optional, click Browse if you have one

5. **Create Passphrase File (Optional)**
   ```bash
   # Create a file with passphrases, one per line
   echo "password123" > passphrases.txt
   echo "mysecret2024" >> passphrases.txt
   echo "bitcoin" >> passphrases.txt
   ```
   - Browse and select this file

6. **Start Search**
   - Click **Start**
   - Monitor mnemonic phrases being tested
   - Check activity log for details

### Tutorial 3: Using v2.1 for Mnemonic

1. **Launch v2.1**
   ```bash
   python3 btc-hack-v2.1-mnemonic.py
   ```

2. **Configure**
   - **Number of mnemonic words**: Select from dropdown
   - **Mnemonic dictionary file**: Browse to passphrase file (optional)

3. **Start/Stop**
   - Click **Start/Stop** button to toggle
   - Watch counters update

4. **View Results**
   - Check output window for tested addresses
   - Found wallets saved to `found.txt`

### Tutorial 4: CLI Version for Automation

1. **Basic Usage**
   ```bash
   python3 btc-hack.py
   ```

2. **Run in Background**
   ```bash
   nohup python3 btc-hack.py > output.log 2>&1 &
   ```

3. **Check Progress**
   ```bash
   tail -f output.log
   ```

4. **Stop**
   ```bash
   pkill -f btc-hack.py
   ```

## Best Practices

### API Usage
1. **Respect Rate Limits**
   - BlockCypher: 200 requests/hour free
   - Use 0.2s delay minimum
   - Switch APIs if rate limited

2. **Handle Errors Gracefully**
   - Monitor API Health in dashboard
   - Increase delay if errors occur
   - Switch provider if persistent issues

3. **Optimize Performance**
   - Use v3 for best monitoring
   - Close unnecessary applications
   - Stable internet connection

### Search Strategy
1. **Start with Private Keys**
   - Faster than mnemonics
   - Good for learning

2. **Use Mnemonics for Variety**
   - Different search space
   - Matches real wallet types

3. **Monitor Continuously**
   - Check dashboard regularly
   - Export stats periodically
   - Save found wallets immediately

### Security
1. **Protect Found Wallets**
   - Secure `found.txt` file
   - Don't share private keys
   - Move funds immediately if found

2. **Safe API Keys**
   - Don't expose API keys
   - Use free tiers for testing
   - Monitor usage limits

## Troubleshooting

### Issue: "Module not found" Error

**Problem**: Missing dependencies

**Solution**:
```bash
pip3 install base58 ecdsa requests PySimpleGUI
```

### Issue: "BIP0039.txt not found"

**Problem**: Mnemonic wordlist missing

**Solution**:
- Ensure `BIP0039.txt` is in the same directory
- Download if missing from repository

### Issue: Constant API Errors

**Problem**: Rate limiting or network issues

**Solutions**:
1. Increase API delay in settings
2. Switch to alternative API provider
3. Check internet connection
4. Wait 1 hour if rate limited

### Issue: GUI Won't Start

**Problem**: Display or PySimpleGUI issue

**Solutions**:
1. Check PySimpleGUI installation:
   ```bash
   pip3 install --upgrade PySimpleGUI
   ```
2. Try different theme
3. Use CLI version instead

### Issue: Slow Performance

**Problem**: System or network bottleneck

**Solutions**:
1. Close other applications
2. Check internet speed
3. Reduce API delay (but watch rate limits)
4. Use wired connection instead of WiFi

### Issue: No Results in Activity Log

**Problem**: Most addresses have 0 balance (expected)

**Solution**:
- This is normal - most addresses are empty
- Success rate is extremely low (~10^-48)
- Tool is working correctly

## FAQ

**Q: How long until I find a wallet with balance?**
A: Statistically, it could take billions of years. This is for educational purposes.

**Q: Is this legal?**
A: The tool itself is legal. Accessing wallets you don't own is illegal. Use responsibly.

**Q: Which version should I use?**
A: v3 Dashboard is recommended for most users - it has all features and best monitoring.

**Q: How many addresses can I check per day?**
A: With BlockCypher free tier: ~4,800 per day. With Blockchain.info: ~7,200 per day.

**Q: Can I run multiple instances?**
A: Technically yes, but you'll hit API rate limits faster. Not recommended.

**Q: What if I find a wallet with balance?**
A: It's saved to `found.txt`. Don't share the private key. Understand legal implications.

**Q: Why use mnemonic vs private key mode?**
A: Different search spaces. Mnemonics match how most real wallets are created.

**Q: Can I pause and resume?**
A: Yes, in v3! Use the Pause button. Stats are preserved.

**Q: How do I export my statistics?**
A: In v3, go to Menu → Export Stats. Creates a JSON file.

**Q: What's a good success rate?**
A: Any success is exceptional. Expect 0% - that's normal for this search space.

**Q: Can I add my own API provider?**
A: Yes, modify the code in v3. See `get_balance()` function.

**Q: Does it support other cryptocurrencies?**
A: No, only Bitcoin. Other coins would need different address generation.

**Q: What's the difference between satoshis and BTC?**
A: 1 BTC = 100,000,000 satoshis. v3 automatically converts to BTC.

**Q: Can I customize the GUI theme?**
A: Yes! Settings → Theme → Choose from 150+ options.

**Q: How accurate is the performance counter?**
A: Very accurate. Based on last 100 attempts with millisecond precision.

## Support

Need more help?

- **GitHub Issues**: https://github.com/DavidMGilbert/btc-hack/issues
- **Documentation**: See README-v3.md for technical details
- **Community**: Check existing issues for solutions

---

**Remember**: This tool is for educational purposes. Understanding probability, cryptography, and blockchain technology is the real value. Happy learning! 📚
