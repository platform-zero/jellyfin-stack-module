import os,pathlib,subprocess,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
SOURCE=(ROOT/'stack.config/jellyfin/entrypoint.sh').read_text()
def function(name):
 start=SOURCE.index(name+'() {');return SOURCE[start:SOURCE.index('\n}',start)+2]
class BootstrapPrivacy(unittest.TestCase):
 def test_bounded_entropy_under_pipefail(self):
  script='set -euo pipefail\n'+function('new_bootstrap_token')+'\nfor i in {1..25}; do token="$(new_bootstrap_token)"; [[ "$token" =~ ^[a-f0-9]{48}$ ]]; done; echo bounded-ok'
  r=subprocess.run(['bash','-c',script],capture_output=True,text=True,timeout=10);self.assertEqual(r.returncode,0);self.assertEqual(r.stdout.strip(),'bounded-ok')
 def render(self,secret,symlink=False):
  with tempfile.TemporaryDirectory()as t:
   root=pathlib.Path(t);template=root/'template';target=root/'target';outside=root/'authored'
   template.write_text('<secret>{{JELLYFIN_OIDC_SECRET}}</secret><host>{{DOMAIN}}</host>');outside.write_text('authored-sentinel')
   if symlink:target.symlink_to(outside)
   else:target.write_text('old-render');target.chmod(0o644)
   start=SOURCE.index('if [ -f /config-templates/SSO-Auth.xml ]');end=SOURCE.index('\nunset JELLYFIN_OIDC_SECRET',start)
   block=SOURCE[start:end].replace('/config-templates/SSO-Auth.xml',str(template)).replace('/config/plugins/configurations/SSO-Auth.xml',str(target))
   script='set -euo pipefail\n'+function('escape_sed_replacement')+'\n'+function('escape_xml_text')+'\n'+block
   r=subprocess.run(['bash','-c',script],env={**os.environ,'DOMAIN':'example.invalid','JELLYFIN_OIDC_SECRET':secret},capture_output=True,text=True)
   return r,target.read_text(),target.stat().st_mode&0o777,outside.read_text(),script
 def test_private_literal_xml_render_not_secret_command_arguments(self):
  secret='fixture-private-&|\\-token';r,text,mode,outside,script=self.render(secret)
  import xml.etree.ElementTree as ET
  self.assertEqual(r.returncode,0);self.assertEqual(ET.fromstring('<config>'+text+'</config>').findtext('secret'),secret);self.assertEqual(mode,0o600);self.assertNotIn(secret,r.stdout+r.stderr+script)
  self.assertIn('| sed -f -',script);self.assertNotIn('-e "s|{{JELLYFIN_OIDC_SECRET}}',script)
 def test_symlink_preserves_authored_outside_file(self):
  r,text,mode,outside,script=self.render('fixture-private-token',True);self.assertNotEqual(r.returncode,0);self.assertEqual(outside,'authored-sentinel')
 def test_multiline_secret_refused_privately(self):
  secret='fixture-private\nsecondline';r,text,mode,outside,script=self.render(secret);self.assertNotEqual(r.returncode,0);self.assertNotIn(secret,r.stdout+r.stderr);self.assertEqual(text,'old-render')
 def test_curl_private_header_and_error_body_not_emitted(self):
  self.assertNotIn('-H "X-Emby-Token: $token"',SOURCE);self.assertEqual(SOURCE.count('X-Emby-Token: %s'),3);self.assertNotIn('/tmp/jellyfin-add-library.out',SOURCE)
 def test_native_admin_readiness_wait_is_bounded_and_does_not_replace_token(self):
  self.assertIn('case "$status" in 000|401|503)',SOURCE);self.assertIn('Jellyfin native library readiness deadline elapsed',SOURCE);self.assertIn('for _ in $(seq 1 120)',SOURCE)
 def test_initialized_token_is_preserved(self):
  self.assertIn('WHERE NOT EXISTS (SELECT 1 FROM ApiKeys WHERE Name',SOURCE);self.assertIn('SELECT AccessToken FROM ApiKeys WHERE Name',SOURCE);self.assertNotIn('UPDATE ApiKeys',SOURCE)
if __name__=='__main__':unittest.main()
