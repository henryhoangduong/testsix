import os
import argparse
import urllib3
import gitlab
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

class GitlabClient():
    def __init__(self, url, authkey, project):
        # Parse command line arguments
        self.url = url
        self.authkey = authkey
        self.project_name = project
        self.project = None
        self.mrs = None  # list of all merge requests
        # Create python-gitlab server instance
        server = gitlab.Gitlab(self.url, authkey, api_version=4, ssl_verify=False)
        # Get an instance of the project and store it off
        self.project = server.projects.get(self.project_name)
        
    def get_raw_file(self, file_path, destination, branch):
        with open(destination, 'wb') as f:
            self.project.files.raw(file_path=file_path, ref=branch, streamed=True, action=f.write)

    def get_raw_content(self, file_path, branch):
        raw_content = self.project.files.raw(file_path=file_path, ref=branch)
        return raw_content


if __name__ == '__main__':
    token = os.getenv("GITLAB_ACCESS_TOKEN")
    parser = argparse.ArgumentParser(description='Three examples of using the REST API. 1st: Summarize all open MRs, 2nd: Post note to existing MR, 3rd: Create new issue in project.')
    parser.add_argument( "--authkey", type=str, dest='authkey', action='store', default=token, help="Personal access token for authentication with GitLab. Create one at https://gitlab.com/profile/personal_access_tokens" )
    parser.add_argument( "--project", type=str, dest='project', action='store', default="automate-solutions-tasks/heppai.tasks.prototype",help="Path to GitLab project in the form <namespace>/<project>")
    parser.add_argument( "--url", dest='url', action='store', help="Gitlab URL.", default='https://gitlab.com/')
    args = parser.parse_args()

    python_gitlab_client = GitlabClient(url=args.url, authkey=args.authkey, project=args.project)
    #python_gitlab_client.get_raw_file(file_path="parameter.json", destination="/tmp/parameter.json", branch="main")
    file_content = python_gitlab_client.get_raw_content(file_path="parameter.json", branch="main")
    print(file_content)
