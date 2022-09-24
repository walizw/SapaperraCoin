import pytest

from wallet.transaction import Transaction
from wallet.wallet import Wallet

def test_transaction ():
    sender_wallet = Wallet ()
    recipient = "0xdeaduwuowonyanya"
    amount = 150
    transaction = Transaction (sender_wallet, recipient, amount)

    assert transaction.output [recipient] == amount
    assert transaction.output [sender_wallet.address] == sender_wallet.balance - amount

    assert "timestamp" in transaction.input
    assert transaction.input ["amount"] == sender_wallet.balance
    assert transaction.input ["address"] == sender_wallet.address
    assert transaction.input ["public_key"] == sender_wallet.public_key

    assert Wallet.verify (transaction.input ["public_key"],
                          transaction.output,
                          transaction.input ["signature"])

def test_transaction_exceeds_balance ():
    with pytest.raises (Exception, match = "Amount exceeds balance"):
        Transaction (Wallet (), "0xdeaduwuowonyanya", 12800)

def test_transaction_update_exceeds_balance ():
    sender_wallet = Wallet ()
    transaction = Transaction (sender_wallet, "0xdeaduwuowonyanya", 50)

    with pytest.raises (Exception, match = "Amount exceeds balance"):
        transaction.update (sender_wallet, "0xfoobarmitzvah", 12800)

def test_transaction_update ():
    sender_wallet = Wallet ()

    first_recipient = "0xdeadfirstrecipient"
    first_amount = 50

    transaction = Transaction (sender_wallet, first_recipient, first_amount)

    next_recipient = "0xdeaduwuowonyanya"
    next_amount = 75
    transaction.update (sender_wallet, next_recipient, next_amount)

    assert transaction.output [next_recipient] == next_amount
    assert transaction.output [sender_wallet.address] == \
        sender_wallet.balance - first_amount - next_amount

    assert Wallet.verify (transaction.input ["public_key"],
                          transaction.output,
                          transaction.input ["signature"])

    first_amount2 = 25
    transaction.update (sender_wallet, first_recipient, first_amount2)
    
    assert transaction.output [first_recipient] == first_amount + first_amount2
    assert transaction.output [sender_wallet.address] == \
        sender_wallet.balance - first_amount - next_amount - first_amount2

    assert Wallet.verify (transaction.input ["public_key"],
                          transaction.output,
                          transaction.input ["signature"])

def test_valid_transaction ():
    Transaction.is_valid_transaction (Transaction (Wallet (), "0xdeaduwuowonyanya", 50))

def test_valid_transaction_invalid_outputs ():
    sender_wallet = Wallet ()
    transaction = Transaction (sender_wallet, "0xdeaduwuowonyanya", 50)
    transaction.output [sender_wallet.address] = 12800

    with pytest.raises (Exception, match="Invalid transaction output values"):
        Transaction.is_valid_transaction (transaction)

def test_valid_transaction_invalid_signature ():
    transaction = Transaction (Wallet (), "0xdeaduwuowonyanya", 50)
    transaction.input ["signature"] = Wallet ().sign (transaction.output)

    with pytest.raises (Exception, match="Invalid signature"):
        Transaction.is_valid_transaction (transaction)
