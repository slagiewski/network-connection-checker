import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from datetime import datetime

from email_service import send_email
import config
import constants

log = print

translate = constants.translate


def today(): return str(datetime.today())


def ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    command = ['ping', param, '1', host]

    return subprocess.call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def check_connection(hosts_config):
    """
        Returns dict with keys:
            1. valid                -> bool
            2. error_msg            -> str
            3. error_source_type    -> str (Local/External)
    """

    response = {
        "valid": True,
        "error_msg": None,
        "error_source_type": None
    }

    def make_response_invalid(error_msg, error_source_type):
        response["valid"] = False
        response["error_msg"] = error_msg
        response["error_source_type"] = error_source_type

    def check_local_connection():
        local_hosts = filter(
            lambda host: host.get("type", "") == constants.LOCAL_HOST,
            hosts_config
        )

        for local_host in local_hosts:
            if not ping(local_host["address"]):
                make_response_invalid(
                    constants.LocalConnectionIsNotWorking,
                    constants.LOCAL_HOST)
                return

    def check_external_connection():
        external_hosts = filter(
            lambda host: host.get("type", "") == constants.EXTERNAL_HOST,
            hosts_config
        )
        num_of_tries = 3
        num_of_failures = 0
        for external_host in external_hosts:
            for _ in range(num_of_tries):
                if not ping(external_host["address"]):
                    num_of_failures += 1
            if num_of_failures == num_of_tries:
                make_response_invalid(
                    f"{translate(constants.ConnectionIssueWith)} [{external_host['name']}]",
                    constants.EXTERNAL_HOST
                )

    check_local_connection()

    if not response["valid"]:
        return response

    check_external_connection()

    return response


def smtpEmailNotifier(receiver_email):
    return lambda message: send_email(config.email_receiver, message, config.email_subject, config.smtp)


def main():
    notifier = smtpEmailNotifier(config.email_receiver)

    result = check_connection(config.hosts)

    if not result["valid"]:
        msg = f"[{today()}] {result['error_msg']}"
        log(msg)
        if result["error_source_type"] == constants.EXTERNAL_HOST:
            notifier(msg)
    else:
        log(f"Connection test finished successfully at {today()}")


if __name__ == '__main__':
    main()
