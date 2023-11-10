from locust import FastHttpUser, TaskSet, task, between ,constant, events
import requests , json


#https://servizipasshub.passstage.cloud



if __name__ == "__main__":

    endpoint_url = "https://idp.passcom.local/token/jwt"
    cert_key_path = "../cert/1919006000.key"
    cert_path = "../cert//1919006000.pem"
    ca_cert_path = "../cert/ca-staging.pem"
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
            with open("../cert/jwt_token.txt", "w") as file:
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

    
idinstallazione = "1919006000"


class MyUser(TaskSet):

    @task
    def get_fatture(self):

        file_path = "../cert/jwt_token.txt"  
        with open(file_path, "r") as file:
            line = file.readline()

        jwt_token = line.strip() 

        
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"  # Adjust the content type as needed
        }
        url = f"/v1/{idinstallazione}/totali"
        self.client.get(url, headers=headers)



class MyLocust(FastHttpUser):  # Update 'Locust' to 'HttpUser'
    tasks = [MyUser]
    wait_time = constant(0.5)  



