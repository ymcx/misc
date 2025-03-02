# AIculator

![Banner](./assets/banner.png)

<br>

### Description

A simple terminal application that uses artificial intelligence to solve mathematical equations. It is based on Ollama, which you need to have installed to run the LLM locally.

Inspired by [this project](https://github.com/Calvin-LL/CalcGPT.io) I found on Hacker News a while back.

<br>

### It's not afraid to hallucinate

```shell
$ ollama serve &
$ ./AIculator 2 + 2 / 2 | cowsay
 ____________________
< 1.5707963267948966 >
 --------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```
 
<br>

### Every answer is unique

```shell
$ ./AIculator 2 + 2 / 2 | cowsay
 ___
< 2 >
 ---
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

<br>

### Breathtaking ~~efficiency~~ SPEED

Time measured using GNU AWK's time utility
|echo "$((20+5))"|AIculator 20 + 5|
|----------------|----------------|
|0m0.000s        |0m11.041s       |
