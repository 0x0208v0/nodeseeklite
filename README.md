# nodeseeklite

## 一句话介绍：

MJJ最热闹的论坛：NodeSeek “Lite” 版它来啦～

`（欢迎各位小伙伴参与 nodeseeklite 开源项目，此处眼神暗示场内场外的MJJ们）`

## TODO（接下来要做的）

1. （重要紧急）加入按用户屏蔽相关功能
1. （重要紧急）加入按关键字屏蔽相关功能

## 页面展示

![](https://img.erpweb.eu.org/imgs/2024/05/7010af3cffec3af6.png)

## 如何本地启动？

首先，确保本机已经安装 docker 和 docker-compose 软件

如果不会安装，这里推荐推荐一个NS论坛相关帖子，看完了评论区，包会！

    https://www.nodeseek.com/post-110630-1

小技巧：可在命令行输入下面的两条命令，来确认 docker 和 docker-compose 是否已经安装成功）

如果已安装，则会输出版本信息；否则会报错  
`（诶嘿嘿，又学到一招～`

    docker -v

    docker-compose -v

确认已安装过 docker 和 docker-compose 后，可在本机启动服务  
（在VPS上也行，只不过目前没文档。。。）

最后，按照下面的步骤，依次执行命令：

### 1. 拉 Docker 镜像

    docker-compose pull 

### 2. 构建 Docker 镜像（主要是 nodeseeklite-webserver和 nodeseeklite-task）

    docker-compose build

### 3. 干掉旧的 Docker 容器，启动新的 Docker 容器

    docker-compose down && docker-compose up -d

## 本机部署后，如何浏览器访问？

### nodeseeklite Web 页面：

默认地址：http://localhost:15100/

### nodeseeklite API ：

浏览器访问：http://localhost:15100/api

或者

命令行输入 `curl http://localhost:15100/api `
