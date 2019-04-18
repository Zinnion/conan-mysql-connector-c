## Package Status

mysql 8.x	

https://github.com/linux-on-ibm-z/docs/wiki/Building-MySQL-8.x



### X DevAPI User Guide

https://downloads.mysql.com/docs/x-devapi-userguide-en.pdf


### Pkg creation `libstdc++11` needs to be specified if you dont have it as default
`conan create . zinnion/stable --build missing -s compiler.libcxx=libstdc++11`


