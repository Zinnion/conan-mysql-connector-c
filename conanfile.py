#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import glob
import os

class MysqlConnectorCConan(ConanFile):
    name = "conan-percona-server"
    version = "8.0.15"
    url = "https://github.com/Zinnion/conan-percona-server"
    description = "A percona server library for C development."
    topics = ("conan", "mysql", "sql", "connector", "database")
    homepage = "https://cdn.mysql.com//Downloads"
    author = "Zinnion <mauro@zinnion.com>"
    license = "GPL-2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "with_ssl": [True, False], "with_zlib": [True, False]}
    default_options = {'shared': False, 'with_ssl': True, 'with_zlib': True}
    _source_subfolder = "source_subfolder"

    def requirements(self):
        self.requires.add("boost/1.68.0@conan/stable")

        if self.options.with_ssl:
            self.requires.add("OpenSSL/1.0.2o@conan/stable")

        if self.options.with_zlib:
            self.requires.add("zlib/1.2.11@conan/stable")
        

    def source(self):
        tools.get("{0}/MySQL-8.0/mysql-{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = "mysql-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

        sources_cmake = os.path.join(self._source_subfolder, "CMakeLists.txt")
        sources_cmake_orig = os.path.join(self._source_subfolder, "CMakeListsOriginal.txt")

        os.rename(sources_cmake, sources_cmake_orig)
        os.rename("CMakeLists.txt", sources_cmake)

    def build(self):
        cmake = CMake(self)

        if self.options.shared:
            cmake.definitions["DISABLE_SHARED"] = "OFF"
            cmake.definitions["DISABLE_STATIC"] = "ON"
        else:
            cmake.definitions["DISABLE_SHARED"] = "ON"
            cmake.definitions["DISABLE_STATIC"] = "OFF"

        if self.settings.compiler == "Visual Studio":
            if self.settings.compiler.runtime == "MD" or self.settings.compiler.runtime == "MDd":
                cmake.definitions["WINDOWS_RUNTIME_MD"] = "ON"

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
        self.cpp_info.bindirs = ['lib']
