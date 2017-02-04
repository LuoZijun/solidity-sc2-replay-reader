'use strict';

// /Users/luozijun/Library/Application Support/io.parity.ethereum
const Web3 = require("web3");
const contracts = require("../build/contract.json");

const env  = {rpcURL: "http://127.0.0.1:8545"};
const web3 = new Web3(new Web3.providers.HttpProvider(env.rpcURL));

// Dev Chain: 0x00c512b12fed6f51f7b9b60d198de9d5ee0abcd9
const account = web3.eth.accounts[0];

function main(){
    // Object.keys(contracts).forEach(function (key, i){
    //     var contract   = web3.eth.contract(contracts[key]["interface"]);
    //     contract.code  = contracts[key]["code"];
    //     contracts[key] = contract;
    //     // contract.new(initializer, callback);
    // });
    const helloworld = contracts.HelloWorld;
    const helloworldContract = web3.eth.contract(helloworld.interface);
    
    helloworldContract.new({
        from : account,
        data : helloworld.code,
        gas  : '4700000',
    }, function(e, contract){
        if(!e) {
            if(!contract.address) {
                var msg = [
                    "Contract transaction send: TransactionHash: ",
                    contract.transactionHash.toString(),
                    " waiting to be mined..."
                ].join("");
                console.log(msg);
            } else {
                console.info("Deploy Success ...");
                console.info("Contract Address: " + contract.address);
                var result = contract.add.call(3, 5);
                console.log(result.toNumber());
                console.log(contract.hi.call());
                var r = contract.test_bytes.call("我");
                console.log(r);
            }
        } else {
            console.error("JSON RPC Callback error.");
            console.debug(e);
        }
    });
}

function demo_test(){
    // let tokenSource = fs.readFileSync("./token.sol", "utf-8");
    var tokenSource = "pragma solidity ^0.4.6;"
                    + "contract Token {"
                    + "    address issuer;"
                    + "    mapping (address => uint) balances;"
                    + "    event Issue(address account, uint amount);"
                    + "    event Transfer(address from, address to, uint amount);"
                    + "    function Token() {"
                    + "        issuer = msg.sender;"
                    + "    }"
                    + "    function issue(address account, uint amount) {"
                    + "        if (msg.sender != issuer) throw;"
                    + "        balances[account] += amount;"
                    + "    }"
                    + "    function transfer(address to, uint amount) {"
                    + "        if (balances[msg.sender] < amount) throw;"
                    + "        balances[msg.sender] -= amount;"
                    + "        balances[to] += amount;"
                    + "        Transfer(msg.sender, to, amount);"
                    + "    }"
                    + "    function getBalance(address account) constant returns (uint) {"
                    + "        return balances[account];"
                    + "    }"
                    + "}";

    var tokenCompiled = { Token: web3.eth.compile.solidity(tokenSource) };

    var contract = web3.eth.contract(tokenCompiled.Token.info.abiDefinition);
    var initializer = {from: web3.eth.accounts[0], data: tokenCompiled.Token.code, gas: 300000};

    // Deploy new contract
    // contract.new(initializer, function(e, contract){
    //     if(!e) {
    //         if(!contract.address) {
    //             console.log("Contract transaction send: TransactionHash: " 
    //                 + contract.transactionHash 
    //                 + " waiting to be mined...");
    //         } else {
    //             // console.log("Contract mined!");
    //             console.info("Deploy Success ...");
    //             // 0x5637c67b02e6ece0d8ede2f5f1390c99c57b2ee7
    //             console.info("Contract Address: ", contract.address);
    //             // console.log(contract);
    //             let balances = contract.getBalance.call(web3.eth.accounts[0]);
    //             console.log("Balances: ", balances.toNumber());
    //         }
    //     }
    // });

    // Instantiate by address
    var myContractInstance = contract.at("0x5637c67b02e6ece0d8ede2f5f1390c99c57b2ee7");
    var result = myContractInstance.getBalance(web3.eth.accounts[0]);
    console.log(result.toNumber());
}

main();
// demo_test();


