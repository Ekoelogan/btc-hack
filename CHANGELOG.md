# Changelog

All notable changes to the BTC-Hack project will be documented in this file.

## [3.0.0] - 2026-02-03

### Added - v3 Dashboard Edition
- **Comprehensive Dashboard Interface**
  - Real-time statistics panel with session metrics
  - Performance monitoring (rate, hourly estimates)
  - API health tracking and error monitoring
  - Professional modern UI with color-coded status

- **Dual Search Modes**
  - Private Key Generation mode (random 256-bit keys)
  - BIP39 Mnemonic Phrase mode (12-24 word phrases)
  - Easy mode switching with dynamic UI updates

- **Advanced Features**
  - Start/Stop/Pause/Resume controls
  - Export statistics to JSON
  - Clear statistics option
  - Session history tracking
  - Last 100 attempts rate calculation

- **Multi-API Support**
  - BlockCypher API (primary)
  - Blockchain.info API (alternative)
  - Configurable API provider selection
  - Automatic satoshi to BTC conversion

- **Enhanced Logging**
  - Timestamped activity log
  - Emoji indicators for different events
  - Color-coded status messages
  - Real-time output window

- **Settings & Configuration**
  - Persistent settings saved to file
  - Theme selection (150+ themes)
  - API delay configuration
  - Auto-save toggle
  - API provider selection

- **Documentation**
  - Comprehensive README-v3.md
  - USAGE-GUIDE.md with tutorials
  - In-app documentation via Help menu
  - About dialog with project info

### Changed - All Versions
- **Updated API Endpoints**
  - Migrated from SoChain to BlockCypher
  - Fixed satoshi to BTC conversion (divide by 100,000,000)
  - Added proper timeout handling (10 seconds)

- **Improved Error Handling**
  - Specific exception catching (Timeout, RequestException)
  - Better error messages with emoji indicators
  - Graceful fallback on API failures

- **Code Quality**
  - Removed duplicate imports (hashlib in v2)
  - Added function docstrings
  - Improved code formatting
  - Better variable naming

- **Dependencies**
  - Updated to latest package versions
  - base58>=2.1.1 (was unversioned)
  - ecdsa>=0.19.0 (was 0.13)
  - requests>=2.31.0 (was 2.19.1)
  - PySimpleGUI>=5.0.0 (was unversioned)
  - Removed multiprocessing from requirements (built-in)

### Fixed
- Fixed balance calculation (satoshis to BTC conversion)
- Fixed API timeout issues
- Improved error handling in all versions
- Fixed duplicate hashlib import in v2

### Documentation
- Created README-v3.md with comprehensive v3 documentation
- Created USAGE-GUIDE.md with step-by-step tutorials
- Updated main README.md with v3 information
- Added version comparison table
- Added FAQ section

### Infrastructure
- Added .gitignore file
  - Python cache files
  - Virtual environments
  - IDE configurations
  - Settings files
  - Output files

## [2.1.0] - Previous

### Added
- BIP39 mnemonic phrase generation
- Configurable word count (3, 6, 9, 12, 15, 18, 21, 24 words)
- Passphrase file support
- Mnemonic-based address derivation

### Features
- GUI with PySimpleGUI
- Settings persistence
- Theme selection
- Win counter
- Attempts counter

## [2.0.0] - Previous

### Added
- Graphical User Interface using PySimpleGUI
- Settings window with theme selection
- Real-time attempt counter
- Success counter
- Start/Stop button
- Output window with formatted results

### Changed
- Switched from CLI to GUI
- Added settings persistence
- Improved user experience

## [1.0.0] - Original

### Added
- Initial release
- Command-line interface
- Multi-threaded processing
- Private key generation
- Public key derivation
- Bitcoin address generation
- Balance checking via API
- Found wallets saved to found.txt

### Features
- Process pooling with ThreadPool
- Queue-based architecture
- SoChain API integration (now deprecated)

---

## Migration Guide

### From v2.x to v3

1. **No Breaking Changes**: v3 is a new file, old versions still work
2. **New Features**: All v2 features are in v3, plus:
   - Dashboard
   - Both search modes
   - Better statistics
   - Export functionality

3. **To Migrate**:
   ```bash
   # Simply start using v3
   python3 btc-hack-v3-dashboard.py
   
   # Your old found.txt is still used
   # Settings will be regenerated
   ```

### From v1 to v3

1. **Interface Change**: CLI → GUI
2. **Dependencies**: Install PySimpleGUI
3. **Same Core**: Same cryptographic functions
4. **Benefits**: Visual feedback, statistics, pause/resume

---

## Upcoming Features (Planned)

- [ ] Multi-threading support in v3
- [ ] Database integration for tracking
- [ ] Chart visualizations (matplotlib)
- [ ] Custom address pattern matching
- [ ] Batch export of statistics
- [ ] API key management for premium tiers
- [ ] Additional cryptocurrency support
- [ ] Offline address database integration
- [ ] Machine learning optimizations
- [ ] Custom search strategies

---

## Version Support

| Version | Status | Support | Use Case |
|---------|--------|---------|----------|
| v3 | ✅ Active | Full | Recommended for all users |
| v2.1 | ✅ Active | Maintenance | Mnemonic-only searches |
| v2 | ✅ Active | Maintenance | Simple GUI searches |
| v1 | ✅ Active | Maintenance | CLI/automation |

---

## Contributing

See GitHub repository for contribution guidelines.

## License

See LICENSE file for details.
