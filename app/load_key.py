def load_key():
    with open('keys/key_api0') as f:
        key = f.read().strip()
    return key


if __name__ == '__main__':
    print(load_key())
