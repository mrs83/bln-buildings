#!/usr/bin/env python3

import click
from app.db.session import get_db
from app.db.crud import create_user
from app.db.schemas import UserCreate
from app.db.session import SessionLocal

@click.command()
@click.option('--email', prompt="E-Mail", help='User e-mail.')
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=True)
def create_superuser(email, password) -> None:
    db = SessionLocal()
    create_user(
        db,
        UserCreate(
            email=email,
            password=password,
            is_active=True,
            is_superuser=True,
        ),
    )


if __name__ == "__main__":
    create_superuser()
