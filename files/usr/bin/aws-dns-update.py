#!/usr/bin/env python
import re
import sys
import boto
from boto.route53.record import ResourceRecordSets

# You may either embed the credentials here, or if these variables are left set to None,
# boto will automatically look for credentials configuration files in ~/.boto and
# /etc/boto.cfg.  See http://code.google.com/p/boto/wiki/BotoConfig for details.
AWS_ACCESS_KEY = None
AWS_SECRET_ACCESS_KEY = None

def get_ip_address():
  ip_address = ''
  tcp_stat = open('/proc/net/tcp', 'r')
  tcp_lines = tcp_stat.readlines()
  for line in tcp_lines:
    match_obj = re.match('^\d+: ([0-9A-Fa-f]+)', line.strip())
    if not match_obj:
      continue
    addr = match_obj.group(1)
    if addr == '0100007F' or addr == '00000000':
      continue
    for i in range(8, 0, -2):
      ip_address += str(int(addr[i-2:i], 16))
      if i > 2:
        ip_address += '.'
    if not ip_address:
      sys.stederr.write('Error:  Could not determine my own IP address.')
    return ip_address

def update_route53_record(conn, ip_address, hostname, domain):
  hosted_zone_name = domain if domain.endswith('.') else domain + '.'
  zone = conn.get_hosted_zone_by_name(hosted_zone_name)
  zone_id = zone['GetHostedZoneResponse']['HostedZone']['Id'].split('/')[2]
  rrsets = conn.get_all_rrsets(zone_id, type='A', name=hostname + '.' + hosted_zone_name)
  changes = ResourceRecordSets(conn, zone_id)

  if len(rrsets) != 0:
    for rrset in rrsets:
      # For some stupid reason Route53 will return RRsets that have nothing
      # to do with what we asked for, so this checks to be sure we're working
      # with the RRset we asked for.
      if rrset.type == 'A' and rrset.name == hostname + '.' + hosted_zone_name:
        change = changes.add_change('DELETE', rrset.name, rrset.type)
        for rr in rrset.resource_records:
          change.add_value(rr)
  change = changes.add_change('CREATE', hostname + '.' + hosted_zone_name, 'A')
  change.add_value(ip_address)
  try:
    ret = changes.commit()
  except boto.route53.exception.DNSServerError as e:
    sys.stderr.write('Error:  Failed to update RRs\n  %s' % e)
    return False
  return True

def get_system_hostname():
  network_file = open('/etc/sysconfig/network', 'r')
  for line in network_file.readlines():
    match_obj = re.match('^HOSTNAME=(\S+)$', line)
    if match_obj:
      return match_obj.group(1)
  sys.stderr.write('Error:  Could not determine local hostname?!?')
  return None

if __name__ == '__main__':
  fqdn = get_system_hostname()
  if not fqdn:
    sys.exit(1)
  if '.useast1.' in fqdn:
    # legacy VPCs had instance shortnames of the form xxx.useast1
    short = '.'.join(fqdn.split('.')[0:2])
    domain = fqdn.split('.', 2)[2]
  else:
    # new VPCs have normal shortnames without subdomains
    short = fqdn.split('.')[0]
    domain = fqdn.split('.', 1)[1]
  ip = get_ip_address()
  if not ip:
    sys.exit(1)
  conn = boto.connect_route53(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)
  if not conn:
    sys.exit(1)
  ret = update_route53_record(conn, ip, short, domain)
  sys.exit(0 if ret else 1)
