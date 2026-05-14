# Selfref

A self-referential image generator. Inspired by [this video](https://www.youtube.com/watch?v=nsj3gTGh9K0).

# Installition

```
cargo build --release
```

# Usage

```
selfref generate \
  --font [FONT] \
  --fg-color [R G B A] \
  --bg-color [R G B A] \
  --font-size [SIZE]
selfref verify \
  --fg-color [R G B A] \
  [IMAGE] \
```

### Example

```
selfref generate \
  --font /usr/share/fonts/adwaita-mono-fonts/AdwaitaMono-Regular.ttf \
  --fg-color 255 255 255 255 \
  --bg-color 0 0 0 255 \
  --font-size 14
selfref verify \
  --fg-color 255 255 255 255 \
  ./images/680.png
> 680
```

![Example](./images/680.png)
