# 101-setup_web_static.pp

exec { 'update_apt':
  command => '/usr/bin/apt-get update',
  path    => ['/usr/bin', '/usr/sbin'],
  unless  => 'test -f /var/lib/apt/periodic/update-success-stamp',
}

package { 'nginx':
  ensure  => installed,
  require => Exec['update_apt'],
}

file { '/data':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  require => File['/data'],
}

file { '/data/web_static/releases':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  require => File['/data/web_static'],
}

file { '/data/web_static/shared':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  require => File['/data/web_static/releases'],
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  require => File['/data/web_static/shared'],
}

file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => '<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['/data/web_static/releases/test'],
}

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  force  => true,
  require => File['/data/web_static/releases/test/index.html'],
}

exec { 'set_ownership':
  command => 'chown -R ubuntu:ubuntu /data/',
  path    => ['/usr/bin', '/usr/sbin'],
  unless  => 'stat -c "%U:%G" /data | grep "ubuntu:ubuntu"',
  require => File['/data/web_static/current'],
}

file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  content => template('nginx/default.erb'),
  notify  => Service['nginx'],
}

service { 'nginx':
  ensure     => 'running',
  enable     => true,
  subscribe  => File['/etc/nginx/sites-available/default'],
}

file_line { 'nginx_hbnb_static':
  path  => '/etc/nginx/sites-available/default',
  line  => 'location /hbnb_static/ { alias /data/web_static/current/; }',
  match => '^location /hbnb_static/',
  notify  => Service['nginx'],
  require => File['/etc/nginx/sites-available/default'],
}
