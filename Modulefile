# vim: set filetype=ruby :

name            'dhclient'
author          'Convection Labs'
license         'Proprietary'
summary         'Convection Labs AWS DHCP Client'
description     'Manages an AWS DHCP Client setting'
source          'https://bitbucket.org/convectionlabs/puppet-module-dhclient'
project_page    'https://bitbucket.org/convectionlabs/puppet-module-dhclient'

dependency      'clabs/core', '>= 0.0.1'

# Set up our git directory, and figure out where the module is, so that
# we can run a successful build outside the working directory; this happens
# when puppet-librarian tries to build from git, at least.
moduledir = File.dirname(__FILE__)
ENV['GIT_DIR'] = moduledir + '/.git'

# Grab the version number from git, and bump up the tiny version number if we
# have a postfix string, since Puppet only supports SemVer 1.0.0, which
# doesn't have anything but "version" and "pre-release of version".
#
# Technically this isn't accurately reflecting the real next release number,
# but whatever - it will do for now.
#git_version = %x{#{moduledir}/bin/get-version-from-git}.chomp
#unless $?.success? and git_version =~ /^\d+\.\d+\.\d+/
#  raise "Unable to determine version using git: #{$?} => #{git_version.inspect}"
#end

#version    git_version
version         '0.0.1'

# Generate the changelog file
#system("'#{moduledir}'/bin/git-log-to-changelog > '#{moduledir}'/CHANGELOG")
#$? == 0 or fail "changelog generation #{$?}!"

# Generate the contributor list in README.md
#system("git shortlog -se|sort -nr|sed -e's/^.\\{7\\}/ - /' > #{moduledir}/CONTRIBUTORS")
#$? == 0 or fail "contributor list generation #{$?}!"

