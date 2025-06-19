import requests
import logging
import xml.etree.ElementTree as ET
from typing import Optional, Tuple
from datetime import datetime, timedelta
from dify_plugin.config.logger_format import plugin_logger_handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(plugin_logger_handler)


class SalesforceSessionManager:
    def __init__(self, username: str, password_with_token: str, login_url: str, storage):
        self.username = username
        self.password_with_token = password_with_token
        self.login_url = login_url.strip().rstrip('/')
        self.storage = storage
        self.session_key = f"salesforce_session_{username}"
        self.instance_url_key = f"salesforce_instance_url_{username}"
        self.session_expiry_key = f"salesforce_session_expiry_{username}"

        logger.info(f"Initialized Salesforce session manager for user: {username[:3]}***")

    def _soap_login(self) -> Optional[Tuple[str, str]]:
        logger.info(f"Starting SOAP login for user: {self.username[:3]}***")

        try:
            soap_envelope = f"""<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:urn="urn:partner.soap.sforce.com">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:login>
         <urn:username>{self.username}</urn:username>
         <urn:password>{self.password_with_token}</urn:password>
      </urn:login>
   </soapenv:Body>
</soapenv:Envelope>"""

            headers = {
                "Content-Type": "text/xml",
                "SOAPAction": '""'
            }

            request_url = f"{self.login_url}/services/Soap/u/63.0"
            logger.info(f"SOAP Login Request URL: {request_url}")
            logger.info(f"Username: {self.username}")
            logger.info(f"Password length: {len(self.password_with_token)} characters")

            logger.info("Sending SOAP login request to Salesforce")
            response = requests.post(
                request_url,
                headers=headers,
                data=soap_envelope,
                timeout=30
            )

            logger.info(f"SOAP login response status: {response.status_code}")

            if response.status_code == 200:
                root = ET.fromstring(response.text)

                namespaces = {
                    'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
                    'sf': 'urn:partner.soap.sforce.com'
                }

                session_id_elem = root.find('.//sf:sessionId', namespaces)
                if session_id_elem is None:
                    raise Exception("Session ID not found in SOAP response")
                session_id = session_id_elem.text

                server_url_elem = root.find('.//sf:serverUrl', namespaces)
                if server_url_elem is None:
                    raise Exception("Server URL not found in SOAP response")
                server_url = server_url_elem.text

                instance_url = server_url.split('/services/')[0]

                if session_id and instance_url:
                    expiry_time = datetime.now() + timedelta(hours=23)
                    logger.info(f"SOAP login successful, session expires at: {expiry_time.isoformat()}")
                    logger.info(f"Instance URL: {instance_url}")
                    self._store_session(session_id, instance_url, expiry_time)
                    return session_id, instance_url

            elif response.status_code == 500:
                logger.warning(f"Received SOAP fault (status 500)")
                self._handle_soap_fault(response.text)

            else:
                logger.error(f"Salesforce login failed with status {response.status_code}")
                raise Exception(
                    f"Salesforce login failed with status {response.status_code}. Response: {response.text[:500]}")

        except requests.exceptions.Timeout as e:
            logger.error(f"Salesforce login request timed out: {e}")
            raise Exception(
                f"Salesforce login request timed out after 30 seconds. Check your network connection and login URL: {self.login_url}")
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Failed to connect to Salesforce: {e}")
            raise Exception(
                f"Failed to connect to Salesforce at {self.login_url}. Check your login URL and network connection. Error: {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during Salesforce login: {e}")
            raise Exception(f"Network error during Salesforce login request to {self.login_url}: {e}")
        except Exception as e:
            if "Invalid Salesforce" in str(e) or "login failed" in str(e) or "SOAP fault" in str(e):
                raise e
            else:
                logger.error(f"Unexpected error during Salesforce authentication: {e}")
                raise Exception(f"Unexpected error during Salesforce authentication: {e}")

        return None

    def _handle_soap_fault(self, response_text: str) -> None:
        error_details = f"Status 500 - Response: {response_text[:1000]}"
        try:
            root = ET.fromstring(response_text)

            fault_string = root.find('.//{http://schemas.xmlsoap.org/soap/envelope/}faultstring')
            fault_code = root.find('.//{http://schemas.xmlsoap.org/soap/envelope/}faultcode')

            if fault_string is not None:
                error_msg = fault_string.text
                fault_code_text = fault_code.text if fault_code is not None else "Unknown"

                if "INVALID_LOGIN" in error_msg:
                    logger.error(f"Invalid login credentials: {fault_code_text} - {error_msg}")
                    raise Exception(
                        f"Invalid Salesforce username, password, or security token. Fault: {fault_code_text} - {error_msg}")
                elif "INVALID_OPERATION" in error_msg:
                    logger.error(f"Invalid operation: {fault_code_text} - {error_msg}")
                    raise Exception(
                        f"Invalid operation or API access disabled. Fault: {fault_code_text} - {error_msg}")
                elif "EXCEEDED_ID_LIMIT" in error_msg:
                    logger.error(f"API limits exceeded: {fault_code_text} - {error_msg}")
                    raise Exception(f"API limits exceeded. Fault: {fault_code_text} - {error_msg}")
                else:
                    logger.error(f"SOAP fault: {fault_code_text} - {error_msg}")
                    raise Exception(f"Salesforce SOAP fault: {fault_code_text} - {error_msg}")
            else:
                logger.error("SOAP error without fault string")
                raise Exception(f"Salesforce login failed with SOAP error. {error_details}")

        except ET.ParseError as parse_error:
            logger.error(f"Failed to parse SOAP response: {parse_error}")
            raise Exception(f"Failed to parse SOAP response (XML Parse Error: {parse_error}). {error_details}")

    def _store_session(self, session_id: str, instance_url: str, expiry_time: datetime) -> None:
        try:
            logger.info("Storing Salesforce session in persistent storage")

            session_size = len(session_id.encode('utf-8'))
            instance_url_size = len(instance_url.encode('utf-8'))
            expiry_str = expiry_time.isoformat()
            expiry_size = len(expiry_str.encode('utf-8'))
            total_size = session_size + instance_url_size + expiry_size

            logger.info(
                f"Session size: {session_size} bytes, instance URL size: {instance_url_size} bytes, "
                f"expiry size: {expiry_size} bytes, total: {total_size} bytes")

            self.storage.set(self.session_key, session_id.encode('utf-8'))
            self.storage.set(self.instance_url_key, instance_url.encode('utf-8'))
            self.storage.set(self.session_expiry_key, expiry_str.encode('utf-8'))

            logger.info("Salesforce session successfully stored in persistent storage")

        except Exception as e:
            logger.warning(f"Failed to store Salesforce session in persistent storage: {e}")
            logger.info("Plugin will authenticate on each request when storage is unavailable")
            pass

    def _get_stored_session(self) -> Optional[Tuple[str, str]]:
        logger.info("Checking for stored Salesforce session")

        try:
            session_bytes = self.storage.get(self.session_key)
            if not session_bytes:
                logger.info("No stored Salesforce session found")
                return None

            session_id = session_bytes.decode('utf-8')

            instance_url_bytes = self.storage.get(self.instance_url_key)
            if not instance_url_bytes:
                logger.warning("Stored session found but no instance URL, considering invalid")
                return None

            instance_url = instance_url_bytes.decode('utf-8')

            expiry_bytes = self.storage.get(self.session_expiry_key)
            if not expiry_bytes:
                logger.warning("Stored session found but no expiry information, considering invalid")
                return None

            expiry_str = expiry_bytes.decode('utf-8')
            expiry_time = datetime.fromisoformat(expiry_str)

            current_time = datetime.now()
            if current_time + timedelta(minutes=5) < expiry_time:
                logger.info(f"Valid stored session found, expires at: {expiry_time.isoformat()}")
                return session_id, instance_url
            else:
                logger.info(f"Stored session expired at: {expiry_time.isoformat()}, cleaning up")
                self._clear_stored_session()
                return None

        except Exception as e:
            logger.warning(f"Error reading stored session: {e}")
            return None

    def _clear_stored_session(self) -> None:
        try:
            logger.info("Clearing stored Salesforce session from persistent storage")
            self.storage.delete(self.session_key)
            self.storage.delete(self.instance_url_key)
            self.storage.delete(self.session_expiry_key)
            logger.info("Successfully cleared stored Salesforce session")
        except Exception as e:
            logger.warning(f"Error clearing stored session: {e}")
            pass

    def get_valid_session(self) -> Tuple[str, str]:
        logger.info("Getting valid Salesforce session")

        session_data = self._get_stored_session()
        if session_data:
            logger.info("Using cached Salesforce session")
            return session_data

        logger.info("No valid cached session, authenticating for new session")
        session_data = self._soap_login()
        if not session_data:
            logger.error("Failed to obtain session from Salesforce")
            raise Exception("Failed to obtain session from Salesforce")

        logger.info("Successfully obtained new Salesforce session")
        return session_data

    def refresh_session(self) -> Tuple[str, str]:
        logger.info("Force refreshing Salesforce session")

        self._clear_stored_session()

        new_session = self.get_valid_session()
        logger.info("Salesforce session successfully refreshed")
        return new_session
