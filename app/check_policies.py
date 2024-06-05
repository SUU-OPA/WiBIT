import os

import json
import logging
import requests

opa_url = os.environ.get("OPA_ADDR", "http://localhost:8181")
policy_path = os.environ.get("POLICY_PATH", "/v1/data/httpapi/authz")


def check_auth_policies(username, option, method, token):
    input_dict = {"input": {
        "user": username,
        "option": option,
        "method": method,
    }}
    if token is not None:
        input_dict["input"]["token"] = token

    logging.info("Checking auth...")
    logging.info(json.dumps(input_dict, indent=2))
    try:
        rsp = requests.post(opa_url + policy_path, data=json.dumps(input_dict))
    except Exception as err:
        logging.info(err)
        return {}
    j = rsp.json()
    if rsp.status_code >= 300:
        logging.info("Error checking auth, got status %s and message: %s", j.status_code, j.text)
        return {}
    logging.info("Auth response:")
    logging.info(json.dumps(j, indent=2))
    return j
