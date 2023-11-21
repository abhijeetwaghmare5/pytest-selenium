import os, requests, json, base64
import shutil
from os import environ
import logging

logger = logging.getLogger()
if not logger.handlers:
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)


class AllureService:
    ALLURE_SERVER = "http://localhost:5252/allure-docker-service-ui/"
    SSL_VERIFICATION = False
    TOKEN_REQUIRED = False

    def __init__(self, allure_directory, html_dir, project_id: str = "assignment1", ):
        self.project_id = project_id
        self.session = requests.session()
        self.allure_directory = allure_directory
        self.html_dir = html_dir
        self.session.headers = {'Content-type': 'application/json'}

    def _get_request_body(self):
        # current_directory = os.path.dirname(os.path.realpath(__file__))
        # current_directory = current_directory.replace('/utils', '')
        # results_directory = current_directory + self.allure_directory
        results_directory = self.allure_directory
        logger.info('RESULTS DIRECTORY PATH: ' + results_directory)

        files = os.listdir(results_directory)

        logger.info('FILES:')
        results = []
        for file in files:
            result = {}

            file_path = results_directory + "/" + file
            #logger.info(file_path)

            if os.path.isfile(file_path):
                try:
                    with open(file_path, "rb") as f:
                        content = f.read()
                        if content.strip():
                            b64_content = base64.b64encode(content)
                            result['file_name'] = file
                            result['content_base64'] = b64_content.decode('UTF-8')
                            results.append(result)
                        else:
                            logger.info('Empty File skipped: ' + file_path)
                finally:
                    f.close()
            else:
                logger.info('Directory skipped: ' + file_path)

        request_body = {
            "results": results
        }
        return request_body

    @staticmethod
    def set_allure_service_variables(allure_server: str = None, results_directory: str = None):
        AllureService.ALLURE_SERVER = allure_server if allure_server is not None else AllureService.ALLURE_SERVER
        AllureService.RESULTS_DIRECTORY = results_directory if results_directory is not None else AllureService.RESULTS_DIRECTORY

    def send_results(self):
        logger.info("------------------SEND-REPORT------------------")
        json_request_body = self._get_request_body()
        logger.info(f"cookies: {self.session.cookies}")
        logger.info(f"{self.session.cookies['csrf_access_token']}")
        self.session.headers.update({'X-CSRF-TOKEN': self.session.cookies['csrf_access_token']})
        # self.session.headers.update({'project_id':})
        response = self.session.post(self.ALLURE_SERVER + 'send-results?project_id=' + self.project_id,
                                     data=json.dumps(json_request_body), verify=self.SSL_VERIFICATION)
        logger.info("STATUS CODE:")
        logger.info(response.status_code)
        if response.status_code != 200:
            logger.info("RESPONSE:")
            json_response_body = json.loads(response.content)
            json_prettier_response_body = json.dumps(json_response_body, indent=4, sort_keys=True)
            logger.info(json_prettier_response_body)
        return response

    def generate_report(self, execution_name: str = 'execution from python script',
                        execution_from: str = 'http://google.com', execution_type: str = 'local'):
        logger.info("------------------GENERATE-REPORT------------------")
        response = self.session.get(
            self.ALLURE_SERVER + 'generate-report?project_id=' + self.project_id + '&execution_name=' +
            execution_name + '&execution_from=' + execution_from + '&execution_type=' + execution_type,
            verify=self.SSL_VERIFICATION)
        logger.info("STATUS CODE:")
        logger.info(response.status_code)
        json_response_body = json.loads(response.content)
        if response.status_code != 200:
            logger.info("RESPONSE:")
            json_prettier_response_body = json.dumps(json_response_body, indent=4, sort_keys=True)
            logger.info(json_prettier_response_body)
            logger.info('ALLURE REPORT URL:')
            logger.info(json_response_body['data']['report_url'])
        return response

    def create_allure_project(self, project_name: str) -> str:
        pass

    def login(self):
        username = "abhijeet"
        password = "abhijeet123"
        response = self.session.post(url=self.ALLURE_SERVER + 'login',
                                     data=json.dumps({"password": password, "username": username})
                                     , verify=False)
        return response


if __name__ == '__main__':
    # allure_service_obj = AllureService()
    # allure_service_obj.send_results()
    root_directory = os.getcwd()
    ALLURE_DIRECTORY = r"C:\Users\dell\PycharmProjects\Assignment1\allure-results"
    HTML_DIRECTORY = f"{root_directory}/render.html"
    EXPORT_REPORT_DIR = f"{root_directory}"
    logger.info(f"ALLURE_DIRECTORY: {ALLURE_DIRECTORY}")
    PROJECT_ID = 'assignment1' if "PROJECT_ID" not in os.environ else os.environ["PROJECT_ID"]
    s = AllureService(allure_directory=ALLURE_DIRECTORY, html_dir=HTML_DIRECTORY, project_id=PROJECT_ID)
    r = s.login()
    logger.info(f"Session Status: {r.status_code}")
    s.send_results()