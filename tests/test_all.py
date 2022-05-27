from scripts.helpful_scripts import get_account
from scripts.deploy_testTokens import deploy_tokenA, deploy_tokenB
from scripts.deploy_token import deploy as deploy_token
from scripts.deploy_SwapContract import deploy as deploy_contract

DECIMALS = 18

def test_can_Deploy():
    account = get_account()
    tokenA = deploy_tokenA()
    tokenB = deploy_tokenB()
    MyToken = deploy_token()
    Swap = deploy_contract(tokenA, tokenB, MyToken)

    MyToken.transfer(Swap.address, 100 * 10 ** DECIMALS, {"from": account})
    tokenA.transfer(Swap.address, 100 * 10 ** DECIMALS, {"from": account})
    tokenB.transfer(Swap.address, 100 * 10 ** DECIMALS, {"from": account})

    assert tokenA.balanceOf(Swap.address) == 100 * 10 ** DECIMALS
    assert tokenB.balanceOf(Swap.address) == 100 * 10 ** DECIMALS
    assert MyToken.balanceOf(Swap.address) == 100 * 10 ** DECIMALS


def test_swap():
    account = get_account()
    tokenA = deploy_tokenA()
    tokenB = deploy_tokenB()
    MyToken = deploy_token()
    Swap = deploy_contract(tokenA, tokenB, MyToken)

    MyToken.transfer(Swap.address, 100 * 10 ** DECIMALS, {"from": account})
    tokenA.transfer(Swap.address, 100 * 10 ** DECIMALS, {"from": account})
    tokenB.transfer(Swap.address, 100 * 10 ** DECIMALS, {"from": account})

    assert tokenA.balanceOf(Swap.address) == 100 * 10 ** DECIMALS
    assert tokenB.balanceOf(Swap.address) == 100 * 10 ** DECIMALS

    amount = 50 * 10 ** DECIMALS

    tokenA.approve(Swap.address, amount, {"from": account})
    Swap.swap(tokenA.address, amount, {"from": account})

    assert tokenA.balanceOf(Swap.address) == 100 * 10 ** DECIMALS + amount
    assert tokenB.balanceOf(Swap.address) == 100 * 10 ** DECIMALS - amount


def test_reward():
    account = get_account()
    tokenA = deploy_tokenA()
    tokenB = deploy_tokenB()
    MyToken = deploy_token()
    Swap = deploy_contract(tokenA, tokenB, MyToken)

    MyToken.transfer(Swap.address, 200 * 10 ** DECIMALS, {"from": account})
    tokenA.transfer(Swap.address, 300 * 10 ** DECIMALS, {"from": account})
    tokenB.transfer(Swap.address, 300 * 10 ** DECIMALS, {"from": account})

    assert tokenA.balanceOf(Swap.address) == 300 * 10 ** DECIMALS
    assert tokenB.balanceOf(Swap.address) == 300 * 10 ** DECIMALS

    amount = 200 * 10 ** DECIMALS
    user_balance = MyToken.balanceOf(account.address)

    tokenA.approve(Swap.address, amount, {"from": account})
    Swap.swap(tokenA.address, amount, {"from": account})

    assert tokenA.balanceOf(Swap.address) == 300 * 10 ** DECIMALS + amount
    assert tokenB.balanceOf(Swap.address) == 300 * 10 ** DECIMALS - amount
    assert MyToken.balanceOf(account.address) == user_balance + 50 * 10 ** DECIMALS
    assert MyToken.balanceOf(Swap.address) == 150 * 10 ** DECIMALS
