#### ShareLaTex Templates
**These LaTex templates was from [sharelatex.com](https://www.sharelatex.com), organized by category/template name including its .zip file and preview image.**
*[download.py](./download.py)* shows how to download templates. unzip it, and then compile. 
Download Link will be update soon!
**Enjoying your work!**

#### How to start your own sharelatex
* Install docker
  see [docker-install](https://github.com/docker/docker-install).
* Download sharelatex offical image
```shell
docker pull sharelatex/sharelatex
```
* Install docker-compose
  see [docker-compose-release](https://github.com/docker/compose/releases), do as below:
```shell
curl -L https://github.com/docker/compose/releases/download/1.17.0-rc1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

* docker-compose
  download [docker-compose.yml](https://github.com/sharelatex/sharelatex/blob/master/docker-compose.yml)

  ```
  sudo docker-compose up
  ```

* Enjoy yourself, visit http://server_ip

  ​
