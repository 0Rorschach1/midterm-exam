"""CLI commands for managing the URL shortener."""
import click
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.repositories.url_repository import URLRepository
from app.services.url_service import URLService


@click.group()
def cli():
    """URL Shortener CLI."""
    pass


@cli.command()
def cleanup_expired():
    """Delete all expired URLs based on TTL setting."""
    db: Session = SessionLocal()
    try:
        repository = URLRepository(db)
        service = URLService(repository)
        count = service.cleanup_expired_urls()
        click.echo(f"Successfully deleted {count} expired URL(s)")
    except Exception as e:
        click.echo(f"Error cleaning up expired URLs: {str(e)}", err=True)
    finally:
        db.close()


if __name__ == "__main__":
    cli()
