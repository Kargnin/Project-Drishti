import os
from dotenv import load_dotenv

load_dotenv()

# Google Cloud Configuration
PROJECT_ID = os.environ.get('PROJECT_ID', 'noted-throne-466513-v6')
LOCATION = os.environ.get('LOCATION', 'us-central1')

# App Configuration
APP_ID = os.environ.get('APP_ID', 'default-app-id')

# Security Agent Configuration
SECURITY_AGENT_ID = 'security_agent'
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB max image size
SUPPORTED_IMAGE_FORMATS = ['image/jpeg', 'image/png', 'image/webp', 'image/bmp', 'image/gif']

# Threat Level Configuration
THREAT_LEVELS = {
    'low': {
        'score_range': (0, 3),
        'response_time': '30 minutes',
        'escalation_required': False
    },
    'medium': {
        'score_range': (4, 7), 
        'response_time': '10 minutes',
        'escalation_required': True
    },
    'high': {
        'score_range': (8, 10),
        'response_time': 'immediate',
        'escalation_required': True
    }
}

# Security Keywords for threat detection
SECURITY_KEYWORDS = {
    'high_risk': [
        'weapon', 'knife', 'gun', 'firearm', 'explosive', 'bomb', 'threat', 'violence',
        'attack', 'assault', 'robbery', 'theft', 'vandalism', 'fire', 'emergency',
        'panic', 'stampede', 'terrorism', 'suspicious package'
    ],
    'medium_risk': [
        'unauthorized', 'trespassing', 'suspicious', 'loitering', 'harassment',
        'disturbance', 'altercation', 'argument', 'crowd control', 'breach',
        'lockdown', 'evacuation', 'medical emergency'
    ],
    'low_risk': [
        'lost', 'found', 'noise complaint', 'minor injury', 'lost item',
        'information request', 'general assistance', 'crowd density'
    ]
} 