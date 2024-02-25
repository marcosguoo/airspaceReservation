// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AirspaceAuction {
    address public owner;
    address public highestBidder;
    uint256 public highestBid;

    mapping(address => uint256) public bids;

    event BidPlaced(address bidder, uint256 amount);
    event AuctionEnded(address winner, uint256 amount);
    event EmergencyClear(address clearer, uint256 amount);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function placeBid() external payable {
        require(msg.value > highestBid, "Bid must be higher than the current highest bid");

        if (highestBidder != address(0)) {
            // Refund the previous highest bidder
            payable(highestBidder).transfer(highestBid);
        }

        highestBidder = msg.sender;
        highestBid = msg.value;

        bids[msg.sender] += msg.value;

        emit BidPlaced(msg.sender, msg.value);
    }

    function endAuction() external onlyOwner {
        require(highestBidder != address(0), "Auction has not ended yet");

        // Transfer the funds to the owner
        payable(owner).transfer(highestBid);

        emit AuctionEnded(highestBidder, highestBid);

        // Reset auction state
        highestBidder = address(0);
        highestBid = 0;
    }

    function emergencyClear() external onlyOwner {
        require(highestBidder != address(0), "No bid to clear");

        // Refund the highest bidder in case of emergency
        payable(highestBidder).transfer(highestBid);

        emit EmergencyClear(msg.sender, highestBid);

        // Reset auction state
        highestBidder = address(0);
        highestBid = 0;
    }
}
