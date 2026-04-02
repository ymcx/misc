project(
  'thinkled',
  'c',
  meson_version : '>= 1.3.0',
  version : '0.1',
  default_options : ['warning_level=3'],
)

dependencies = [
  dependency('libsystemd')
]

sources = [
  'thinkled.c',
]

exe = executable(
  'thinkled',
  sources,
  dependencies : dependencies,
  install : true,
)

test('basic', exe)
