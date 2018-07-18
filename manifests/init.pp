# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2 foldmethod=marker smartindent
#
# == Class: dhclient
# ---
#
# Manages the DHCP Client for AWS instances (Route53 DNS)
#
# === Parameters
# ---
#
# [*interface*]
# - Default - eth0
# - Expects - (*String*) - The interface to manage the DHCP client requests
#
# [*searchpath*]
# - Default - (*Hiera*) - system:dns:searchpath (OR $::domain if no Hiera data)
# - Expects - (*Array*) - The system DNS default searchpath(s)
#
# [*nameservers*]
# - Default - [] - Will allow dhclient to use it's best judgement on nameservers
# - Expects - (*Array*) - The system DNS custom nameservers
class dhclient(

  $interface  = 'eth0',
  $searchpath = $::domain,
  $nameservers = [],

) {

  # Workaround for use of hiera_* functions unsupported in class def header
  $sp = hiera_array('system:dns:searchpath', $searchpath)
  $ns = hiera_array('system:dns:nameservers', $nameservers)

  if ($::operatingsystem != 'Amazon') {
    clabs::module::unsupported { $name:
      msg =>
        "The ${name} module is only supported on the Amazon ::operatingsystem";
    }
  }

  clabs::module::init { $name: }

}

