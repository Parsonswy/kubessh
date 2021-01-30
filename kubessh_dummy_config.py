from kubessh.authentication.ldap import LDAPAuthenticator

# Make sure this exists
c.KubeSSH.host_key_path = 'dummy-kubessh-host-key'

c.KubeSSH.debug = True
c.KubeSSH.authenticator_class = LDAPAuthenticator