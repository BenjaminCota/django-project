const API_URL = import.meta.env.VITE_BASE_API_URL

export async function loginApi(formData) {
  try {
    const url = `${API_URL}/api/v1/auth/token/`
    const params = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    }

    const response = await fetch(url, params)

    if (response.status !== 200) {
      throw new Error('Usuario o contraseña incorrecta')
    }

    return await response.json()
  } catch (error) {
    throw new Error(error.message || 'Error al iniciar sesión')
  }
}

export async function registerApi(formData) {
  try {
    const url = `${API_URL}/api/v1/auth/register/`
    const params = {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    }

    const response = await fetch(url, params)
    const result = await response.json()

    if (response.status !== 201) {
      const detalle = Object.values(result).flat().join(' ')
      throw new Error(detalle || 'No se pudo crear el usuario')
    }

    return result
  } catch (error) {
    throw new Error(error.message || 'No se pudo crear el usuario')
  }
}

export async function getMeApi(token) {
  const url = `${API_URL}/api/v1/auth/me/`
  const params = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }

  const response = await fetch(url, params)
  return await response.json()
}
