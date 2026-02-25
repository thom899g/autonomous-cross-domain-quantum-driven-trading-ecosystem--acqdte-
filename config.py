"""
ACQDTE Configuration Management
Centralized configuration with environment variables and validation
"""

import os
from typing import Dict, Any, Optional
from pydantic import BaseSettings, Field, validator
from dataclasses import dataclass
from enum import Enum
import logging
from loguru import logger

class TradingMode(str, Enum):
    PAPER = "paper"
    LIVE = "live"
    BACKTEST = "backtest"

class QuantumAlgorithm(str, Enum):
    QAOA = "qaoa"
    VQE = "vqe"
    QUANTUM_ANNEALING = "quantum_annealing"

class Settings(BaseSettings):
    # Firebase Configuration
    FIREBASE_CREDENTIALS_PATH: str = Field(
        default="config/firebase-credentials.json",
        description="Path to Firebase service account credentials"
    )
    FIRESTORE_DATABASE: str = Field(
        default="(default)",
        description="Firestore database name"
    )
    
    # Trading Configuration
    TRADING_MODE: TradingMode = Field(
        default=TradingMode.PAPER,
        description="Trading mode: paper, live, or backtest"
    )
    DEFAULT_EXCHANGE: str = Field(
        default="binance",
        description="Default cryptocurrency exchange"
    )
    SYMBOLS: list = Field(
        default=["BTC/USDT", "ETH/USDT", "SOL/USDT"],
        description="Trading symbols"
    )
    
    # Quantum Configuration
    QUANTUM_ALGORITHM: QuantumAlgorithm = Field(
        default=QuantumAlgorithm.QAOA,
        description="Quantum-inspired algorithm to use"
    )
    QUANTUM_ITERATIONS: int = Field(
        default=1000,
        ge=100,
        le=10000,
        description="Number of quantum optimization iterations"
    )
    
    # RL Configuration
    RL_EPOCHS: int = Field(
        default=10000,
        ge=1000,
        description="Reinforcement learning training epochs"
    )
    NEUROEVOLUTION_POPULATION: int = Field(
        default=50,
        ge=10,
        le=500,
        description="Neuroevolution population size"
    )
    
    # Risk Management
    MAX_POSITION_SIZE: float = Field(
        default=0.1,
        ge=0.01,
        le=0.5,
        description="Maximum position size as fraction of capital"
    )
    STOP_LOSS_PERCENT: float = Field(
        default=0.02,
        ge=0.005,
        le=0.1,
        description="Stop loss percentage"
    )
    
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN: Optional[str] = Field(
        default=None,
        description="Telegram bot token for emergency alerts"
    )
    TELEGRAM_CHAT_ID: Optional[str] = Field(
        default=None,
        description="Telegram chat ID for notifications"
    )
    
    # System Configuration
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level"
    )
    HEARTBEAT_INTERVAL: int = Field(
        default=60,
        description="Heartbeat interval in seconds"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    @validator("SYMBOLS", pre=True)
    def parse_symbols(cls, v):
        if isinstance(v, str):
            return [s.strip() for s in v.split(",")]
        return v

# Global settings instance
settings = Settings()

# Configure logging
logger.remove()
logger.add(
    "logs/acqdte_{time:YYYY-MM-DD}.log",
    level=settings.LOG_LEVEL,
    rotation="500 MB",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} - {message}"
)
logger.add(
    sys.stdout,
    level=settings.LOG_LEVEL,
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}"
)