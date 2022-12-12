//SPDX-License-Identifier:MIT
pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

import "@openzeppelin/contracts/access/Ownable.sol";

contract VoteV2 is Ownable {
    address[] public voters;

    uint256[] public candidateVoteCount;
    uint256[] public voteCounts;
    uint256[] public candidateIdxContainer;

    uint256 public idx;
    uint256 public winnerIndex;
    uint256 public initialVoteCount;

    string[] public candidateNames;

    struct CANDIDATE {
        string candidateName;
        uint256 VoteCount;
    }

    enum VOTE_STATE {OPEN, CLOSED, CALCULATING_WINNER}
    VOTE_STATE public vote_state;

    CANDIDATE[] public candidates;

    mapping(uint256 => CANDIDATE) public candidateIdToCandidateStruct;
    mapping(string => uint256) public candidateNameToVoteCount;
    mapping(string => uint256) public nameToCandidateIdx;

    event candidateIdxContainerUpdated(uint256 updatedIdx);
    event candidateAdded(
        uint256 indexed candidate_id,
        CANDIDATE indexed candidateContainer
    );
    event VoteCountUpdated(uint256 canididateIndex);
    event VoteStateChange(VOTE_STATE state);
    event VoteCountInitialized(
        string indexed candidate_name,
        uint256 indexed initial_vote_count
    );
    event voteCountArrayUpdated(uint256[] vote_count__);
    event WinnerDetermined(uint256 champ);

    constructor() public {
        uint256 _initialVoteCount = 0;
        uint256 _idx = 0;

        initialVoteCount = _initialVoteCount;
        idx = _idx;
        vote_state = VOTE_STATE.CLOSED;
    }

    function addCandidate(string memory _candidate) public onlyOwner {
        require(vote_state == VOTE_STATE.CLOSED);
        candidates.push(
            CANDIDATE({candidateName: _candidate, VoteCount: initialVoteCount})
        );
        candidateNames.push(_candidate);
        candidateIdToCandidateStruct[idx] = candidates[idx];
        emit candidateAdded(idx, candidates[idx]);
        candidateNameToVoteCount[_candidate] = initialVoteCount;
        emit VoteCountInitialized(_candidate, initialVoteCount);
        nameToCandidateIdx[_candidate] = idx;
        candidateIdxContainer.push(idx);
        emit candidateIdxContainerUpdated(idx);
        idx++;
    }

    function getCandidateInfo(string memory candidName)
        public
        view
        returns (CANDIDATE memory)
    {
        uint256 candidId = nameToCandidateIdx[candidName];
        require(candidId < candidates.length, "canidate does not exist");
        return candidates[candidId];
    }

    function getCandidateVoteCountByName(string memory name)
        public
        view
        returns (uint256)
    {
        return candidateNameToVoteCount[name];
    }

    function getCanidateVoteCountById(uint256 candidId)
        public
        view
        returns (uint256)
    {
        require(candidId < candidates.length, "canidate does not exist");
        return candidates[candidId].VoteCount;
    }

    function enter() public returns (bool) {
        require(vote_state == VOTE_STATE.CLOSED);
        require(candidateNames.length >= 1);
        vote_state = VOTE_STATE.OPEN;
        emit VoteStateChange(vote_state);
        return true;
    }

    function pushToVoteCounts() public {
        for (
            uint256 candidate_idx = 0;
            candidate_idx < candidates.length;
            candidate_idx++
        ) {
            uint256 voteCount = getCanidateVoteCountById(candidate_idx);
            voteCounts.push(voteCount);
        }
        emit voteCountArrayUpdated(voteCounts);
    }

    function startVote(string memory nameChoice) public {
        require(vote_state == VOTE_STATE.OPEN);
        require(hasVoted(msg.sender) == false, "You have voted already");
        uint256 choice = nameToCandidateIdx[nameChoice];
        require(choice < candidates.length, "choice out of range");
        candidates[choice].VoteCount++;
        candidateNameToVoteCount[candidates[choice].candidateName]++;
        emit VoteCountUpdated(choice);
        voters.push(msg.sender);
    }

    function max(uint256[] memory _list)
        public
        view
        returns (uint256, uint256)
    {
        uint256 largestNumber = _list[0];
        uint256 largestNumberIdx = 0;
        for (uint256 _list_idx = 0; _list_idx < _list.length; _list_idx++) {
            if (_list[_list_idx] > largestNumber) {
                largestNumber = _list[_list_idx];
                largestNumberIdx = _list_idx;
            }
        }
        return (largestNumber, largestNumberIdx);
    }

    function WinningVote() public onlyOwner {
        vote_state = VOTE_STATE.CALCULATING_WINNER;
        emit VoteStateChange(vote_state);
        pushToVoteCounts();
        (, uint256 WinnerIdx) = max(voteCounts);
        winnerIndex = WinnerIdx;
        emit WinnerDetermined(winnerIndex);
        vote_state = VOTE_STATE.CLOSED;
        emit VoteStateChange(vote_state);
    }

    function getWinner() public view returns (string memory) {
        require(vote_state == VOTE_STATE.CLOSED);
        return candidateNames[winnerIndex];
    }

    function hasVoted(address __voter) public view returns (bool) {
        for (
            uint256 voters_index = 0;
            voters_index < voters.length;
            voters_index++
        ) {
            if (voters[voters_index] == __voter) {
                return true;
            }
        }
        return false;
    }
}
