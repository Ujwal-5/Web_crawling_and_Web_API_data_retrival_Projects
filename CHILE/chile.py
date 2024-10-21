from twocaptcha import TwoCaptcha
import os
import requests
import json

api_key = os.getenv('APIKEY_2CAPTCHA', 'your_2captcha_key')

solver = TwoCaptcha(api_key)

result = solver.recaptcha(sitekey="6Ldg2F8UAAAAABeObtL-07JwAW0bYWI_j2rgz21u",
                          url='https://www.registrodeempresasysociedades.cl/BuscarActuaciones2.aspx')

session = requests.Session()

url = "https://www.registrodeempresasysociedades.cl/BuscarActuaciones2.aspx/Busqueda"

payload = json.dumps({
  "Response": result['code'],
  "texto": "2024-03-01",
  "tipoBusqueda": "6",
  "tipoRegistro": "1"
})
headers = {
  'Content-Type': 'application/json',
#   'Cookie': 'ASP.NET_SessionId=55fnttcq3ug4wbuu02ip2300'
}

response = session.post(url, headers=headers, data=payload)

link_json = response.json()
link_json["d"]
data = json.loads(link_json["d"])
link = data["Link"]

url2 = 'https://www.registrodeempresasysociedades.cl/Busqueda/ActuacionDetalle.aspx/DatosActuaciones'
registration_date = "01-03-2024"
payload2 = json.dumps({
  "ParamBusqueda1": registration_date,
  "codehash": link.split('=')[-1],
  "tipoBusqueda": "6"
  })

response2 = session.post(url2, headers=headers, data=payload2)

print(response2.json())
