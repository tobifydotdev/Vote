from brownie import network, accounts, config

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "gabnache-local"]
FORKED_ENVIRONMENTS = ["mainnet-fork-dev"]
CANDIDATES = ["ST_BERNARD", "SIR_LANCELOT", "KLAUS"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if network.show_active() in FORKED_ENVIRONMENTS:
        return accounts[0]
    return accounts.load("tobiade")
    # return accounts.add(config["wallets"]["from_key"])
