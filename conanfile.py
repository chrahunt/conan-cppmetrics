#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import shutil


class CppmetricsConan(ConanFile):
    name = "cppmetrics"
    version = "0.1.1"
    description = "Keep it short"
    url = "https://github.com/bincrafters/conan-libname"
    homepage = "https://github.com/ultradns/cppmetrics"

    # Indicates License type of the packaged library
    license = "Apache-2.0"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    requires = (
        "boost_asio/[>=1.53.0]@bincrafters/stable",
        "boost_atomic/[>=1.53.0]@bincrafters/stable",
        "boost_chrono/[>=1.53.0]@bincrafters/stable",
        "boost_date_time/[>=1.53.0]@bincrafters/stable",
        "boost_filesystem/[>=1.53.0]@bincrafters/stable",
        "boost_foreach/[>=1.53.0]@bincrafters/stable",
        "boost_lexical_cast/[>=1.53.0]@bincrafters/stable",
        "boost_random/[>=1.53.0]@bincrafters/stable",
        "boost_smart_ptr/[>=1.53.0]@bincrafters/stable",
        "boost_thread/[>=1.53.0]@bincrafters/stable",
        "boost_timer/[>=1.53.0]@bincrafters/stable",
        "gflags/2.2.1@bincrafters/stable",
        "glog/0.3.5@bincrafters/stable",
    )

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://github.com/ultradns/cppmetrics"
        # XXX: issue has been opened to tag relevant commit with version
        #tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        commit = 'd360363f3a8ffd1ce7b9e89784d8df4c83098f34'
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, commit))
        extracted_dir = self.name + "-" + commit

        # Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)
        # Overwrite existing CMakeLists.txt, it is not salvageable.
        os.remove(os.path.join(self.source_subfolder, 'CMakeLists.txt'))
        os.rename('CMakeLists.txt', os.path.join(self.source_subfolder, 'CMakeLists.txt'))

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = False # example
        if self.settings.os != 'Windows':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        # We override CMakeLists.txt and use the following:
        cmake.definitions["CONAN_INCLUDE_DIRS"] = ';'.join(self.deps_cpp_info.include_paths)
        cmake.definitions["CONAN_LIB_DIRS"] = ';'.join(self.deps_cpp_info.lib_paths)
        cmake.configure(build_folder=self.build_subfolder, source_folder=self.source_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        #self.copy(pattern="LICENSE", dst="license", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()
        # If the CMakeLists.txt has a proper install method, the steps below may be redundant
        # If so, you can just remove the lines below
        # include_folder = os.path.join(self.source_subfolder, "include")
        self.copy(pattern="*", dst="include", src='include')
        self.copy(pattern="*", dst="lib", src='lib')
        #self.copy(pattern="*.dll", dst="bin", keep_path=False)
        #self.copy(pattern="*.lib", dst="lib", keep_path=False)
        #self.copy(pattern="*.a", dst="lib", keep_path=False)
        #self.copy(pattern="*.so*", dst="lib", keep_path=False)
        #self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
