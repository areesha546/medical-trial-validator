"""
GUID Service for generating unique error identifiers.
Author: Areesha Anum

Uses the external UUID API (uuidtools.com) with local UUID fallback.
"""

import uuid
import logging
import requests

from app.config import GUID_API_URL

logger = logging.getLogger(__name__)


def generate_error_id() -> tuple[str, bool]:
    """
    Generate a unique error ID using the external GUID API.
    Falls back to local UUID generation if the API is unavailable.

    Returns:
        tuple: (error_id: str, used_api: bool)
    """
    try:
        response = requests.get(GUID_API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            error_id = str(data[0])
            logger.info(f"Generated error ID from API: {error_id}")
            return error_id, True
        else:
            raise ValueError("Unexpected API response format")

    except Exception as e:
        # Fallback to local UUID
        error_id = str(uuid.uuid4())
        logger.warning(f"GUID API unavailable ({str(e)}), using local fallback: {error_id}")
        return error_id, False
