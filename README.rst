星际争霸2 裁判合约
===================


:Date: 01/06 2017

.. contents::

介绍
-----

构建在 `Ethereum BlockChain` 上面的裁判 智能合约。

该合约可以对 `星际争霸2` 这款游戏的比赛结果进行分析，并给出胜负结果。

开发
------

*相关依赖*:

.. code:: bash
	
	# brew install geth # 选择安装 geth 或 parity
	brew install parity --master
	brew install solidity

	npm install -g ethereumjs-testrpc
	npm install -g solc web3 dapple
	npm install -g webpack
	# 克隆代码
	git clone https://github.com/LuoZijun/solidity-sc2-replay-reader
	cd solidity-sc2-replay-reader
	npm install -d


安装完上述工具包，你的系统应该就有以下命令可以使用:


*	geth
*	parity
*	solc
*	testrpc
*	solcjs
*	webpack


简单介绍下这几个命令的作用:

`parity` (基于 Rust 语言) 和 `geth` (基于 Golang 语言) 是以太坊的客户端，你可以按照喜好选择安装一个(推荐 `parity` )。


`testrpc` 是一个以太坊 `JsonRPC Service` 模拟器，可以用来在开发时，对代码进行测试。
以太坊客户端 `parity` 和 `geth` 都提供了 完整的 `JsonRPC Service` 。


`solc` 和 `solcjs` 是 以太坊 合约语言 `solidity` 的编译器，其中 `solc` 采用 `C++` 语言编写，
`solcjs` 采用 `Emscripten <https://github.com/kripken/emscripten>`_ 这个工具 对 `C++` 代码翻译成 `JavaScript` 代码，
所以，如果你在意性能，请直接使用 `C++` 版本的 `solidity` 编译器。


`webpack` 这个是 `NodeJS` 的打包工具，相信不需要多介绍了 :))


*编译合约*:

.. code:: bash

	cd solidity-sc2-replay-reader/
	parity --chain dev # geth --dev console
	# 使用辅助脚本来编译，或者直接使用 `solc target.solc || solcjs target.solc` 命令来编译 
	python solidity.py
	# 打包 JS 文件
	webpack -w
	# 打开测试文件
	open index.html


参考
------

*Starcraft II Replay Protocol :*

*	`Blizzard s2protocol <https://github.com/Blizzard/s2protocol>`_
*	`sc2reader <https://github.com/GraylinKim/sc2reader>`_

**Ethereum:**

*	`Solidity <https://github.com/ethereum/solidity>`_
*	`Solidity Browserbased compiler <https://ethereum.github.io/browser-solidity>`_
*	`Solidity repl <https://github.com/raineorshine/solidity-repl>`_

*	`Solidity Document <http://solidity.readthedocs.io/>`_
*	`Solidity Features <https://github.com/ethereum/wiki/wiki/Solidity-Features>`_

*Solidity Lnaguage:*

*	`Solidity Grammar <https://github.com/ethereum/solidity/blob/develop/docs/grammar.txt>`_
*	`Solidity Units and Globally Available Variables <http://solidity.readthedocs.io/en/develop/units-and-global-variables.html>`_ , 单位以及全局变量

*Solidity Package:*

*	`Solidity Dapple <https://github.com/nexusdev/dapple>`_ , Package and deployment manager for Solidity
*	`Solidity Solidity standard library <https://github.com/ethereum/solidity/tree/develop/std>`_

*Web3.js :*

*	`Web3 JavaScript Ðapp API <https://github.com/ethereum/wiki/wiki/JavaScript-API>`_