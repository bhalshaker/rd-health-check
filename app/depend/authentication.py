from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
import os

http_bearer = HTTPBearer()

class Auth:
    """
    A class to handle authentication-related tasks.
    """

    @staticmethod
    def get_admin_key() -> str:
        """Get the admin key from environment variables."""
        return os.getenv('ADMIN_KEY', 'rd-healthcheck')
    
    @staticmethod
    def is_admin(token: HTTPAuthorizationCredentials = Depends(http_bearer)):
        """
        Dependency to check if the user is an admin.
        Raises HTTPException if the user is not an admin.
        """
        # Check if the provided token matches the admin key
        if token.credentials != Auth.get_admin_key():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        return True