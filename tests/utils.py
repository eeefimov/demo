"""Class contains different utils functions.
    Add screenshot to Allure report.
    Load file json file.
    Setup Playwright interceptor to check requested endpoints
    when web page loads.
    Check target endpoint in requested routs.
    Get json from web page requests.
    Modify json ingredients data_models for response.
    Multiply x2 ingredients items.
    Create IMAP server, connect to gmail account
    get email with code.
"""
import os
import datetime
import json
import uuid
import allure
import easyimap as e


class UTILS:
    """Class contains different utils functions."""
    @staticmethod
    def add_screenshot(page: object):
        """Add screenshot to Allure report."""
        attach = page.screenshot()

        allure.attach(
            attach,
            name=f"Screenshot_{datetime.datetime.now()}",
            attachment_type=allure.attachment_type.PNG,
        )

    @staticmethod
    def load_file(filename: str):
        """Load file json file."""
        file_path = os.path.join(os.path.dirname(__file__), filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def setup_routs(page: object, endpoint: str, link: str):
        """
        Setup Playwright interceptor to check requested endpoints
        when web page loads.
        """
        target_url = [False]
        log_request = UTILS.check_request_endpoint(endpoint, target_url)
        page.route("**", log_request)
        page.goto(link)
        page.wait_for_timeout(3000)
        return target_url

    @staticmethod
    def check_request_endpoint(target_url, found_target_url):
        """Check target endpoint in requested routs."""
        def interceptor(route, request):
            if target_url in request.url:
                found_target_url[0] = True
            route.continue_()

        return interceptor

    @staticmethod
    def get_json_web(page: object, url: str) -> json:
        """Get json from web page requests."""
        page.goto(url)
        json_data = page.evaluate('''() => {
                return fetch(document.location.href)
                    .then(response => response.json());
            }''')
        return json_data

    @staticmethod
    @allure.step("Modify ingredients titles")
    def modify_ingredients(response: dict, new_value: str) -> dict:
        """Modify json ingredients data_models for response."""
        for i in range(0, len(response['data'])):
            response['data'][i]['name'] = new_value
        return response

    @staticmethod
    @allure.step("Double ingredients items")
    def double_data(response: dict) -> dict:
        """Multiply x2 ingredients items."""
        new_data = response.copy()
        new_data['data'] *= 2
        for i in range(len(new_data['data'])):
            new_data['data'][i]['_id'] = str(uuid.uuid4())
        return new_data

    @staticmethod
    def mail_check(user: str, password: str) -> [str, str]:
        """Create IMAP server, connect to gmail account
        get email with code."""
        server = e.connect('imap.gmail.com', user, password)
        message_ids = server.listids()

        if not message_ids:
            print("No messages found in the mailbox.")
            return None, None

        email = server.mail(message_ids[0])
        email_address: str = email.from_addr
        email_body: str = email.body
        start_index = email_body.find(": ") + 2
        end_index = email_body.find(".", start_index)
        code = email_body[start_index:end_index]
        return email_address, code
