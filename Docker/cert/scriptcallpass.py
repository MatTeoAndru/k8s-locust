import requests
import json

endpoint_url = "https://idp.passcom.local/token/jwt"
cert_key_path = "./1919006000.key"
cert_path = "./1919006000.pem"
ca_cert_path = "./ca-staging.pem"
passhub_url = "https://servizipasshub.passstage.cloud/v1/1919006000/totali"

data = {
    "grant_type": "client_credentials",
    "scope": "sdi"
}

# Get Token JWT
try:
    response = requests.post(
        endpoint_url,
        data=data,
        cert=(cert_path, cert_key_path),
        verify=ca_cert_path
    )

    if response.status_code == 200:
        print("Request for JWT TOKEN was successful, Status Code 200. Response content:")
        print(response.text)

        response_data = json.loads(response.text)
        jwt_token = response_data["access_token"]

        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }

        # Save JWT token to a text file
        with open("jwt_token.txt", "w") as file:
            file.write(jwt_token)
        print("JWT token has been saved to jwt_token.txt")

        # Passhub get
        try:
            response = requests.get(passhub_url, headers=headers)
            if response.status_code == 200:
                print("Request for passhub was successful, Status Code 200. Response content:")
                print(response.text)
            else:
                print(f"Request failed with status code {response.status_code}")
                print(response.text)
        except requests.exceptions.RequestException as e:
            print(f"Request failed with error: {e}")

    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
except requests.exceptions.RequestException as e:
    print(f"Request failed with error: {e}")
