import { Button } from 'semantic-ui-react'
import { useAuth } from '../../hooks/useAuth'
import { ThirdPartyWidget } from '../../components/ThirdPartyWidget'

export function Dashboard() {
  const { logout, auth } = useAuth()
  const user = auth.me

  return (
    <div className="dashboard">
      <div className="dashboard__header">
        <h1>Dashboard</h1>
        <h3>Bienvenido {user.username} ({user.email})</h3>
        <Button type="button" content="Cerrar Sesión" onClick={logout} />
      </div>

      <div className="dashboard__widgets">
        <ThirdPartyWidget />
      </div>
    </div>
  )
}
