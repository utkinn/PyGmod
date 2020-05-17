file(GLOB python_stdlib_py ${PYTHON_SOURCE_DIR}/Lib/*)
file(GLOB python_stdlib_pyd ${PYTHON_SOURCE_DIR}/PCbuild/win32/*.pyd)

set(stdlib_dir stdlib)
file(MAKE_DIRECTORY ${stdlib_dir}/lib)
file(COPY ${python_stdlib_py} DESTINATION ${stdlib_dir}/lib)
file(COPY ${python_stdlib_pyd} DESTINATION ${stdlib_dir}/lib)

file(TOUCH stdlib.generated)
