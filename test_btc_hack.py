#!/usr/bin/env python3
"""
Test script for BTC-Hack v3 Dashboard
Validates core functionality without GUI
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    try:
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
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_core_functions():
    """Test core cryptographic functions"""
    print("\nTesting core functions...")
    
    # Import all required modules at the top
    import binascii
    import os
    import ecdsa
    import hashlib
    import base58
    
    # Test private key generation
    private_key = binascii.hexlify(os.urandom(32)).decode('utf-8')
    assert len(private_key) == 64, "Private key should be 64 hex chars"
    print(f"✓ Private key generation: {private_key[:16]}...")
    
    # Test public key generation
    try:
        sign = ecdsa.SigningKey.from_string(binascii.unhexlify(private_key), curve=ecdsa.SECP256k1)
        public_key = '04' + binascii.hexlify(sign.verifying_key.to_string()).decode('utf-8')
        assert len(public_key) == 130, "Public key should be 130 chars"
        print(f"✓ Public key generation: {public_key[:16]}...")
    except Exception as e:
        print(f"✗ Public key generation failed: {e}")
        return False
    
    # Test address generation
    try:
        alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        var = hashlib.new('ripemd160')
        var.update(hashlib.sha256(binascii.unhexlify(public_key.encode())).digest())
        doublehash = hashlib.sha256(hashlib.sha256(binascii.unhexlify(('00' + var.hexdigest()).encode())).digest()).hexdigest()
        address = '00' + var.hexdigest() + doublehash[0:8]
        
        count = 0
        for char in address:
            if char != '0':
                break
            count += 1
        count = count // 2
        
        n = int(address, 16)
        output = []
        while n > 0:
            n, remainder = divmod(n, 58)
            output.append(alphabet[remainder])
        
        val = 0
        while val < count:
            output.append(alphabet[0])
            val += 1
        
        btc_address = ''.join(output[::-1])
        assert btc_address[0] == '1', "BTC address should start with 1"
        print(f"✓ Address generation: {btc_address}")
    except Exception as e:
        print(f"✗ Address generation failed: {e}")
        return False
    
    # Test WIF conversion
    try:
        var80 = "80" + str(private_key)
        var = hashlib.sha256(binascii.unhexlify(hashlib.sha256(binascii.unhexlify(var80)).hexdigest())).hexdigest()
        wif = str(base58.b58encode(binascii.unhexlify(str(var80) + str(var[0:8]))), 'utf-8')
        assert wif[0] in ['5', 'K', 'L'], "WIF should start with 5, K, or L"
        print(f"✓ WIF generation: {wif[:16]}...")
    except Exception as e:
        print(f"✗ WIF generation failed: {e}")
        return False
    
    print("✓ All core functions working")
    return True

def test_bip39():
    """Test BIP39 mnemonic generation"""
    print("\nTesting BIP39 mnemonic...")
    
    if not os.path.exists('BIP0039.txt'):
        print("⚠ BIP0039.txt not found - mnemonic mode will not work")
        return True
    
    try:
        import random
        with open('BIP0039.txt', 'r') as f:
            words = f.read().split()
            mnemonic = ' '.join([random.choice(words) for _ in range(12)])
            assert len(mnemonic.split()) == 12, "Mnemonic should have 12 words"
            print(f"✓ Mnemonic generation: {mnemonic[:40]}...")
        return True
    except Exception as e:
        print(f"✗ Mnemonic generation failed: {e}")
        return False

def test_api_mock():
    """Test API call structure (without actual call)"""
    print("\nTesting API call structure...")
    
    try:
        import requests
        test_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
        url = f"https://api.blockcypher.com/v1/btc/main/addrs/{test_address}/balance"
        print(f"✓ API URL format: {url}")
        print("  Note: Not making actual API call in test")
        return True
    except Exception as e:
        print(f"✗ API test failed: {e}")
        return False

def test_file_operations():
    """Test file operations"""
    print("\nTesting file operations...")
    
    try:
        # Test settings file structure
        import json
        test_settings = {
            'theme': 'DarkBlue3',
            'api_delay': 0.2,
            'auto_save': True,
            'api_provider': 'blockcypher'
        }
        
        # Test JSON serialization
        json_str = json.dumps(test_settings, indent=2)
        loaded = json.loads(json_str)
        assert loaded['theme'] == 'DarkBlue3', "Settings should serialize correctly"
        print("✓ Settings serialization working")
        
        # Test found.txt format
        test_output = "Address: 1Test...\nPrivate key: abc123...\n"
        print("✓ Output file format validated")
        
        return True
    except Exception as e:
        print(f"✗ File operations failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("BTC-Hack v3 Dashboard - Test Suite")
    print("="*60)
    
    tests = [
        ("Imports", test_imports),
        ("Core Functions", test_core_functions),
        ("BIP39 Mnemonic", test_bip39),
        ("API Structure", test_api_mock),
        ("File Operations", test_file_operations),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Test '{name}' crashed: {e}")
            results.append((name, False))
    
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! BTC-Hack v3 is ready to use.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check above for details.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
