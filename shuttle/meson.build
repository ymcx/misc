project(
  'shuttle',
  'c',
  meson_version : '>= 1.3.0',
  version : '0.1',
  default_options : ['warning_level=3'],
)

dependencies = [
  dependency('libcurl'),
  dependency('libxml2'),
  dependency('zlib')
]

sources = [
  'shuttle.c',
]

exe = executable(
  'shuttle',
  sources,
  dependencies : dependencies,
  install : true,
)

test('basic', exe)
