Contracts in Solidity are similar to classes in object-oriented languages. Each contract can contain declarations of State Variables, Functions, Function Modifiers, Events, Struct Types and Enum Types. Furthermore, contracts can inherit from other contracts.

There are also special kinds of contracts called libraries and interfaces.

The section about contracts contains more details than this section, which serves to provide a quick overview.

State Variables
State variables are variables whose values are permanently stored in contract storage.

pragma solidity >=0.4.0 <0.6.0;

contract SimpleStorage {
    uint storedData; // State variable
    // ...
}
See the Types section for valid state variable types and Visibility and Getters for possible choices for visibility.

Functions
Functions are the executable units of code within a contract.

pragma solidity >=0.4.0 <0.6.0;

contract SimpleAuction {
    function bid() public payable { // Function
        // ...
    }
}
Function Calls can happen internally or externally and have different levels of visibility towards other contracts. Functions accept parameters and return variables to pass parameters and values between them.

Function Modifiers
Function modifiers can be used to amend the semantics of functions in a declarative way (see Function Modifiers in the contracts section).

pragma solidity >=0.4.22 <0.6.0;

contract Purchase {
    address public seller;

    modifier onlySeller() { // Modifier
        require(
            msg.sender == seller,
            "Only seller can call this."
        );
        _;
    }

    function abort() public view onlySeller { // Modifier usage
        // ...
    }
}
Events
Events are convenience interfaces with the EVM logging facilities.

pragma solidity >=0.4.21 <0.6.0;

contract SimpleAuction {
    event HighestBidIncreased(address bidder, uint amount); // Event

    function bid() public payable {
        // ...
        emit HighestBidIncreased(msg.sender, msg.value); // Triggering event
    }
}
See Events in contracts section for information on how events are declared and can be used from within a dapp.

Struct Types
Structs are custom defined types that can group several variables (see Structs in types section).

pragma solidity >=0.4.0 <0.6.0;

contract Ballot {
    struct Voter { // Struct
        uint weight;
        bool voted;
        address delegate;
        uint vote;
    }
}
Enum Types
Enums can be used to create custom types with a finite set of ‘constant values’ (see Enums in types section).

pragma solidity >=0.4.0 <0.6.0;

contract Purchase {
    enum State { Created, Locked, Inactive } // Enum
}
