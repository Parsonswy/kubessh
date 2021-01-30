from kubessh.authentication import Authenticator
import ldap
import socket
import sys
from traitlets import List

class LDAPAuthenticator(Authenticator):
	"""
	Authenticate with LDAP(S)
	"""
	allowed_users = List(
		[],
		config=True,
		help="""
			List of GitHub users allowed to log in.
			By default, no users are allowed
		"""
	)

	ldap_servers = List(
		[],
		config=True,
		help="""
			List of FQDN:port and/or IP Addresses:port of LDAP servers.
			Will attempt connections sequentailly until finding
			a responsive server to handle the query.
		"""
	)

	def connection_made(self, conn):
		self.conn = conn

	def public_key_auth_supported(self):
		return False

	def password_auth_supported(self):
		return True

	async def validate_password(self, username, password):
		connectionString = self.test_ldap_server_connection_strings()
		if connectionString is None:
			self.log.info(f"[LDAP] Unable to authenticate user {username}. No LDAP servers responded to ping.")
			return False

		ldapConn = ldap.initialize(connectionString)
		ldapConn.protocol_version = 3
		ldapConn.set_option(ldap.OPT_REFERRALS, 0)
		try:
			result = ldapConn.simple_bind_s(username, password)
			ldapConn.unbind_s()
			return True
		except ldap.INVALID_CREDENTIALS:
			self.log.info(f"[LDAP] User {username} attempted to authenticate to backend {connectionString}, but password was incorrect.")
			return False
		except ldap.LDAPError as e:
			self.log.info("f[LDAP] Error authenticating user {username} " + e.message['desc'])
			return False
	
	"""
	Test the connection strings provided to find an online LDAP server
	"""
	def test_ldap_server_connection_strings(self):
		s = socket.socket()
		for conString in self.ldap_servers:
			addrComponents = conString.split(":")
			testAddress = addrComponents[0]
			testPorts = [636, 389]

			# has custom port
			if (len(addrComponents) > 1):
				testPorts.insert(0, addrComponents[1])

			for testPort in testPorts:
				try:
					self.log.info(f"[LDAP] Pinging server {testAddress}:{testPort}")
					s.connect((testAddress, testPort))
					s.close()
					self.log.info(f"[LDAP] ... ping succedded. Using this server.")

					# TODO: This doesn't support LDAPS on non-standard ports
					if testPort == 636:
						return "ldaps://" + testAddress + ":" + str(testPort)
					return "ldap://" + testAddress + ":" + str(testPort)

				except Exception:
					self.log.info(f"[LDAP] ... ping failed.")

		s.close()
		return None
