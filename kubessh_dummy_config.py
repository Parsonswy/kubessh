from kubessh.authentication.ldap import LDAPAuthenticator

# Make sure this exists
c.KubeSSH.host_key_path = 'dummy-kubessh-host-key'

c.KubeSSH.debug = True
c.KubeSSH.authenticator_class = LDAPAuthenticator
c.KubeSSH.authenticator_class.ldap_servers = [ 'dc01.ncsa.tech', 'dc02.ncsa.tech' ]