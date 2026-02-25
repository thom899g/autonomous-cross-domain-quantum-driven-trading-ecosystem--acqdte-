"""
Firebase Manager for ACQDTE
Handles all Firebase Firestore interactions with robust error handling
"""

import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from google.cloud import firestore
from google.cloud.firestore_v1 import Client
from google.oauth2 import service_account
from loguru import logger
import traceback

class FirebaseManager:
    """Manages Firebase Firestore connections and operations"""
    
    def __init