<template>
  <div v-if="showBirthDateForm">
   <div class="modal-overlay"></div>
   <div class="modal-container">
      <div class="modal-title">소셜 로그인 진행중...</div>
    <div class="modal-subtitle">더 나은 서비스 제공을 위해 생년월일 입력이 필요해요.</div>

    <label class="modal-label" for="birth-date">생년월일</label>        
    <input
      id="birth-date"
      class="modal-input"
      type="date"
      v-model="birthDate"
    />

    <div class="modal-button-group">
      <button class="modal-button cancel" @click="cancelModal">취소</button>
        <button class="modal-button confirm" @click="submitProfileUpdate">가입하기</button>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

const route = useRoute()
const router = useRouter()
const accountStore = useAccountStore()
const API_BASE = import.meta.env.VITE_API_BASE_URL
const accessToken   = ref('')
const birthDate     = ref('1999-01-01')
const showBirthDateForm = ref(false)

const cancelModal = () => {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')

  accountStore.setToken(null, null)

  router.push({ name: 'LogInView' })
}

// 1) 콜백에서 code를 받아 토큰 교환 & 백엔드 로그인/가입 요청
onMounted(async () => {
  const code = route.query.code
  if (!code) {
    alert('인가 코드가 없습니다.')
    return router.replace({ name: 'LogInView' })
  }

  try {
    // 1-1) 카카오 토큰 교환
    const tokenRes = await axios.post(
      'https://kauth.kakao.com/oauth/token',
      new URLSearchParams({
        grant_type:   'authorization_code',
        client_id:    import.meta.env.VITE_APP_KAKAO_CLIENT_ID,
        redirect_uri: 'http://localhost:5173/accounts/kakao/login/callback/',
        code,
      }),
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
    )
    accessToken.value = tokenRes.data.access_token

    // 1-2) 백엔드에 카카오 토큰 전달
    const res = await axios.post(
      `${API_BASE}/accounts/signup/kakao/`,
      { access_token: accessToken.value }
    )

    // 2) 생년월일 추가 입력
    if (res.data.status === 'need_birth_date') {
      showBirthDateForm.value = true
      accessToken.value = res.data.access_token
      return
    }

    // 3) 정상 로그인/가입 완료
    if (res.data.status === 'logged_in' || res.data.status === 'created' || res.data.status === 'linked') {
      localStorage.setItem('access', res.data.access)
      localStorage.setItem('refresh', res.data.refresh)
      accountStore.setToken(res.data.access, res.data.refresh)
      
      console.log({
        'logged_in': '로그인 성공!',
        'created': '회원가입 및 로그인 성공!',
        'linked': '카카오 계정 연결 및 로그인 성공!'
      }[res.data.status])
      
      router.replace({ name: 'HomeView' })
    }

  } catch (err) {
    console.error('Kakao callback error:', err.response?.data || err)
    alert('카카오 로그인 처리 중 오류가 발생했습니다.')
    router.replace({ name: 'LogInView' })
  }
})

// 4) need_birth_date 처리 후 폼 전송
async function submitProfileUpdate() {

  try {
    const updateRes = await axios.post(
      `${API_BASE}/accounts/profile/update/`,
      {
        access_token: accessToken.value,
        birth_date:   birthDate.value,
      }
    )

    localStorage.setItem('access_token', updateRes.data.access)
    localStorage.setItem('refresh_token', updateRes.data.refresh)
    accountStore.setToken(updateRes.data.access, updateRes.data.refresh)
    console.log('Kakao signup response:', updateRes.data)

    router.replace({ name: 'HomeView' })

  } catch (err) {
    console.error('Profile update error:', err.response?.data || err)
    alert(err.response?.data?.detail |'프로필 업데이트 중 오류가 발생했습니다.')
  }
}
</script>

<style scoped>
.modal-overlay{
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(129, 139, 126, 0.5);
  z-index: 999;
}

.modal-container{
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 400px;
  height: 300px;
  background-color: #ffffff;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  z-index: 1000;

  display: flex;
  flex-direction: column;
  text-align: center;
}

.modal-title{
  font-size: 24px;
  font-weight: 500;
  color: #000000;
  line-height: 1.2;
  margin-bottom: 12px;
  padding: 0;
}

.modal-subtitle{
  font-size: 14px;
  font-weight: 300;
  color: #818B7E;
  margin-top: 0px;
  padding-top: 0px;
  margin-bottom: 52px;
}

.modal-label{
  font-size: 14px;
  color: #454E42;
  text-align: left;
  margin-bottom: 4px;
}

.modal-input{
  border: 1px solid #454E42;
  width: 100%;
  height: 56px;
  padding: 0 12px;
  border-radius: 12px;
  font-size: 14px;
  color: #454E42;
  box-sizing: border-box;
  margin-bottom: 52px;
}

.modal-button-group{
  display: flex;
  justify-content: center;
  gap: 32px;
  margin-top: 12px;
}

.modal-button {
  padding: 12px 0;
  width: 140px;
  height: 52px;
  font-size: 18px;
  border-radius: 12px;
  cursor: pointer;
  transition: 0.2s;
  display: inline-block;
  text-align: center;
}

.modal-button.confirm {
  background-color: #818B7E;
  color: white;
  border: none;
}

.modal-button.cancel {
  background-color: white;
  border: 1px solid #454E42;
  color: #454E42;
}
</style>
