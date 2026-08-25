import requests

# URL base que devuelve los datos recibidos
BASE_URL = "https://httpbin.org"

# Encabezados personalizados de prueba
custom_headers = {
    "User-Agent": "MiPruebaPython/1.0",
    "Authorization": "Bearer TOKEN_DE_PRUEBA_123",
    "Content-Type": "application/json",
    "X-Custom-Header": "ValorEspecial"
}

# Datos para los métodos que envían información en el cuerpo (body)
payload = {
    "nombre": "Ejemplo",
    "estado": "Activo"
}

def probar_metodo(metodo, url, headers=None, json_data=None):
    print(f"\n{'='*15} Probando {metodo} {'='*15}")
    try:
        response = requests.request(
            method=metodo,
            url=url,
            headers=headers,
            json=json_data
        )
        print(f"Código de estado: {response.status_code}")
        
        # httpbin devuelve en la clave 'headers' los encabezados que recibió
        data = response.json()
        print("Encabezados recibidos por el servidor:")
        for clave, valor in data.get("headers", {}).items():
            print(f"  {clave}: {valor}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la petición: {e}")

# 1. GET
probar_metodo("GET", f"{BASE_URL}/get", headers=custom_headers)

# 2. POST
probar_metodo("POST", f"{BASE_URL}/post", headers=custom_headers, json_data=payload)

# 3. PUT
probar_metodo("PUT", f"{BASE_URL}/put", headers=custom_headers, json_data=payload)

# 4. PATCH
probar_metodo("PATCH", f"{BASE_URL}/patch", headers=custom_headers, json_data={"estado": "Inactivo"})

# 5. DELETE
probar_metodo("DELETE", f"{BASE_URL}/delete", headers=custom_headers)
