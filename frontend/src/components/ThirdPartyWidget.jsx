import { useEffect, useState } from 'react'
import { Button, Card, Loader } from 'semantic-ui-react'
import { getRandomDogApi } from '../api/thirdParty'

export function ThirdPartyWidget() {
  const [imageUrl, setImageUrl] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchDog = async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await getRandomDogApi()
      setImageUrl(result.message)
    } catch (err) {
      setError('No se pudo cargar la imagen de la API de terceros')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchDog()
  }, [])

  return (
    <Card className="third-party-widget">
      <Card.Content>
        <Card.Header>API de terceros: Dog CEO</Card.Header>
        <Card.Meta>Imagen aleatoria de un perro (dog.ceo)</Card.Meta>
      </Card.Content>
      <Card.Content>
        {loading && <Loader active inline="centered">Cargando...</Loader>}
        {error && <p className="third-party-widget__error">{error}</p>}
        {!loading && !error && imageUrl && (
          <img className="third-party-widget__image" src={imageUrl} alt="Perro aleatorio" />
        )}
      </Card.Content>
      <Card.Content extra>
        <Button primary fluid onClick={fetchDog} loading={loading}>
          Nueva imagen
        </Button>
      </Card.Content>
    </Card>
  )
}
