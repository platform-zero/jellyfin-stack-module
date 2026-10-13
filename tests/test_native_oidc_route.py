from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class NativeOidcRoute(unittest.TestCase):
 def test_owned_gateway_preserves_public_authority_and_ca(self):
  text=(ROOT/'stack.runtime.yaml').read_text()
  self.assertIn('"keycloak.${DOMAIN}:host-gateway"',text)
  self.assertIn('SSL_CERT_FILE: "/ca/caddy-ca.crt"',text)
  self.assertIn('"caddy_ca:/ca:ro"',text)
  self.assertNotIn('insecure',text.lower());self.assertNotIn('skipverify',text.lower())
if __name__=='__main__':unittest.main()
