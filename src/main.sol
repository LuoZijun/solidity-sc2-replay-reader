pragma solidity ^0.4.8;

import {Math} from './math.sol';
import {Mpq} from './mpq.sol';
import {Replay} from './sc2/replay.sol';

/**

// JavaScript Number To Bits

function number_to_binary(n, b){
    var s = [], m;
    while (n !== 0){
        m = n % b;
        n = Math.floor(n / b);
        s.push(m.toString());
    }
    s.push("0b");
    s.reverse();
    return s.join("");
}
**/

library HelloWorld {
    function hi() returns(string) {
        return "Hello, 世界！";
    }
}

contract BytesReader {
    uint[] s;
    // storage memory
    function byte_to_bits(uint n) returns (uint[]) {
        uint b = 2;
        uint idx = 0;
        while ( n != 0 ) {
            uint m = n % b;
            n = n/b;
            s.push(m);
        }
        return s;
    }
}


