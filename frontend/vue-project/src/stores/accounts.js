import axios from 'axios'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { googleTokenLogin } from 'vue3-google-login'
import { useRouter } from 'vue-router'

export const useAccountStore = defineStore('account', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const router = useRouter()

  const token = ref({
    access: localStorage.getItem('access') || null,
    refresh: localStorage.getItem('refresh') || null,
  })

  const signUp = function (payload) {
    const { first_name, last_name, birth_date, email, password } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: { first_name, last_name, birth_date, email, password }
    })
      .then(() => {
        console.log('회원가입 완료')
      })
      .catch(err => {
        console.log(err.response?.data || err.message)
      })
  }

  const logIn = function (payload) {
    const { email, password } = payload

    return axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: { email, password }
    })
      .then(res => {
        console.log('로그인 완료')
        setToken(res.data.access, res.data.refresh)
        return { access: res.data.access, refresh: res.data.refresh }
      })
      .catch(err => {
        console.log(err.response?.data || err.message)
      })
  }

  const logout = async function () {  
    try {
      const access = token.value.access || localStorage.getItem('access')
      const refresh = token.value.refresh || localStorage.getItem('refresh')
     
      if (!access || !refresh || typeof access !== 'string' || typeof refresh !== 'string') {
      throw new Error('access 또는 refresh 토큰이 문자열 형식이 아님')
      }

      await axios.post(`${API_URL}/accounts/logout/`, { refresh },
        {
          headers: {
            Authorization: `Bearer ${access}`,
          }
        }
      )

      clearToken()
      router.push({ name: 'LogInView' })
      console.log('로그아웃 성공')
    } catch (err) {
      console.error('로그아웃 실패:', err.response?.data || err.message)
    }
  }

  const setToken = function (access, refresh) {
    token.value.access = access
    token.value.refresh = refresh
    localStorage.setItem('access', access)
    localStorage.setItem('refresh', refresh)
    axios.defaults.headers.common['Authorization'] = `Bearer ${access}`
  }

  const clearToken = function () {
    token.value.access = null
    token.value.refresh = null
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
  }

  const loadTokenFromStorage = function () {
    token.value.access = localStorage.getItem('access')
    token.value.refresh = localStorage.getItem('refresh')
  }

  const isLogin = computed(() => {
    return !!token.value.refresh
  })

const googleLogin = async function (birth_date = '1999-01-01') {
  try {
    const { access_token } = await googleTokenLogin()

    const res = await axios.post(`${API_URL}/accounts/signup/google/`, {
      access_token,
      birth_date,
    })

    setToken(res.data.access, res.data.refresh)
    console.log('구글 로그인 성공:', res.data)
    router.push({ name: 'mainView' })

  } catch (err) {
    console.error('구글 로그인 실패:', err.response?.data || err.message)
    alert('구글 로그인 중 오류가 발생했습니다.')
  }
}

  return { API_URL, signUp, logIn, logout, setToken, clearToken, loadTokenFromStorage, token, isLogin, googleLogin }
})
