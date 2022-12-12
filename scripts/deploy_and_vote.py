from scripts.helpful_scripts import (
    get_account,
    CANDIDATES,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    FORKED_ENVIRONMENTS,
)
from brownie import network, VoteV2


def deploy_and_vote():
    account = get_account()
    vote = VoteV2.deploy({"from": account})
    for candidate_idx in range(len(CANDIDATES)):
        add_candidate_tx = vote.addCandidate(
            CANDIDATES[candidate_idx], {"from": account}
        )
        add_candidate_tx.wait(1)
    enter_tx = vote.enter({"from": account})
    enter_tx.wait(1)
    candidate_id = 0
    i_want_to_vote_this_candidate = CANDIDATES.index(CANDIDATES[candidate_id])
    vote_tx = vote.startVote(i_want_to_vote_this_candidate, {"from": account})
    vote_tx.wait(1)
    winnning_vote_tx = vote.getWinningVote({"from": account})
    winnning_vote_tx.wait(1)
    winner = vote.getWinner()
    print(winner)


def main():
    deploy_and_vote()
