from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from . import schemas, security, dependencies

app = FastAPI(title="Auth Service", description="Handles Authentication & RBAC")

# Mock Database for testing
fake_users_db = {
    "customer_bob": {
        "username": "customer_bob",
        "password_hash": security.get_password_hash("bob123"),
        "role": "customer"
    },
    "admin_alice": {
        "username": "admin_alice",
        "password_hash": security.get_password_hash("admin123"),
        "role": "admin"
    }
}

@app.post("/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not security.verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Create JWT token embedding the user's role for RBAC
    access_token = security.create_access_token(
        data={"sub": user["username"], "role": user["role"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- PROTECTED ROUTES ---

@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(dependencies.get_current_user)):
    """Any logged-in user can access this."""
    return {"message": "You are authenticated!", "user": current_user}

@app.get("/admin/dashboard")
async def read_admin_data(current_user: dict = Depends(dependencies.require_role("admin"))):
    """ONLY users with the 'admin' role can access this (RBAC)."""
    return {"message": "Welcome to the secure admin dashboard!", "admin_user": current_user["username"]}