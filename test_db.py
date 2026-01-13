import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
from alembic import command
from alembic.config import Config

TEST_DB_URL = "postgresql+asyncpg://postgres:password@localhost/project_test_db"

alembic_cfg = Config("alembic.ini")
alembic_cfg.set_main_option("sqlalchemy.url", TEST_DB_URL)
    

def reset_test_db():
    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")
