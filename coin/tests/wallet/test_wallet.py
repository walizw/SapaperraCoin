from wallet.wallet import Wallet

def test_verify_valid_signature ():
    data = { "foo": "bar" }
    wallet = Wallet ()
    signature = wallet.sign (data)

    assert Wallet.verify (wallet.public_key, data, signature) == True

def test_verify_invalid_signature ():
    data = { "foo": "bar" }
    wallet = Wallet ()
    signature = wallet.sign (data)

    assert Wallet.verify (wallet.public_key, { "FOo": "bAR" }, signature) == False
