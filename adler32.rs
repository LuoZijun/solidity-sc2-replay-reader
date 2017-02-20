
// Copy from https://golang.org/src/hash/adler32/adler32.go

// BASE is the largest prime that is less than 65536.
const BASE: usize  = 65521;
// nmax is the largest n such that
// 255 * n * (n+1) / 2 + (n+1) * (BASE-1) <= 2^32-1.
// It is mentioned in RFC 1950 (search for "5552").
const NMAX: usize = 5552;

struct Adler32 (u32);

struct Bytes {
    vec: Vec<u8>
}

impl Adler32 {
    fn new () -> Self {
        Adler32(1)
    }
    fn check_sum(data: &mut Vec<u8>) -> u32 {
        let adler32 = Adler32::new();
        adler32.update(data)
    }
    fn update(&self, p: &mut Vec<u8>) -> u32{
        let mut s1 = 1;
        let mut s2 = 0;
        
        let mut p_s = 0;
        let mut p_e = p.len();
        
        loop {
            let p_length = p.len();
            if p_length == 0 {
                break;
            }

            let mut q: Vec<u8> = Vec::new();

            if p_length >= 4 {
                let mut _p = &p[0..std::cmp::min(NMAX, p_length)].to_owned();
                let mut _q = &p[std::cmp::min(NMAX, p_length)..].to_owned();
                p.clear();
                p.append(&mut _p.to_vec());
                
                q.clear();
                q.append(&mut _q.to_vec());
            }
            loop {
                let p_length = p.len();
                if p_length < 4 {
                    break;
                }
                s1 += p[0] as u32;
                s2 += s1;

                s1 += p[1] as u32;
                s2 += s1;

                s1 += p[2] as u32;
                s2 += s1;

                s1 += p[3] as u32;
                s2 += s1;
                let mut _p = &p[std::cmp::min(4, p_length)..].to_owned();
                p.clear();
                p.append(&mut _p.to_vec());
            }

            for x in p.iter() {
                s1 += *x as u32;
                s2 += s1;
            }

            s1 %= BASE as u32;
            s2 %= BASE as u32;

            p.clear();
            p.append(&mut q);
        }

        (s2 << 16 | s1) as u32
    }

    fn sum32(&self) -> u32 {
        self.0.clone()
    }

    fn sum(&self, _in: &mut Vec<u8>) {
        let s: u32 = self.0.clone();
        _in.push( (s>>24) as u8 );
        _in.push( (s>>16) as u8 );
        _in.push( (s>> 8) as u8 );
        _in.push( s as u8 );
    }
}


fn main() {
    let mut s = String::from("hello, 世界！");
    let mut bytes: Vec<u8> = s.as_bytes().to_owned();
    println!("{} {:?}", s, bytes);
    let num = Adler32::check_sum(&mut bytes);
    
    println!("String: {:?}\nBytes: {:?}\nNum: {:?}\tHex: {:#x}", s, bytes, num, num);
}