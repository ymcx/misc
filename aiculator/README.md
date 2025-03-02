# AIculator

![Banner](./assets/banner.png)

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
