
use std::fs::File;
use std::io::Read;
use std::ptr::copy_nonoverlapping;

// Result:
// 11011010100010101000001001101
// 1101101010001

fn sp(){
    let bytes: [u8; 4] = [77, 80, 81, 27];
    let buf_a: [u8; 2] = [77, 80];
    let buf_b: [u8; 2] = [81, 27];

    let mut num_a: u32 = 0;
    let mut num_b: u32 = 0;
    unsafe {
        copy_nonoverlapping(buf_a.as_ptr(), &mut num_a as *mut u32 as *mut u8, 2);
        copy_nonoverlapping(buf_b.as_ptr(), &mut num_b as *mut u32 as *mut u8, 2);
    }
    println!("SP Bits: {:16b}  {:16b}", num_a.to_le(), num_b.to_le());
}
fn main() {
    sp();

    let mut f: File = File::open("test.replay").unwrap();
    let mut buf = [0u8; 4];
    let size = f.read(&mut buf).unwrap();

    let mut data: u32 = 0;
    unsafe {
        copy_nonoverlapping(buf.as_ptr(), &mut data as *mut u32 as *mut u8, 4)
    }
    let bits = data.to_le();
    let _string = std::str::from_utf8(&buf).unwrap().to_owned();

    println!("String: {:?} ", _string );
    println!("Bytes: {:?}   Size: {:?}", buf, size);
    println!("U32: {:?}   Bits: {:b}", bits, bits );
}