# Performance Improvements Summary

This document outlines the performance optimizations made to the BTC-Hack codebase.

## Overview

The following optimizations were implemented to improve code efficiency, reduce redundant calculations, and enhance overall performance:

## 1. HTTP Session Caching (All Files)

**Issue**: Each API request created a new HTTP connection, adding overhead.

**Solution**: Implemented a reusable `requests.Session()` object that maintains connection pooling.

```python
# Before
response = requests.get("https://api.blockcypher.com/v1/btc/main/addrs/" + str(address) + "/balance")

# After
_session = requests.Session()
response = _session.get(f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance")
```

**Impact**: Reduced connection overhead, faster API requests through connection reuse.

## 2. Eliminated Redundant Calculations (btc-hack.py, btc-hack-v2.py)

**Issue**: WIF and public keys were recalculated multiple times when printing and saving results.

**Solution**: Calculate once and cache the result in a variable.

```python
# Before
print("WIF private key: " + str(private_key_to_WIF(private_key)))
file.write("WIF private key: " + str(private_key_to_WIF(private_key)))
file.write("Public key: " + str(private_key_to_public_key(private_key)).upper())

# After
wif_key = private_key_to_WIF(private_key)
pub_key = private_key_to_public_key(private_key).upper()
print(f"WIF private key: {wif_key}")
file.write(f"WIF private key: {wif_key}")
file.write(f"Public key: {pub_key}")
```

**Impact**: Eliminated CPU-intensive cryptographic operations being performed 2-3 times per address.

## 3. Optimized String Concatenation (All Files)

**Issue**: Used inefficient string concatenation with `+` operator.

**Solution**: Replaced with f-strings (Python 3.6+) for better performance and readability.

```python
# Before
print("Address: " + "{:<34}".format(str(address)) + "\n" + "Private key: " + str(private_key))

# After
print(f"Address: {address:<34}\n"
      f"Private key: {private_key}")
```

**Impact**: Faster string formatting, reduced memory allocations.

## 4. BIP0039 Word List Caching (btc-hack-v2.1-mnemonic.py)

**Issue**: BIP0039.txt file was read from disk on every mnemonic generation.

**Solution**: Implemented lazy loading with in-memory caching.

```python
# Before
def bip(num):
    with open('BIP0039.txt', 'r') as f:
        words = f.read().split()
        # ... generate mnemonic

# After
_bip_words = None

def _load_bip_words():
    global _bip_words
    if _bip_words is None:
        with open('BIP0039.txt', 'r') as f:
            _bip_words = f.read().split()
    return _bip_words

def bip(num):
    words = _load_bip_words()
    # ... generate mnemonic
```

**Impact**: Eliminated repeated file I/O operations, reads file only once per session.

## 5. Optimized Mnemonic/Passphrase Generation (btc-hack-v2.1-mnemonic.py)

**Issue**: Inefficient loops with unnecessary iterations.

**Solution**: Simplified logic with direct list comprehension.

```python
# Before
def bip(num):
    with open('BIP0039.txt', 'r') as f:
        words = f.read().split()
        for word in words:  # Unnecessary loop
            sent = [random.choice(words) for word in range(int(num))]
            return ' '.join(sent)

# After
def bip(num):
    words = _load_bip_words()
    sent = [random.choice(words) for _ in range(int(num))]
    return ' '.join(sent)
```

**Impact**: Removed unnecessary iteration, cleaner and faster code.

## 6. Improved File Handling (All Files)

**Issue**: Files opened without context managers, risking resource leaks.

**Solution**: Use `with` statements for automatic resource cleanup.

```python
# Before
file = open("found.txt", "a")
file.write(...)
file.close()

# After
with open("found.txt", "a") as file:
    file.write(...)
```

**Impact**: Guaranteed file closure, prevents resource leaks.

## 7. Optimized Base58 Address Encoding (All Files)

**Issue**: Inefficient loop to count leading zeros and add padding.

**Solution**: Used string methods for counting and list extend for padding.

```python
# Before
count = 0; val = 0
for char in address:
    if (char != '0'):
        break
    count += 1
while (val < count):
    output.append(alphabet[0])
    val += 1

# After
count = len(address) - len(address.lstrip('0'))
count = count // 2
output.extend([alphabet[0]] * count)
```

**Impact**: Faster execution, more Pythonic code.

## 8. Fixed Duplicate Import (btc-hack-v2.py)

**Issue**: `hashlib` was imported twice.

**Solution**: Removed duplicate import.

```python
# Before
import hashlib
import os
import hashlib  # Duplicate

# After
import hashlib
import os
```

**Impact**: Cleaner code, reduced parsing overhead.

## 9. Removed Unnecessary Data Tuples (btc-hack-v2.py, btc-hack-v2.1-mnemonic.py)

**Issue**: Created unnecessary tuple just to extract values.

**Solution**: Use variables directly.

```python
# Before
data = (private_key, address)
balance = get_balance(data[1])
private_key = data[0]
address = data[1]

# After
balance = get_balance(address)
# Use private_key and address directly
```

**Impact**: Reduced memory allocations, clearer code.

## 10. Consolidated Output String (btc-hack-v2.1-mnemonic.py)

**Issue**: Same output string constructed twice (once for print, once for file).

**Solution**: Build string once and reuse.

```python
# Before
print('mnemonic: ' + str(mnemonic) + '...')
file.write('mnemonic: ' + str(mnemonic) + '...')

# After
output_str = f'mnemonic: {mnemonic}...'
print(output_str)
file.write(output_str)
```

**Impact**: Reduced string operations, DRY principle.

## Performance Metrics (Estimated)

While specific benchmarks depend on system configuration and API response times, the improvements are estimated to provide:

- **~30-50% reduction** in redundant cryptographic operations (based on eliminating 2-3 recalculations)
- **~90% reduction** in file I/O for mnemonic generation after first load (one read vs. multiple reads)
- **~10-20% improvement** in HTTP request performance through connection pooling (typical session reuse gains)
- **~5-10% improvement** in address generation through optimized string operations

*Note: These are estimates based on typical performance characteristics of the optimizations applied. Actual improvements may vary based on hardware, network conditions, and usage patterns.*

## Future Optimization Opportunities

1. **Batch API Requests**: Query multiple addresses in a single API call if supported
2. **Async/Await**: Use `asyncio` and `aiohttp` for concurrent API requests
3. **Pre-computation**: Generate and cache private/public key pairs
4. **Database Integration**: Use local database for address lookup before API calls
5. **Multiprocessing Optimization**: Better load balancing in btc-hack.py

## Compatibility

All optimizations maintain backward compatibility with Python 3.6+ and preserve the original functionality.
