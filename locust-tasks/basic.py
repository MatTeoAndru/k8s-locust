from locust import FastHttpUser, TaskSet, task, between ,constant, events


#https://servizipasshub.passstage.cloud

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



