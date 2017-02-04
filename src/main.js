
const Web3 = require("web3");
const contracts = require("../build/contract.json");

const env  = {rpcURL: "http://localhost:8545"};
const web3 = new Web3(new Web3.providers.HttpProvider(env.rpcURL));

const Address = web3.eth.accounts[0];

Object.keys(contracts).forEach(function (key, i){
    var contract   = web3.eth.contract(contracts[key]["interface"]);
    contract.code  = contracts[key]["code"];
    contracts[key] = contract;
    // contract.new(initializer, callback);
});


const helloworld = contracts.HelloWorld;
const initializer = {
    from: web3.eth.accounts[0],
    data: contracts.HelloWorld["code"],
    gas : '4000000'
};

helloworld.new(initializer, function(e, contract){
    if(!e) {
        if(!contract.address) {
            var msg = [
                "Contract transaction send: TransactionHash: ",
                contract.transactionHash.toString(),
                " waiting to be mined..."
            ].join("");
            console.log(msg);
        } else {
            console.log("Contract mined!");
            console.log(contract);
            let result = contract.hi.call();
            console.log(result);
        }
    }
});


