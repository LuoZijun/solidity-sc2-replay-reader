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

contract BytesReader {
    
    function byte_to_bits(byte b) returns (uint1 [] ) {
        
    }
    function BytesReader (){

    }
}