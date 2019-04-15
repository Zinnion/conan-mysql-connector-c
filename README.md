## Package Status

mysql 8.x	

https://github.com/linux-on-ibm-z/docs/wiki/Building-MySQL-8.x



### X DevAPI User Guide

https://downloads.mysql.com/docs/x-devapi-userguide-en.pdf


### Pkg creation
conan create . zinnion/stable --build missing -s compiler.libcxx=libstdc++11

How to manage the GCC >= 5 ABI
In version 5.1, GCC released libstdc++, which introduced a new library ABI that includes new implementations of std::string and std::list. These changes were necessary to conform to the 2011 C++ standard which forbids Copy-On-Write strings and requires lists to keep track of their size.

You can choose which ABI to use in your Conan packages by adjusting the compiler.libcxx:

libstdc++: Old ABI.
libstdc++11: New ABI.
When Conan creates the default profile the first time it runs, it adjusts the compiler.libcxx setting to libstdc++ for backwards compatibility. However, if you are using GCC >= 5 your compiler is likely to be using the new CXX11 ABI by default (libstdc++11).

If you want Conan to use the new ABI, edit the default profile at ~/.conan/profiles/default adjusting compiler.libcxx=libstdc++11 or override this setting in the profile you are using.
