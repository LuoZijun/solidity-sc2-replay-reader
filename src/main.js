
const Web3 = require("web3");
const contracts = require("../build/contract.json");

const env  = {rpcURL: "http://localhost:8545"};
const web3 = new Web3(new Web3.providers.HttpProvider(env.rpcURL));

const callback = function(e, contract){
    if(!e) {
      	if(!contract.address) {
      		let message = [
      			"Contract transaction send: TransactionHash: ",
      			contract.transactionHash,
      			" waiting to be mined..."
      		].join("");
        	console.log(message);
      	} else {
        	console.log("Contract mined!");
        	console.log(contract);
      	}
    }
};


Object.keys(contracts).forEach(function (key, i){
	let initializer = {
		from: web3.eth.accounts[0],
		data: contracts[key]["code"],
		gas : 300000
	};
	
	let contract = web3.eth.contract(contracts[key]["interface"]);
	contract.code = contracts[key]["code"];
	contracts[key] = contract;
	// contract.new(initializer, callback);
});


console.log(contracts);

