from pathlib import Path
import secrets

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import typer

from webex_assistant_skills_sdk.shared.services import CryptoService


class CryptoGenService(CryptoService):
    def generate_keys(
        self,
        directory_path: Path = Path.cwd(),
        file_name: str = 'id_rsa',
        confirm: bool = True,
    ) -> None:
        """Generate an RSA keypair"""
        
        private_key_name = f'{Path(file_name).stem}.pem'
        private_key_path = directory_path / private_key_name

        public_key_name = f'{Path(file_name).stem}.pub'
        public_key_path = directory_path / public_key_name

        should_prompt = confirm and (private_key_path.exists() or public_key_path.exists())
        if should_prompt:
            typer.confirm(
            (
                'RSA keypair already exists, would you like to overwrite '
                f'{private_key_name} and {public_key_name} in {directory_path}?'
            ),
            default=False,
            abort=True,
        )

        typer.echo('🔐 Generating new RSA keypair...')

        self._generate_keys(private_key_path, public_key_path)

        typer.echo(f'Done! {private_key_name} and {public_key_name} written to {directory_path}')

    def generate_secret(self) -> str:
        return secrets.token_urlsafe()

    def _generate_keys(
        self,
        private_key_path: Path,
        public_key_path: Path,
    ):
        private_key = rsa.generate_private_key(65537, 4096)
        public_key: rsa.RSAPublicKey = private_key.public_key()

        private_key_path.write_bytes(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

        public_key_path.write_bytes(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )
