project('looptools', 'c', 'fortran')

py = import('python').find_installation(pure: false)

install_subdir(
    'looptools',
    install_dir: py.get_install_dir(),
)

ext_src = custom_target(
    command: [py, files('looptools_build.py')],
    output: '_looptools_lib.c'
)

looptools_lib = declare_dependency(
  link_args: ['-lgfortran' ,'-LLoopTools-2.16/build','-looptools']
)

py.extension_module(
    '_looptools_lib',
    ext_src,
    install: true,
    include_directories: ['LoopTools-2.16/build'],
    dependencies: [py.dependency(), looptools_lib],
    limited_api: '3.8',
)

#
# py.extension_module(
#     '_looptools_lib',
#     ['_looptools_lib.c'],
#     include_directories : ['LoopTools-2.16/build'],
#     install: true,
# )
