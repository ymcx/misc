project(
  'tlglowctl',
  'c',
  meson_version : '>= 1.3.0',
  version : '0.1',
  default_options : ['warning_level=3'],
)

dependencies = [
  dependency('libsystemd'),
]

sources = [
  'main.c',
]

exe = executable(
  'tlglowctl',
  sources,
  dependencies : dependencies,
  install : true,
  link_args : ['-lm']
)

test('basic', exe)
