from locust import FastHttpUser, TaskSet, task, between ,constant, events , SequentialTaskSet ,HttpUser , LoadTestShape
from locust.runners import MasterRunner 
import requests , json , logging , math

idinstallazione = "1919006000"
endpoint_url = "https://idp.passcom.local/token/jwt"
cert_key_path = "./1919006000.key"
cert_path = "./1919006000.pem"
ca_cert_path = "./ca-staging.pem"


def get_jwt_token(endpoint_url, cert_key_path, cert_path, ca_cert_path):
    data = {"grant_type": "client_credentials", "scope": "sdi"}

    try:
        response = requests.post(
            endpoint_url,
            data=data,
            cert=(cert_path, cert_key_path),
            verify=ca_cert_path
        )

        response.raise_for_status()  

        response_data = response.json()
        jwt_token = response_data["access_token"]
        return jwt_token

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to get JWT token: {e}")
        return None

def save_jwt_token_to_file(jwt_token, file_path="jwt_token.txt"):
    with open(file_path, "w") as file:
        file.write(jwt_token)
    logging.info(f"JWT token has been saved to {file_path}")


# @events.init.add_listener
# def on_locust_init(environment, **kw):
#     @environment.web_ui.app.route("/added_page")
#     def my_added_page():
#         return "Another page"


@events.test_start.add_listener
def on_locust_init(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        logging.info("I'm on the master node")
    
    else:
        logging.info("I'm on a worker or standalone node")

    jwt_token = get_jwt_token(endpoint_url, cert_key_path, cert_path, ca_cert_path)

    if jwt_token:
        save_jwt_token_to_file(jwt_token)

##

@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--my-argument",  type=str, env_var="LOCUST_MY_ARGUMENT", default="1919006000", help="Id Installazione")
    parser.add_argument("--env", choices=["stage", "prod"], default="stage", help="Environment")



@events.test_start.add_listener
def _(environment, **kw):
    print(f"Args Id: {environment.parsed_options.my_argument}")
    print(f"Args Env: {environment.parsed_options.env}")


##
class MyUserGet(TaskSet):
    @task
    def get_fatture(self):
        file_path = "jwt_token.txt"
        with open(file_path, "r") as file:
            line = file.readline()

        jwt_token = line.strip() 

        
        headersGet = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"  # Adjust the content type as needed
        }
        url = f"/v1/{idinstallazione}/totali"
        response = self.client.get(url, headers=headersGet)
        if  response.status_code == 200:
            print("Richiesta GET fatture riuscita!")
        else:
            print(f"Errore nella richiesta GET fatture. Codice di stato: {response.status_code}")
            print(response.text)

    @task
    def get_datiTrasmittente(self):

        file_path = "jwt_token.txt"  
        with open(file_path, "r") as file:
            line = file.readline()

        jwt_token = line.strip() 

        headersGet = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"  # Adjust the content type as needed
        }
        url = f"/v1/{idinstallazione}/DatiTrasmittente"
        response = self.client.get(url, headers=headersGet)
        if response.status_code == 200:
            print("Richiesta GET dati riuscita!")
        else:
            print(f"Errore nella richiesta GET dati. Codice di stato: {response.status_code}")
            print(response.text)


class MyUserPost(TaskSet):
    @task
    def postCreazioneAzienda(self):
        file_path = "jwt_token.txt"
        with open(file_path, "r") as file:
            line = file.readline()

        jwt_token = line.strip() 

        
        headersPost = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "text/xml" 
        }
        url = f"/v1/{idinstallazione}/aziende?oneCompanyPerUser=true&sovrascrivi=true"
        
        xml_file_path = "./xml/postCreazioneAzienda.xml"  
        with open(xml_file_path, "r") as xml_file:
            xml_content = xml_file.read()


        response = self.client.post(url, headers=headersPost , data = xml_content)

        if response.status_code == 200:
            print("Richiesta POST riuscita!")
        else:
            print(f"Errore nella richiesta POST. Codice di stato: {response.status_code}")
            print(response.text)


class GetDatiTrasmittenteANDFatture(FastHttpUser):  
    tasks = [MyUserGet]
    wait_time = constant(0.5)  


class PostCreazioneAziendaAND(FastHttpUser):  
    tasks = [MyUserPost]
    wait_time = constant(1.0)  



#SEQUENCE TASK

# class TaskSequenziali(FastHttpUser):    
#     @task
#     class SequenceOfTasks(SequentialTaskSet):
#         wait_time = between(1, 5)
#         @task
#         def mainPage(self):
#             self.client.get("/")
#             self.client.get("https://api.demoblaze.com/entries")
#         @task
#         def login(self):
#             self.client.options("https://api.demoblaze.com/login")
#             self.client.post("https://api.demoblaze.com/login",json={"username":"aaaa","password":"YWFhYQ=="})
#             self.client.options("https://api.demoblaze.com/check")
#             self.client.get("https://api.demoblaze.com/entries")
#             self.client.post("https://api.demoblaze.com/check",json={"token":"YWFhYTE2MzA5NDU="})            



#Class to call api without jwt token, to test that response is 504 and is not giving any problem to the service


class MyTaskSet(TaskSet):

    @task
    def my_task(self):
        # Access command-line arguments using self.environment.options
        arg_id_install = self.environment.options.my_argument
        env_value = self.environment.options.env
        #invisible_argument_value = self.environment.options.my_ui_invisible_argument

        # Now you can use these values in your task logic
        print(f"Id Installazione: {arg_id_install}")
        print(f"Environment: {env_value}")
        #print(f"Invisible Argument: {invisible_argument_value}")

# class MyLocust(FastHttpUser):
#     task_set = MyTaskSet
#     wait_time = between(1, 3)



class DoubleWaveUserSpawn600s(LoadTestShape):
    """
    A shape to imitate some specific user behaviour. In this example, midday
    and evening meal times. First peak of users appear at time_limit/3 and
    second peak appears at 2*time_limit/3

    Settings:
        min_users -- minimum users
        peak_one_users -- users in first peak
        peak_two_users -- users in second peak
        time_limit -- total length of test
    """

    min_users = 20
    peak_one_users = 140
    peak_two_users = 70
    time_limit = 600

    def tick(self):
        run_time = round(self.get_run_time())

        if run_time < self.time_limit:
            user_count = (
                (self.peak_one_users - self.min_users)
                * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 5) ** 2) + (self.peak_two_users - self.min_users)
                * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 10) ** 2) + self.min_users
            )
            return (round(user_count), round(user_count))
        else:
            return None
        


class StagesShape(LoadTestShape):
    stages = [
        {"duration": 60, "users": 10}, 
        {"duration": 100, "users": 50}, 
        {"duration": 180, "users": 100}, 
        {"duration": 220, "users": 30}, 
        {"duration": 240, "users": 10}, 
        {"duration": 260, "users": 1} 
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                # arbitrary high spawn rate to get to users as quickly as possible
                tick_data = (stage["users"], 100) 
                return tick_data

        return None
    


class MyCustomShape(LoadTestShape):
    step_time = 30 
    step_load = 10 
    spawn_rate = 10 
    time_limit = 600

    def tick(self):
        run_time = self.get_run_time()


        if run_time > self.time_limit:
            return None

        current_step = math.floor(run_time / self.step_time) + 1
        return (current_step * self.step_load, self.spawn_rate)