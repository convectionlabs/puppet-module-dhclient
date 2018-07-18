# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2 foldmethod=marker smartindent
#
# == Class: dhclient::config
# ---
#
# Manages the DHCP Client for AWS instances
#
class dhclient::config inherits dhclient {

  clabs::exe { [
      '/usr/bin/aws-dns-update.py',
      '/etc/dhcp/dhclient-exit-hooks',
    ]:
    notify => Exec['restart_networking'];
  }

  $spath = inline_template('<%= @sp.flatten.join(" ") %>')
  $nsstring = inline_template('<%= @ns.flatten.join(" ") %>')

  clabs::template { '/etc/dhcp/dhclient.conf': }
  clabs::template { '/etc/dhcp/dhclient-enter-hooks': }

  exec { 'restart_networking':
    command     => 'service network restart',
    path        => '/bin:/sbin:/usr/bin:/usr/sbin',
    require     => Clabs::Template['/etc/dhcp/dhclient.conf'],
    refreshonly => true,
  }

}
