<template>
  <div class="container">
    <div class="full-wrapper">
      <h1 class="form-title">JEEUN-I</h1>
      <form @submit.prevent="logIn">
        <div class="form-group">
          <input class="form-input" type="text" id="email" placeholder="아이디(이메일)" v-model.trim="email">
        </div>

        <div class="form-group">
          <input class="form-input" type="password" id="password" placeholder="비밀번호" v-model.trim="password">
        </div>
  
        <input class="login-button" type="submit" value="로그인">
      </form>
      
      <div class="help-wrapper">
        <div class="help-link">
          <RouterLink :to="{ name: 'SignUpView'}">이메일 찾기</RouterLink>
        </div>
        <span class="divider">|</span>
        <div class="help-link">
          <RouterLink :to="{ name: 'SignUpView'}">비밀번호 찾기</RouterLink>
        </div>
        <span class="divider">|</span>
        <div class="help-link">
          <RouterLink :to="{ name: 'SignUpView'}">회원가입</RouterLink>
        </div>
      </div>

      <div>
        <p class="social-login">간편 로그인</p>

        <div class="button-group">
          <div class="google-button" @click="googleLogin"> 
            <img class="google-icon" src="@/assets/google-logo.png" alt="Google">
          </div>
          <div class="kakao-button" @click="kakaoLogin"> 
            <img class="kakao-icon" src="@/assets/kakao-logo.png" alt="Kakao">
          </div>
        </div>
      </div>

      <Teleport to="body">
      <div v-if="showModal">
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
              <button class="modal-button confirm" @click="submitBirthDate">가입하기</button>
          </div>
        </div>
      </div>
      </Teleport>
    </div>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import { useRouter, RouterLink } from 'vue-router'
  import { useAccountStore } from '@/stores/accounts.js'
  import { googleTokenLogin } from 'vue3-google-login'
  import axios from 'axios'
  
  const router = useRouter()
  const accountStore = useAccountStore()
  const API_BASE = import.meta.env.VITE_API_BASE_URL
  
  const email = ref('')
  const password = ref('')
  const birthDate = ref('1999-01-01')
  const accessToken = ref('')
  const showModal = ref(false)

  const cancelModal = () => {
    showModal.value = false

    localStorage.removeItem('access')
    localStorage.removeItem('refresh')

    accountStore.setToken(null, null)

    router.push({ name: 'LogInView' })
  }



  // 일반로그인
  // const logIn = function () {
  //   const payload = {
  //     email: email.value,
  //     password: password.value
  //   }

  //   accountStore.logIn(payload)
  // }

  const logIn = async () => {
    try {
      const { access, refresh } = await accountStore.logIn({ email: email.value, password: password.value })
      // accountStore.logIn 안에서 setToken을 해 주고 있다면,
      // 여기서는 router.push만 해 주시면 됩니다.
      router.replace({ name: 'HomeView' })
    } catch (err) {
      alert('로그인 실패')
    }
  }

  async function googleLogin() {
    try {
      // 1) 구글 토큰 획득
      const { access_token } = await googleTokenLogin()
      accessToken.value = access_token

      // 2) 백엔드에 access_token만 전송 → 가입 여부 판단
      const res = await axios.post(
        `${API_BASE}/accounts/signup/google/`,
        { access_token: access_token }
      )

      // 3) 백엔드 응답 분기
      if (res.data.status === 'logged_in') {
        // 기존 유저 로그인 처리
        accountStore.setToken(res.data.access, res.data.refresh)
        localStorage.setItem('access', res.data.access)
        localStorage.setItem('refresh', res.data.refresh)
        // console.log('구글 로그인 완료')
        router.replace({ name: 'HomeView' })

      } else if (res.data.status === 'need_birth_date') {
        // 회원가입 진행을 위해 생년월일 모달 띄우기
        accessToken.value = access_token
        showModal.value = true

      } else {
        alert('알 수 없는 상태입니다.')
      }

    } catch (err) {
      console.error('Google login failed:', err.response?.data || err)
      
    if (err.type === 'popup_closed') {
      return
    }
      alert(err.response?.data?.detail || '구글 로그인 중 오류가 발생했습니다.')
    }
  }


  // 카카오 설정
  const KAKAO_CLIENT_ID = import.meta.env.VITE_APP_KAKAO_CLIENT_ID
  const REDIRECT_URI = `${window.location.origin}/accounts/kakao/login/callback`

  function kakaoLogin() {
    if (!KAKAO_CLIENT_ID) {
    alert('카카오 클라이언트 ID가 설정되지 않았습니다.')
    return
    }
  
    const kakaoAuthUrl = `https://kauth.kakao.com/oauth/authorize?client_id=${KAKAO_CLIENT_ID}&redirect_uri=${encodeURIComponent(REDIRECT_URI)}&response_type=code&prompt=login`
    window.location.href = kakaoAuthUrl
  }

  const submitBirthDate = async () => {
    showModal.value = false

    try {
      const updateRes = await axios.post(
        `${API_BASE}/accounts/profile/update/`,
        {
          access_token: accessToken.value,
          birth_date: birthDate.value
        }
      )

      localStorage.setItem('access', updateRes.data.access)
      localStorage.setItem('refresh', updateRes.data.refresh)
      accountStore.setToken(updateRes.data.access, updateRes.data.refresh)

      console.log('회원가입 완료')
      router.replace({ name: 'HomeView' })

    } catch(err){
      console.log(err)
      alert(
        err.response?.data.detail || '프로필 업데이트 중 오류가 발생했습니다.'
      )
    }
  }
</script>

<style>
  body {
    margin: 0;
    padding: 0;
    min-height: 100vh;
    background: linear-gradient(135deg, #f8faf5 0%, #c0cfba 100%);
    background-attachment: fixed;
  }
</style>

<style scoped>
  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0;
    min-height: 100vh;
    min-width: 100vw;
  }

  .full-wrapper {
    width: 516px;
    position: absolute;
    top: 16%;
  }

  .form-title {
    color: #818B7E;
    font-family: "Rozha One", sans-serif;
    font-size: 56px;
    font-weight: 700;
    text-align: center;
    letter-spacing: 0;
    line-height: 48px;
    white-space: nowrap;
    margin-bottom: 16%;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 28px;
  }
  
  .form-input {
    border: 1px solid #818B7E;
    border-radius: 12px;
    height: 56px;
    font-size: 16px;
    font-weight: 400;
    box-sizing: border-box;
    padding-left: 4%;
    padding-right: 4%;
  }

  .login-button {
    color: #FFFFFF;
    background-color: #818B7E;
    border: none;
    border-radius: 40px;
    height: 56px;
    width: 220px;
    font-size: 16px;
    font-weight: 400;
    box-sizing: border-box;
    display: block;
    margin: 0 auto;
    margin-top: 40px;
  }

  .help-wrapper {
    margin-top: 60px;
    text-align: center;
    display: flex;
    justify-content: space-between;
  }

  .help-link {
    flex: 1;
    text-align: center;
    color:#818B7E;
  }

  .help-link a {
    text-decoration: none;
    color: inherit;        
    font-weight: 200;
  }

  .help-link a:hover {
    font-weight: 500;
  }

  .divider {
    color: #818B7E;
    margin: 0 12px;
  }

  .social-login {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    margin-top: 40px;
    margin-bottom: 40px;
  }

  .social-login::before, .social-login::after {
    content: "";
    flex-grow: 1;
    height: 1px;
    background-color: #818B7E;
    margin: 0 24px;
  }

.button-group {
  display: flex;
  justify-content: center;
  gap: 8%;
  margin-top: 6%;
  margin-bottom: 6%;
}

.google-button {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background-color: #FFFFFF;
  border: 1px solid #EFEFEF;
  display: flex;
  justify-content: center;
  align-items: center;
}

.google-icon {
  width: 24px;
  height: 24px;
}

.kakao-button {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background-color: #FEE500;
  border: 1px solid #EFEFEF;
  display: flex;
  justify-content: center;
  align-items: center;
}

.kakao-icon {
  border-radius: 50%;
  width: 56px;
  height: 56px;
}

/* 모달 CSS 시작!!! */

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
  margin-bottom: 4%;
}

.modal-label{
  font-size: 14px;
  color: #454E42;
  text-align: left;
  margin-bottom: 1%;
}

.modal-input{
  border: 1px solid #454E42;
  width: 100%;
  height: 32%;
  padding: 0 12px;
  border-radius: 12px;
  font-size: 14px;
  color: #454E42;
  box-sizing: border-box;
  margin-bottom: 4%;
}

.modal-button-group{
  display: flex;
  justify-content: center;
  gap: 32px;
  margin-top: 4%;
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