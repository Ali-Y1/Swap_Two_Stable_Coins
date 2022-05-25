from brownie import Swap
from scripts.helpful_scripts import get_account
from web3 import Web3

def deploy(tokenA,tokenB,myToken):
    account = get_account()
    swap = Swap.deploy(tokenA,tokenB,myToken, {"from": account})
    print(" Deployed")
    return swap


