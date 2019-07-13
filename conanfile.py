# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import os


class CppTaskflowConan(ConanFile):
    name = "cpp-taskflow"
    version = "2.2.0"
    description = "A fast C++ header-only library to help you quickly write parallel programs with complex task dependencies."
    topics = ("conan", "cpp-taskflow", "tasking", "parallelism")
    url = "https://github.com/Hopobcn/conan-cpp-taskflow"
    homepage = "https://github.com/cpp-taskflow/cpp-taskflow"
    author = "Hopobcn <hopobcn@gmail.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False], 
        "fPIC": [True, False]
    }
    default_options = {
        "shared": False, 
        "fPIC": True
    }

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def configure(self):
        if self.settings.compiler.cppstd.value < "17":
            raise ConanInvalidConfiguration("cpp-taskflow requires c++17")
            
    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        sha256 = "60b2340ff029a241a3371d88c26b778ba7fccdf1a95995a716d9220575771689"
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["TF_BUILD_EXAMPLES"] = False
        cmake.definitions["TF_BUILD_TESTS"] = False
        cmake.definitions["TF_BUILD_BENCHMARKS"] = False
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if not self.settings.os == "Windows":
            self.cpp_info.cxxflags = ["-pthread"]
