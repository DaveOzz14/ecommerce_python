import jwt
import time

APP_ID = 2657639            # <-- TU APP ID (int)
PRIVATE_KEY_PATH = "C:\\Users\\david\\Downloads\\grafana-assistant-otel-s.2026-01-14.private-key.pem"

with open(PRIVATE_KEY_PATH, "r") as f:
    private_key = f.read()

payload = {
    "iat": int(time.time()) - 60,
    "exp": int(time.time()) + 540,
    "iss": APP_ID
}

encoded_jwt = jwt.encode(payload, private_key, algorithm="RS256")
print(encoded_jwt)


# eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3Njg0MTMzNTMsImV4cCI6MTc2ODQxMzk1MywiaXNzIjoyNjU3NjM5fQ.jRlFE0fgObnFRNiPLSPkVeKAPAjClqylZyqapOOKtCsMTUBnoKS9JPb2jlkE1uyd_u3U5w-ofQQkI-BNn1JWir4AW0668semt4P-1sSlLeet9QQrRyG7EhuH45EEXZ7ZDtCu6WflLa4s23R8ja-G4ARFwbLYlaOfyty7COOuJWJGGYFw83YJJiQHIATNWZFGOFT2rEdak3HvtzaGzGzssOFXNCRdVEeO-zsLaADSM1li5xZ9-JtT_TZbCAjh9_pgW03KpOG7PQ6XNNjyZ7yGnGD1K0Xqdpvj6d3ekYbFP9XQ5P3SOddxJoUQhEzzNHDIEaBn14z7tMX-kSDG5FtNdw