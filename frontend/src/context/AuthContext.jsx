import { useState, useEffect, createContext } from 'react'
import { setToken, getToken, removeToken } from '../api/token'
import { useUser } from '../hooks/useUser'

export const AuthContext = createContext({
  auth: undefined,
  login: () => null,
  logout: () => null,
})

export function AuthProvider({ children }) {
  const [auth, setAuth] = useState(undefined)
  const { getMe } = useUser()

  useEffect(() => {
    const token = getToken()
    if (!token) {
      setAuth(null)
    } else {
      login(token)
    }
  }, [])

  const login = async (token) => {
    setToken(token)
    const me = await getMe(token)
    setAuth({ token, me })
  }

  const logout = () => {
    setAuth(null)
    setToken(null)
    removeToken()
  }

  const valueContext = {
    auth,
    login,
    logout,
  }

  return (
    <AuthContext.Provider value={valueContext}>{children}</AuthContext.Provider>
  )
}
