use crate::connection::Connection;
use chrono::Utc;
use std::{error::Error, time::Duration};
use tokio::time;

mod connection;
mod feed;
mod parse;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let connection = Connection::new()?;
    let feeds = parse::parse_feeds()?;
    let mut last_sync = Utc::now();

    loop {
        if let Err(e) = parse::sync_feeds(&connection, &feeds, &last_sync).await {
            eprintln!("{}", e);
        }

        last_sync = Utc::now();
        time::sleep(Duration::from_hours(1)).await;
    }
}
