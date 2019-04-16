#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import glob
import os

class MysqlConnectorCConan(ConanFile):
    name = "mysql-connector-c"
    version = "8.0.15"
    url = "https://github.com/Zinnion/conan-percona-server"
    description = "A MySQL client library for C development."
    topics = ("conan", "mysql", "sql", "connector", "database")
    homepage = "https://cdn.mysql.com//Downloads/Connector-C++"
    author = "Zinnion <mauro@zinnion.com>"
    license = "GPL-2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "with_ssl": [True, False], "with_zlib": [True, False]}
    default_options = {'shared': False, 'with_ssl': True, 'with_zlib': True}
    _source_subfolder = "source_subfolder"

    #def config_options(self):
    #    del self.settings.compiler.libcxx

    def requirements(self):
        if self.options.with_ssl:
            self.requires.add("OpenSSL/1.1.1b@zinnion/stable")

        if self.options.with_zlib:
            self.requires.add("zlib/1.2.11@zinnion/stable")

    def source(self):
        tools.get("{0}/mysql-connector-c++-{1}-src.tar.gz".format(self.homepage, self.version))
        extracted_dir = "mysql-connector-c++-" + self.version + "-src"
        os.rename(extracted_dir, self._source_subfolder)

        sources_cmake = os.path.join(self._source_subfolder, "CMakeLists.txt")
        sources_cmake_orig = os.path.join(self._source_subfolder, "CMakeListsOriginal.txt")

        os.rename(sources_cmake, sources_cmake_orig)
        os.rename("CMakeLists.txt", sources_cmake)

    def build(self):
        cmake = CMake(self)
        if self.options.with_ssl:
            cmake.definitions["WITH_SSL"] = "system"

        if self.options.with_zlib:
            cmake.definitions["WITH_ZLIB"] = "system"
       
        cmake.configure(source_dir=self._source_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        pass

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        #self.cpp_info.bindirs = ['lib']
