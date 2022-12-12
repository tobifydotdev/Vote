from brownie import VoteV2, network, accounts
from scripts.helpful_scripts import (
    CANDIDATES,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
)
import pytest


def test_can_vote_integration():
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    else:
        account = get_account()
        vote = VoteV2.deploy({"from": account})
        for candidate_idx in range(len(CANDIDATES)):
            add_candidate_tx = vote.addCandidate(
                CANDIDATES[candidate_idx], {"from": account}
            )
            add_candidate_tx.wait(1)
        enter_tx = vote.enter({"from": account})
        enter_tx.wait(1)
        vote_tx = vote.startVote(CANDIDATES[0], {"from": account})
        vote_tx.wait(1)
        # name_list = []
        # vote_count_list = []
        """for candidate_idx in range(len(CANDIDATES)):
            name, vote_count = vote.getCandidateInfo(
                CANDIDATES[candidate_idx], {"from": account}
            )
            name_list.append(name)
            vote_count_list.append(vote_count)"""
        winnning_vote_tx = vote.getWinningVote({"from": account})
        winnning_vote_tx.wait(1)
        assert (
            vote.getWinner()
            == CANDIDATES[0]  # name_list[
            # vote_count_list.index(max(vote_count_list), 0, len(vote_count_list))
            # ]
        )
