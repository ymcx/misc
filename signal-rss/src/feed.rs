use atom_syndication::{Entry, Feed};
use chrono::{DateTime, FixedOffset};
use quick_xml::{Reader, events::Event};
use rss::{Channel, Item};
use std::error::Error;

pub struct Stream(pub Vec<Article>);

pub enum Article {
    Atom(Entry),
    Rss(Item),
}

impl Stream {
    fn is_atom(contents: &[u8]) -> Result<bool, Box<dyn Error>> {
        let contents = str::from_utf8(contents)?;
        let mut reader = Reader::from_str(contents);

        loop {
            return match reader.read_event() {
                Ok(Event::Start(i)) => Ok(i.name().as_ref() == b"feed"),
                Ok(Event::Eof) => Err("Invalid feed".into()),
                _ => continue,
            };
        }
    }

    pub async fn new(url: &str) -> Result<Self, Box<dyn Error>> {
        let response = reqwest::get(url).await?;
        let bytes = response.bytes().await?;
        let slice = bytes.as_ref();
        let articles = if Self::is_atom(slice)? {
            Feed::read_from(slice)?
                .entries
                .into_iter()
                .map(Article::Atom)
                .collect()
        } else {
            Channel::read_from(slice)?
                .items
                .into_iter()
                .map(Article::Rss)
                .collect()
        };

        Ok(Self(articles))
    }
}

impl Article {
    pub fn title(&self) -> Result<&str, Box<dyn Error>> {
        let title = match self {
            Article::Atom(i) => i.title().as_str(),
            Article::Rss(i) => i.title().ok_or("Invalid title")?,
        };

        Ok(title)
    }

    pub fn url(&self) -> Result<&str, Box<dyn Error>> {
        let url = match self {
            Article::Atom(i) => i.links().first().ok_or("Invalid URL")?.href.as_str(),
            Article::Rss(i) => i.link().ok_or("Invalid URL")?,
        };

        Ok(url)
    }

    pub fn time(&self) -> Result<DateTime<FixedOffset>, Box<dyn Error>> {
        let time = match self {
            Article::Atom(i) => i.published.ok_or("Invalid time")?,
            Article::Rss(i) => {
                let i = i.pub_date.as_ref().ok_or("Invalid time")?;
                DateTime::parse_from_rfc2822(i)?
            }
        };

        Ok(time)
    }
}
