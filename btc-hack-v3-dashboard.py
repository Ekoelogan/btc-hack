#!/usr/bin/env python3
# BTC hack v3 - Enhanced Dashboard Edition
# Made by David Gilbert
# Enhanced with comprehensive dashboard and modern features
# https://github.com/DavidMGilbert/btc-hack
# https://www.davidmgilbert.com

import hashlib
import os
import random
import binascii
import requests
import ecdsa
import base58
import datetime
import time
import json
import hmac
import threading
from collections import deque
import PySimpleGUI as sg
from json import load as jsonload, dump as jsondump
from os import path

# Global variables for statistics
stats = {
    'total_attempts': 0,
    'total_successes': 0,
    'session_start': datetime.datetime.now(),
    'last_100_times': deque(maxlen=100),
    'api_calls': 0,
    'api_errors': 0,
    'mode': 'private_key'
}

# Configuration
SETTINGS_FILE = path.join(path.dirname(__file__), r'settings_file.cfg')
DEFAULT_SETTINGS = {
    'theme': 'DarkBlue3',
    'api_delay': 0.2,
    'auto_save': True,
    'api_provider': 'blockcypher'
}
SETTINGS_KEYS_TO_ELEMENT_KEYS = {
    'theme': '-THEME-',
    'api_delay': '-API_DELAY-',
    'auto_save': '-AUTO_SAVE-',
    'api_provider': '-API_PROVIDER-'
}

def generate_private_key():
    """Generate a random private key"""
    return binascii.hexlify(os.urandom(32)).decode('utf-8')

def private_key_to_WIF(private_key):
    """Convert private key to Wallet Import Format"""
    var80 = "80" + str(private_key)
    var = hashlib.sha256(binascii.unhexlify(hashlib.sha256(binascii.unhexlify(var80)).hexdigest())).hexdigest()
    return str(base58.b58encode(binascii.unhexlify(str(var80) + str(var[0:8]))), 'utf-8')

def private_key_to_public_key(private_key):
    """Convert private key to public key"""
    sign = ecdsa.SigningKey.from_string(binascii.unhexlify(private_key), curve=ecdsa.SECP256k1)
    return ('04' + binascii.hexlify(sign.verifying_key.to_string()).decode('utf-8'))

def public_key_to_address(public_key):
    """Convert public key to Bitcoin address"""
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    count = 0
    val = 0
    var = hashlib.new('ripemd160')
    var.update(hashlib.sha256(binascii.unhexlify(public_key.encode())).digest())
    doublehash = hashlib.sha256(hashlib.sha256(binascii.unhexlify(('00' + var.hexdigest()).encode())).digest()).hexdigest()
    address = '00' + var.hexdigest() + doublehash[0:8]
    for char in address:
        if (char != '0'):
            break
        count += 1
    count = count // 2
    n = int(address, 16)
    output = []
    while (n > 0):
        n, remainder = divmod(n, 58)
        output.append(alphabet[remainder])
    while (val < count):
        output.append(alphabet[0])
        val += 1
    return ''.join(output[::-1])

def bip39_mnemonic(num_words):
    """Generate BIP39 mnemonic phrase"""
    try:
        with open('BIP0039.txt', 'r') as f:
            words = f.read().split()
            return ' '.join([random.choice(words) for _ in range(int(num_words))])
    except FileNotFoundError:
        return None

def mnemonic_to_seed(mnemonic, passphrase=''):
    """Convert mnemonic to seed (simplified)"""
    combined = mnemonic + ' ' + passphrase
    return hashlib.sha256(combined.encode("utf-8")).hexdigest().upper()

def get_balance(address, api_provider='blockcypher', delay=0.2):
    """Check balance of Bitcoin address with multiple API support"""
    time.sleep(delay)
    stats['api_calls'] += 1
    
    try:
        if api_provider == 'blockcypher':
            response = requests.get(f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance", timeout=10)
            if response.status_code == 200:
                return float(response.json().get('balance', 0)) / 100000000  # Convert satoshis to BTC
        elif api_provider == 'blockchain.info':
            response = requests.get(f"https://blockchain.info/q/addressbalance/{address}", timeout=10)
            if response.status_code == 200:
                return float(response.text) / 100000000  # Convert satoshis to BTC
        return 0.0
    except Exception as e:
        stats['api_errors'] += 1
        return -1

def format_elapsed_time(td):
    """Format timedelta to readable string"""
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def calculate_rate():
    """Calculate attempts per second"""
    if len(stats['last_100_times']) < 2:
        return 0.0
    time_diff = (stats['last_100_times'][-1] - stats['last_100_times'][0]).total_seconds()
    if time_diff > 0:
        return len(stats['last_100_times']) / time_diff
    return 0.0

def save_found_wallet(data, balance, mode='private_key'):
    """Save found wallet to file"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("found.txt", "a") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Found at: {timestamp}\n")
        f.write(f"Mode: {mode}\n")
        if mode == 'mnemonic':
            f.write(f"Mnemonic: {data.get('mnemonic', 'N/A')}\n")
            f.write(f"Passphrase: {data.get('passphrase', 'N/A')}\n")
        f.write(f"Address: {data['address']}\n")
        f.write(f"Private key: {data['private_key']}\n")
        f.write(f"WIF: {data['wif']}\n")
        f.write(f"Public key: {data['public_key']}\n")
        f.write(f"Balance: {balance} BTC\n")
        f.write(f"{'='*60}\n\n")

def load_settings(settings_file, default_settings):
    """Load settings from file"""
    try:
        with open(settings_file, 'r') as f:
            settings = jsonload(f)
        # Merge with defaults for any missing keys
        for key in default_settings:
            if key not in settings:
                settings[key] = default_settings[key]
        return settings
    except Exception:
        return default_settings.copy()

def save_settings(settings_file, settings, values=None):
    """Save settings to file"""
    if values:
        for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:
            try:
                settings[key] = values[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(f'Problem updating settings. Key = {key}: {e}')
    
    with open(settings_file, 'w') as f:
        jsondump(settings, f, indent=2)

def create_settings_window(settings):
    """Create settings window"""
    sg.theme(settings['theme'])
    
    def TextLabel(text):
        return sg.Text(text+':', justification='r', size=(15, 1))
    
    layout = [
        [sg.Text('Settings', font='Any 15')],
        [TextLabel('Theme'), sg.Combo(sg.theme_list(), size=(20, 20), key='-THEME-')],
        [TextLabel('API Delay (sec)'), sg.Input(size=(20, 1), key='-API_DELAY-')],
        [TextLabel('Auto Save'), sg.Checkbox('', key='-AUTO_SAVE-')],
        [TextLabel('API Provider'), sg.Combo(['blockcypher', 'blockchain.info'], size=(20, 1), key='-API_PROVIDER-')],
        [sg.Button('Save'), sg.Button('Exit')]
    ]
    
    window = sg.Window('Settings', layout, keep_on_top=True, finalize=True)
    
    # Update values
    try:
        window['-THEME-'].update(value=settings.get('theme', 'DarkBlue3'))
        window['-API_DELAY-'].update(value=str(settings.get('api_delay', 0.2)))
        window['-AUTO_SAVE-'].update(value=settings.get('auto_save', True))
        window['-API_PROVIDER-'].update(value=settings.get('api_provider', 'blockcypher'))
    except Exception as e:
        print(f'Problem updating window: {e}')
    
    return window

def create_dashboard_window(settings):
    """Create main dashboard window"""
    sg.theme(settings['theme'])
    
    menu_def = [
        ['&Menu', ['&Settings', '&Export Stats', '&Clear Stats', 'E&xit']],
        ['&Help', ['&About', '&Documentation']]
    ]
    
    # Statistics column
    stats_col = [
        [sg.Text('DASHBOARD STATISTICS', font=('Helvetica', 12, 'bold'), text_color='cyan')],
        [sg.HorizontalSeparator()],
        [sg.Text('Session Started:', size=(20, 1)), sg.Text('', size=(25, 1), key='-SESSION_START-')],
        [sg.Text('Elapsed Time:', size=(20, 1)), sg.Text('', size=(25, 1), key='-ELAPSED-')],
        [sg.Text('Total Attempts:', size=(20, 1)), sg.Text('0', size=(25, 1), key='-ATTEMPTS-', font=('Helvetica', 10, 'bold'))],
        [sg.Text('Wallets Found:', size=(20, 1)), sg.Text('0', size=(25, 1), key='-FOUND-', font=('Helvetica', 10, 'bold'), text_color='green')],
        [sg.Text('Success Rate:', size=(20, 1)), sg.Text('0%', size=(25, 1), key='-SUCCESS_RATE-')],
        [sg.HorizontalSeparator()],
        [sg.Text('PERFORMANCE METRICS', font=('Helvetica', 12, 'bold'), text_color='cyan')],
        [sg.HorizontalSeparator()],
        [sg.Text('Current Rate:', size=(20, 1)), sg.Text('0.00/sec', size=(25, 1), key='-RATE-')],
        [sg.Text('Est. Hourly:', size=(20, 1)), sg.Text('0', size=(25, 1), key='-EST_HOURLY-')],
        [sg.Text('API Calls:', size=(20, 1)), sg.Text('0', size=(25, 1), key='-API_CALLS-')],
        [sg.Text('API Errors:', size=(20, 1)), sg.Text('0', size=(25, 1), key='-API_ERRORS-')],
        [sg.Text('API Health:', size=(20, 1)), sg.Text('Unknown', size=(25, 1), key='-API_HEALTH-')],
        [sg.HorizontalSeparator()],
    ]
    
    # Control column
    control_col = [
        [sg.Text('SEARCH MODE', font=('Helvetica', 12, 'bold'), text_color='cyan')],
        [sg.HorizontalSeparator()],
        [sg.Radio('Private Key Generation', 'MODE', default=True, key='-MODE_PRIVKEY-', enable_events=True)],
        [sg.Radio('Mnemonic Phrase', 'MODE', key='-MODE_MNEMONIC-', enable_events=True)],
        [sg.HorizontalSeparator()],
        [sg.Text('MNEMONIC OPTIONS', font=('Helvetica', 10, 'bold'))],
        [sg.Text('Number of words:'), sg.Combo(['12', '15', '18', '21', '24'], default_value='12', size=(10, 1), key='-MNEMONIC_WORDS-', disabled=True)],
        [sg.Text('Passphrase file:'), sg.Input(size=(20, 1), key='-PASSPHRASE_FILE-', disabled=True), sg.FileBrowse(disabled=True, key='-PASSPHRASE_BROWSE-')],
        [sg.HorizontalSeparator()],
        [sg.Text('')],
        [sg.Button('Start', size=(15, 2), font=('Helvetica', 12, 'bold'), button_color=('white', 'green'), key='-START_STOP-')],
        [sg.Button('Pause', size=(15, 1), disabled=True, key='-PAUSE-')],
        [sg.Text('')],
    ]
    
    # Output area
    output_frame = [
        [sg.Text('RECENT ACTIVITY LOG', font=('Helvetica', 12, 'bold'), text_color='cyan')],
        [sg.Multiline(size=(95, 15), font=('Courier', 9), key='-OUTPUT-', autoscroll=True, disabled=True, 
                      write_only=False, reroute_stdout=False, reroute_stderr=False)]
    ]
    
    # Main layout
    layout = [
        [sg.Menu(menu_def)],
        [sg.Text('BTC HACK v3 - ENHANCED DASHBOARD', font=('Helvetica', 16, 'bold'), 
                 justification='center', expand_x=True, text_color='yellow')],
        [sg.HorizontalSeparator()],
        [
            sg.Column(stats_col, vertical_alignment='top'),
            sg.VerticalSeparator(),
            sg.Column(control_col, vertical_alignment='top')
        ],
        [sg.HorizontalSeparator()],
        output_frame,
        [sg.HorizontalSeparator()],
        [sg.Text('Status:'), sg.Text('Ready', size=(80, 1), key='-STATUS-', text_color='yellow')]
    ]
    
    return sg.Window('BTC Hack v3 - Dashboard', layout, finalize=True, resizable=True)

def update_dashboard(window, settings):
    """Update dashboard statistics"""
    # Calculate statistics
    elapsed = datetime.datetime.now() - stats['session_start']
    rate = calculate_rate()
    est_hourly = int(rate * 3600)
    
    success_rate = 0
    if stats['total_attempts'] > 0:
        success_rate = (stats['total_successes'] / stats['total_attempts']) * 100
    
    # API health
    api_health = 'Healthy'
    if stats['api_calls'] > 0:
        error_rate = (stats['api_errors'] / stats['api_calls']) * 100
        if error_rate > 10:
            api_health = 'Poor'
        elif error_rate > 5:
            api_health = 'Fair'
    
    # Update window
    window['-SESSION_START-'].update(stats['session_start'].strftime("%Y-%m-%d %H:%M:%S"))
    window['-ELAPSED-'].update(format_elapsed_time(elapsed))
    window['-ATTEMPTS-'].update(str(stats['total_attempts']))
    window['-FOUND-'].update(str(stats['total_successes']))
    window['-SUCCESS_RATE-'].update(f"{success_rate:.8f}%")
    window['-RATE-'].update(f"{rate:.2f}/sec")
    window['-EST_HOURLY-'].update(str(est_hourly))
    window['-API_CALLS-'].update(str(stats['api_calls']))
    window['-API_ERRORS-'].update(str(stats['api_errors']))
    window['-API_HEALTH-'].update(api_health)

def log_output(window, message):
    """Add message to output log"""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    window['-OUTPUT-'].print(f"[{timestamp}] {message}")

def process_private_key_mode(window, settings):
    """Process in private key generation mode"""
    start = datetime.datetime.now()
    
    # Generate private key
    private_key = generate_private_key()
    public_key = private_key_to_public_key(private_key)
    address = public_key_to_address(public_key)
    wif = private_key_to_WIF(private_key)
    
    # Check balance
    balance = get_balance(address, settings['api_provider'], settings['api_delay'])
    
    stats['total_attempts'] += 1
    stats['last_100_times'].append(datetime.datetime.now())
    
    # Log result
    if balance == -1:
        log_output(window, f"⚠️  API Error checking {address}")
        window['-STATUS-'].update('API Error - Check connection', text_color='red')
    elif balance > 0:
        stats['total_successes'] += 1
        log_output(window, f"💰 FOUND! Address: {address} | Balance: {balance} BTC")
        window['-STATUS-'].update(f'WALLET FOUND with {balance} BTC!', text_color='green')
        
        # Save to file
        data = {
            'address': address,
            'private_key': private_key,
            'public_key': public_key.upper(),
            'wif': wif
        }
        save_found_wallet(data, balance, 'private_key')
    else:
        log_output(window, f"🔍 Address: {address[:20]}... | Balance: 0 BTC")
        window['-STATUS-'].update(f'Searching... Last: {address[:30]}...', text_color='yellow')

def process_mnemonic_mode(window, settings, num_words, passphrase_file):
    """Process in mnemonic phrase mode"""
    start = datetime.datetime.now()
    
    # Generate mnemonic
    mnemonic = bip39_mnemonic(num_words)
    if mnemonic is None:
        log_output(window, "⚠️  Error: BIP0039.txt file not found")
        return
    
    # Get passphrase if file provided
    passphrase = ''
    if passphrase_file and os.path.exists(passphrase_file):
        try:
            with open(passphrase_file, 'r') as f:
                words = f.read().split()
                if words:
                    passphrase = random.choice(words)
        except Exception:
            pass
    
    # Generate address from mnemonic
    seed = mnemonic_to_seed(mnemonic, passphrase)
    
    try:
        public_key = private_key_to_public_key(seed.lower())
        address = public_key_to_address(public_key)
        wif = private_key_to_WIF(seed.lower())
    except Exception as e:
        log_output(window, f"⚠️  Error generating address from mnemonic: {e}")
        return
    
    # Check balance
    balance = get_balance(address, settings['api_provider'], settings['api_delay'])
    
    stats['total_attempts'] += 1
    stats['last_100_times'].append(datetime.datetime.now())
    
    # Log result
    if balance == -1:
        log_output(window, f"⚠️  API Error checking {address}")
        window['-STATUS-'].update('API Error - Check connection', text_color='red')
    elif balance > 0:
        stats['total_successes'] += 1
        log_output(window, f"💰 FOUND! Mnemonic: {mnemonic[:30]}... | Balance: {balance} BTC")
        window['-STATUS-'].update(f'WALLET FOUND with {balance} BTC!', text_color='green')
        
        # Save to file
        data = {
            'address': address,
            'private_key': seed,
            'public_key': public_key.upper(),
            'wif': wif,
            'mnemonic': mnemonic,
            'passphrase': passphrase
        }
        save_found_wallet(data, balance, 'mnemonic')
    else:
        log_output(window, f"🔍 Mnemonic: {mnemonic[:30]}... | Address: {address[:20]}... | Balance: 0 BTC")
        window['-STATUS-'].update(f'Searching... Last: {address[:30]}...', text_color='yellow')

def export_statistics():
    """Export statistics to JSON file"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"btc_hack_stats_{timestamp}.json"
    
    export_data = {
        'session_start': stats['session_start'].isoformat(),
        'session_end': datetime.datetime.now().isoformat(),
        'total_attempts': stats['total_attempts'],
        'total_successes': stats['total_successes'],
        'api_calls': stats['api_calls'],
        'api_errors': stats['api_errors'],
        'mode': stats['mode']
    }
    
    with open(filename, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    return filename

def main():
    """Main application loop"""
    settings = load_settings(SETTINGS_FILE, DEFAULT_SETTINGS)
    window = create_dashboard_window(settings)
    
    running = False
    paused = False
    
    # Initialize dashboard
    window['-SESSION_START-'].update(stats['session_start'].strftime("%Y-%m-%d %H:%M:%S"))
    log_output(window, "🚀 BTC Hack v3 Dashboard initialized")
    log_output(window, "ℹ️  Configure your settings and click Start to begin")
    
    while True:
        event, values = window.read(timeout=100)
        
        if event in (None, 'Exit'):
            break
        
        # Update dashboard
        if running and not paused:
            update_dashboard(window, settings)
        
        # Menu events
        if event == 'Settings':
            settings_window = create_settings_window(settings)
            s_event, s_values = settings_window.read(close=True)
            if s_event == 'Save':
                save_settings(SETTINGS_FILE, settings, s_values)
                settings = load_settings(SETTINGS_FILE, DEFAULT_SETTINGS)
                sg.popup('Settings saved! Please restart for theme changes to take effect.', 
                        title='Settings Saved')
        
        elif event == 'Export Stats':
            filename = export_statistics()
            sg.popup(f'Statistics exported to {filename}', title='Export Complete')
        
        elif event == 'Clear Stats':
            if sg.popup_yes_no('Are you sure you want to clear all statistics?', title='Confirm') == 'Yes':
                stats['total_attempts'] = 0
                stats['total_successes'] = 0
                stats['session_start'] = datetime.datetime.now()
                stats['last_100_times'].clear()
                stats['api_calls'] = 0
                stats['api_errors'] = 0
                log_output(window, "📊 Statistics cleared")
        
        elif event == 'About':
            sg.popup('BTC Hack v3 - Enhanced Dashboard Edition\n\n'
                    'An advanced Bitcoin wallet brute force tool\n'
                    'with comprehensive dashboard and analytics.\n\n'
                    'Made by David Gilbert\n'
                    'Enhanced with modern features\n\n'
                    'https://github.com/DavidMGilbert/btc-hack',
                    title='About')
        
        elif event == 'Documentation':
            sg.popup('BTC Hack v3 Documentation\n\n'
                    'MODES:\n'
                    '• Private Key: Generates random private keys\n'
                    '• Mnemonic: Generates BIP39 mnemonic phrases\n\n'
                    'FEATURES:\n'
                    '• Real-time dashboard with statistics\n'
                    '• Multiple API providers\n'
                    '• Performance metrics\n'
                    '• Export/Import functionality\n'
                    '• Session history\n\n'
                    'USAGE:\n'
                    '1. Select search mode\n'
                    '2. Configure settings if needed\n'
                    '3. Click Start to begin\n'
                    '4. Found wallets are saved to found.txt\n\n'
                    'Note: This is for educational purposes only.',
                    title='Documentation')
        
        # Mode change events
        elif event == '-MODE_PRIVKEY-':
            window['-MNEMONIC_WORDS-'].update(disabled=True)
            window['-PASSPHRASE_FILE-'].update(disabled=True)
            window['-PASSPHRASE_BROWSE-'].update(disabled=True)
            stats['mode'] = 'private_key'
        
        elif event == '-MODE_MNEMONIC-':
            window['-MNEMONIC_WORDS-'].update(disabled=False)
            window['-PASSPHRASE_FILE-'].update(disabled=False)
            window['-PASSPHRASE_BROWSE-'].update(disabled=False)
            stats['mode'] = 'mnemonic'
        
        # Start/Stop button
        elif event == '-START_STOP-':
            running = not running
            if running:
                window['-START_STOP-'].update('Stop', button_color=('white', 'red'))
                window['-PAUSE-'].update(disabled=False)
                paused = False
                log_output(window, f"▶️  Search started in {stats['mode']} mode")
                window['-STATUS-'].update('Running...', text_color='green')
            else:
                window['-START_STOP-'].update('Start', button_color=('white', 'green'))
                window['-PAUSE-'].update(disabled=True)
                log_output(window, "⏹️  Search stopped")
                window['-STATUS-'].update('Stopped', text_color='red')
        
        # Pause button
        elif event == '-PAUSE-':
            paused = not paused
            if paused:
                window['-PAUSE-'].update('Resume')
                log_output(window, "⏸️  Search paused")
                window['-STATUS-'].update('Paused', text_color='orange')
            else:
                window['-PAUSE-'].update('Pause')
                log_output(window, "▶️  Search resumed")
                window['-STATUS-'].update('Running...', text_color='green')
        
        # Process if running and not paused
        if running and not paused:
            try:
                if values['-MODE_PRIVKEY-']:
                    process_private_key_mode(window, settings)
                else:
                    num_words = values['-MNEMONIC_WORDS-']
                    passphrase_file = values['-PASSPHRASE_FILE-']
                    process_mnemonic_mode(window, settings, num_words, passphrase_file)
            except Exception as e:
                log_output(window, f"❌ Error: {str(e)}")
                window['-STATUS-'].update(f'Error: {str(e)}', text_color='red')
    
    window.close()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        sg.popup_error(f'Fatal error: {str(e)}', title='Error')
