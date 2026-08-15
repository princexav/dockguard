import unittest
from dockguard.rules import scan_dockerfile

class TestDockguardRules(unittest.TestCase):
    def test_insecure_dockerfile_findings(self):
        dockerfile = """
        FROM python:latest
        ENV API_KEY=secret_token_123
        EXPOSE 22
        CMD ["python", "app.py"]
        """
        findings = scan_dockerfile(dockerfile)
        rule_ids = [f.rule_id for f in findings]
        
        self.assertIn("DG-001", rule_ids) # unpinned tag
        self.assertIn("DG-002", rule_ids) # secret in ENV
        self.assertIn("DG-003", rule_ids) # exposed SSH port 22
        self.assertIn("DG-004", rule_ids) # no non-root user
        self.assertIn("DG-005", rule_ids) # no healthcheck

    def test_secure_dockerfile(self):
        dockerfile = """
        FROM python:3.11.4-slim
        RUN useradd -m appuser
        USER appuser
        HEALTHCHECK --interval=30s CMD curl -f http://localhost:8000/health || exit 1
        CMD ["python", "app.py"]
        """
        findings = scan_dockerfile(dockerfile)
        high_findings = [f for f in findings if f.severity == "HIGH"]
        self.assertEqual(len(high_findings), 0)

if __name__ == "__main__":
    unittest.main()
