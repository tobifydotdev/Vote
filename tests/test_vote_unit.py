from brownie import network, accounts, VoteV2, exceptions
import pytest

# from sources.scripts.helpful_scripts import CANDIDATES

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local", "mainnet-fork-dev"]
candidates = ["tobi", "tobiade", "ayo"]


def test_can_add_candidate():
    # Assign/Arrange

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        account = accounts[0]
    else:
        pytest.skip()
    # Act
    vote_v2 = VoteV2.deploy({"from": account})
    for i in range(len(candidates)):
        tx = vote_v2.addCandidate(candidates[i], {"from": account})
        tx.wait(1)

    # Assert
    assert vote_v2.getCandidateInfo(candidates[0]) == [candidates[0], 0]
    assert vote_v2.getCandidateInfo(candidates[1]) == [candidates[1], 0]
    assert vote_v2.getCandidateInfo(candidates[2]) == [candidates[2], 0]

    # assert vote_v2.getCandidateInfo("ayo") == [candidates[2], 0]


def test_can_get_max_number():
    # Assign/Arrange
    numbers = [6, 8, 10, 100, 55, 78]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        account = accounts[0]
    else:
        pytest.skip()
    # Act
    vote_v2 = VoteV2.deploy({"from": account})
    # x = vote_v2.max(numbers, {"from": account})

    # tx.wait(1)
    # Assert_
    assert vote_v2.max(numbers) == [max(numbers), 3]


def test_can_get_candidate_votecount_by_name():
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        account = accounts[0]
    else:
        pytest.skip()
    # Act
    vote_v2 = VoteV2.deploy({"from": account})
    tx_1 = vote_v2.addCandidate(candidates[0], {"from": account})
    tx_1.wait(1)
    tx_e = vote_v2.enter({"from": account})
    tx_e.wait(1)
    tx_2 = vote_v2.startVote(candidates[0], {"from": account})
    tx_2.wait(1)
    # Assert
    assert vote_v2.getCandidateVoteCountByName(candidates[0]) == 1


def test_can_enter_vote():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        account = accounts[0]
    else:
        pytest.skip()
    # Act
    vote_v2 = VoteV2.deploy({"from": account})
    tx = vote_v2.addCandidate(candidates[0], {"from": account})
    tx.wait(1)
    tx_2 = vote_v2.enter({"from": account})
    tx_2.wait(1)
    # Assert
    assert vote_v2.vote_state() == 0


def test_cant_vote_unless_entered():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        account = accounts[0]
    else:
        pytest.skip()
    # Act
    vote_v2 = VoteV2.deploy({"from": account})
    vote_v2.addCandidate(candidates[0], {"from": account})
    with pytest.raises(exceptions.VirtualMachineError):
        vote_v2.startVote(candidates[0], {"from": account})


def test_get_candidate_vote_count_by_id():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        account = accounts[0]
    else:
        pytest.skip()
    # Act
    vote_v2 = VoteV2.deploy({"from": account})
    vote_v2.addCandidate(candidates[0], {"from": account})
    vote_v2.enter({"from": account})
    vote_v2.startVote(candidates[0], {"from": account})
    assert vote_v2.getCanidateVoteCountById(0) == 1


def test_can_get_candidate_info():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        account = accounts[0]
    else:
        pytest.skip()
    # Act
    vote_v2 = VoteV2.deploy({"from": account})
    vote_v2.addCandidate(candidates[0], {"from": account})
    vote_v2.enter({"from": account})
    assert vote_v2.getCandidateInfo(candidates[0]) == [candidates[0], 0]
    vote_v2.startVote(candidates[0], {"from": account})
    assert vote_v2.getCandidateInfo(candidates[0]) == [candidates[0], 1]


def test_can_get_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        account = accounts[0]
        account_2 = accounts[1]
        account_3 = accounts[2]
    else:
        pytest.skip()
    # Act
    vote_v2 = VoteV2.deploy({"from": account})
    vote_v2.addCandidate(candidates[0], {"from": account})
    vote_v2.addCandidate(candidates[1], {"from": account})
    vote_v2.enter({"from": account})
    vote_v2.startVote(candidates[0], {"from": account})
    vote_v2.startVote(candidates[0], {"from": account_2})
    vote_v2.startVote(candidates[1], {"from": account_3})
    vote_v2.getWinningVote({"from": account})
    assert vote_v2.getWinner() != candidates[1]


def test_check_if_voted_already():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        account = accounts[0]
    else:
        pytest.skip()
    # Act
    vote_v2 = VoteV2.deploy({"from": account})
    vote_v2.addCandidate(candidates[0], {"from": account})
    vote_v2.enter({"from": account})
    # assert vote_v2.getCandidateInfo(0) == [candidates[0], 0]
    vote_v2.startVote(candidates[0], {"from": account})
    assert vote_v2.hasVoted(account) == True
    with pytest.raises(exceptions.VirtualMachineError):
        vote_v2.startVote(candidates[1], {"from": account})


def test_idx_container_contains_all_idx():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        account = accounts[0]
    else:
        pytest.skip()
    # Act
    vote_v2 = VoteV2.deploy({"from": account})
    for i in range(len(candidates)):
        tx = vote_v2.addCandidate(candidates[i], {"from": account})
        tx.wait(1)
    for i in range(len(candidates)):
        print(vote_v2.idxContainerTest(i))
        assert vote_v2.idxContainerTest(i) == i
