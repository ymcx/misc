use crate::{connection::Connection, feed::Stream};
use base64::{Engine, prelude::BASE64_STANDARD};
use chrono::{DateTime, Utc};
use std::{env, error::Error, fs};

pub async fn sync_feeds(
    connection: &Connection,
    feeds: &Vec<(Vec<u8>, String)>,
    last_sync: &DateTime<Utc>,
) -> Result<(), Box<dyn Error>> {
    for feed in feeds {
        let feed_group = &feed.0;
        let feed_url = &feed.1;
        let stream = Stream::new(feed_url).await?;

        for article in stream.0 {
            if article.time()? < *last_sync {
                continue;
            }

            let message = format!("{}\n{}", article.title()?, article.url()?);
            connection.send(&message, feed_group)?;
        }
    }

    Ok(())
}

fn parse_feed(feed: &str) -> Result<(Vec<u8>, String), Box<dyn Error>> {
    let (group, url) = feed.split_once(' ').ok_or("Invalid feed")?;
    let group = BASE64_STANDARD.decode(group)?;
    let url = url.to_string();

    Ok((group, url))
}

pub fn parse_feeds() -> Result<Vec<(Vec<u8>, String)>, Box<dyn Error>> {
    let arguments: Vec<String> = env::args().collect();
    let path = arguments.get(1).ok_or("No file provided")?;
    let contents = fs::read_to_string(path)?;
    let feeds = contents.lines().map(|feed| parse_feed(feed)).collect();

    feeds
}
