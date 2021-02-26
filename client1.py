from flask import Flask, redirect,request,render_template
import time
import requests


app=Flask(__name__)


#point d'entrée de l'application, permet uniquement de s'authentifier
@app.route('/')
def hello():
        return(render_template("bouton.html"))



#déclenché quand on appuie sur le bouton, redirige vers keycloak
@app.route('/redirectTest')
def redirection():
        authz_endpoint_url = 'http://localhost:8080/auth/realms/test/protocol/openid-connect/auth'
        scope = 'openid%20profile'
        response_type = 'code'
        client_id = 'client1'
        redirect_uri = 'http%3A%2F%2Flocalhost:5000%2Fcallback'
        url_tot = authz_endpoint_url + '?response_type=' + response_type + '&scope=' + scope + '&client_id=' + client_id + '&redirect_uri=' + redirect_uri
        return(redirect(url_tot,302))

#on revient à cette url de callback après avoir passé keycloak avec succès, on y récupère le code dans le corps de la requete get

@app.route('/callback', methods=["GET","POST"])
def callback():
        #on a deux cas: le retour lors de la demande de code, et le retour lors de la demande de token
        session_state = request.args.get('session_state')
        code = request.args.get('code')
        if code: #on a reçu une requete get avec notre code
                url_token = "http://localhost:8080/auth/realms/test/protocol/openid-connect/token"
                params = {"url_token":"http://localhost:8080/auth/realms/test/protocol/openid-connect/token","grant_type":"authorization_code", "code":code, "client_auth_method":"none","client_id":"client1","redirect_uri":"http://localhost:5000/callback"}
                #on envoie alors une requete post, 
                reponse = requests.post(url_token,params)
                JSONrecu=reponse.json()
                accessToken=JSONrecu["access_token"]
                userinfo=requests.get("http://localhost:8080/auth/realms/test/protocol/openid-connect/userinfo",headers={"Authorization":["Bearer",str(accessToken)]})
                return(userinfo.text)  #on affiche le json reçu



        else:#qqn visite l'url pour le fun
                return("vous n'avez rien à faire ici")
