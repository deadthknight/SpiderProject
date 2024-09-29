![截屏2024-09-01 17.57.54](/Users/vickyyang/Desktop/截屏2024-09-01 17.57.54.png)

<img alt="截屏2024-09-01 17.58.13" src="/Users/vickyyang/Desktop/截屏2024-09-01 17.58.13.png"/>

搜索不到数据，说明数据是加密的，search decrypt![截屏2024-09-01 17.58.47](/Users/vickyyang/Desktop/截屏2024-09-01 17.58.47.png)

![截屏2024-09-01 17.59.04](/Users/vickyyang/Desktop/截屏2024-09-01 17.59.04.png)

打断点，发现是AES CBC

![截屏2024-09-01 17.59.30](/Users/vickyyang/Desktop/截屏2024-09-01 17.59.30.png)

f是密钥 m是iv，后面f重新被复制，所有第一幅图第一个请求没有响应数据。![截屏2024-09-01 21.14.43](/Users/vickyyang/Desktop/截屏2024-09-01 21.14.43.png)