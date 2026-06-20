import os
import requests

LAMATOK_API_KEY = os.environ.get("LAMATOK_API_KEY")

def check_credentials(email: str, password: str) -> dict:
    """
    Verifies TikTok credentials via the Lamatok API.
    
    Note: Lamatok uses usernames, not emails.
    For demonstration, we're using the email as the username.
    """
    
    if not LAMATOK_API_KEY:
        return {
            "success": False,
            "status": "config_error",
            "message": "Lamatok API key not configured. Please add LAMATOK_API_KEY to environment variables."
        }

    # Lamatok endpoint to get user info by username
    lamatok_url = "https://api.lamatok.com/v1/user/by/username"

    headers = {
        "x-access-key": LAMATOK_API_KEY,
        "Content-Type": "application/json",
    }
    
    # Using email as username (Lamatok uses username, not email)
    # If you have a username, use that instead
    params = {"username": email}

    try:
        response = requests.get(
            lamatok_url,
            headers=headers,
            params=params,
            timeout=20
        )
        
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            
            # Check if user data exists
            if data and data.get("data"):
                user_data = data.get("data")
                return {
                    "success": True,
                    "status": "valid",
                    "message": "Credentials are valid",
                    "account": {
                        "username": user_data.get("username", ""),
                        "nickname": user_data.get("nickname", ""),
                        "followers": user_data.get("follower_count", 0),
                        "following": user_data.get("following_count", 0),
                        "is_verified": user_data.get("verified", False),
                    }
                }
            else:
                return {
                    "success": False,
                    "status": "user_not_found",
                    "message": "User not found. Please check the username.",
                }
        elif response.status_code == 401:
            return {
                "success": False,
                "status": "auth_error",
                "message": "Invalid Lamatok API key. Please check your configuration.",
            }
        elif response.status_code == 404:
            return {
                "success": False,
                "status": "user_not_found",
                "message": "User not found on TikTok.",
            }
        else:
            return {
                "success": False,
                "status": "api_error",
                "message": f"Lamatok API error: {response.status_code}",
            }
            
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "status": "timeout",
            "message": "Request timed out. Please try again.",
        }
    except Exception as e:
        return {
            "success": False,
            "status": "error",
            "message": f"Error: {str(e)}",
        }
