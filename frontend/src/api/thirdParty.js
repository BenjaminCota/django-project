const DOG_API_URL = 'https://dog.ceo/api/breeds/image/random'

export async function getRandomDogApi() {
  const response = await fetch(DOG_API_URL)

  if (!response.ok) {
    throw new Error('No se pudo obtener la imagen')
  }

  return await response.json()
}
