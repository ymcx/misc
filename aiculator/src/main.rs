use handler::{parse, query};
use std::env::args;

mod handler;

#[tokio::main]
async fn main() {
    let args = parse(args().collect());
    let response = query(args, "phi3:mini").await;

    println!("{}", response);
}
