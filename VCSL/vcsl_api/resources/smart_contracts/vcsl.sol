// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract StorageContract {
    address private owner;
    string private storedUrl;
    mapping(string => Data) public dataDictionary;

    struct Data {
        string ipns;
        uint256 creationTS;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function setUrl(string memory _url) external onlyOwner {
        storedUrl = _url;
    }

    function addData(string memory _id, string memory _ipns) external onlyOwner {
        require(bytes(_id).length > 0, "ID cannot be empty");
        require(bytes(dataDictionary[_id].ipns).length == 0, "ID already exists");

        dataDictionary[_id] = Data({
            ipns: _ipns,
            creationTS: block.timestamp
        });
    }

    function getData(string memory _id) external view returns (string memory ipns, uint256 creationTS) {
        require(bytes(dataDictionary[_id].ipns).length > 0, "ID not found");
        
        Data storage data = dataDictionary[_id];
        return (data.ipns, data.creationTS);
    }

    function getUrl() external view returns (string memory) {
        return storedUrl;
    }
}
