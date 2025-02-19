import os
import json
import requests
import argparse

SNYK_TOKEN = os.getenv("SNYK_TOKEN")


class APIClient:
    def __init__(
        self, snyk_token, owner, name, snyk_org, integration_id, branch
    ) -> None:
        self.snyk_token = snyk_token
        self.owner = owner
        self.name = name
        self.snyk_org = snyk_org
        self.integration_id = integration_id
        self.branch = branch
        self.base_url = "https://api.snyk.io/v1"

    def import_repo(self) -> object:
        request_url = f"{self.base_url}/org/{self.snyk_org}/integrations/{self.integration_id}/import"
        headers = self._format_headers()
        body = self._format_body()
        response = requests.post(
            request_url,
            headers=headers,
            data=body,
        )
        return response

    def _format_body(self) -> object:
        body = json.dumps(
            {"target": {"owner": self.owner, "name": self.name, "branch": self.branch}}
        )
        return body

    def _format_headers(self) -> object:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"token {self.snyk_token}",
        }
        return headers


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import a repository to Snyk.")
    parser.add_argument("--owner", required=True, help="Repository owner")
    parser.add_argument("--name", required=True, help="Repository name")
    parser.add_argument("--snyk-org", required=True, help="Snyk organization ID")
    parser.add_argument("--integration-id", required=True, help="Snyk integration ID")
    parser.add_argument("--branch", required=True, help="Repository branch")

    args = parser.parse_args()

    client = APIClient(
        SNYK_TOKEN,
        args.owner,
        args.name,
        args.snyk_org,
        args.integration_id,
        args.branch,
    )
    response = client.import_repo()
    print("status_code", response.status_code)
