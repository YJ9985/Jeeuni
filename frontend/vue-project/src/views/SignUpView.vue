<template>
  <div class="container">
    <div class="form-wrapper">
      <h1 class="form-title">회원가입</h1>
      <form @submit.prevent="signUp">

        <div class="signup-form">

          <div class="name-row">
            <div class="name-field">
              <label class="form-label" for="first_name">성 <span class="warning-star">*</span></label>
              <input class="form-input first-name-input" type="text" id="first_name" placeholder="성을 입력해 주세요" v-model="first_name">
              <p class="warning" v-if="errors.first_name">{{ errors.first_name }}</p>
            </div>
  
            <div class="name-field">
              <label class="form-label" for="last_name">이름 <span class="warning-star">*</span></label>
              <input class="form-input last-name-input" type="text" id="last_name" placeholder="이름을 입력해 주세요" v-model="last_name">
              <p class="warning" v-if="errors.last_name">{{ errors.last_name }}</p>
            </div>
          </div>
  
          <div class="form-group">
            <label class="form-label" for="birth_date">생년월일 <span class="warning-star">*</span></label>
            <input class="form-input" type="date" id="birth_date" v-model="birth_date" :max="today">
            <p class="warning" v-if="errors.birth_date">{{ errors.birth_date }}</p>
          </div>
  
          <div class="form-group">
            <label class="form-label" for="email">이메일 <span class="warning-star">*</span></label>
            <div class="email-row">
              <input class="form-input email-input" type="text" id="email" placeholder="이메일을 입력해 주세요" v-model="email">
              <button class="verify-button" type="button" @click="verifyEmail" :disabled="isVerified">{{ isVerified ? '완료' : '인증' }}</button>
            </div>
            <p class="warning" v-if="errors.email">{{ errors.email }}</p>
          </div>
  
          <div class="form-group">
            <label class="form-label" for="password1">비밀번호 <span class="warning-star">*</span></label>
            <input class="form-input" type="password" id="password1" placeholder="비밀번호를 입력해 주세요" v-model="password1" @input="validatePassword1">
            <p class="warning" v-if="errors.password1">{{ errors.password1 }}</p>
          </div>
  
          <div class="form-group">
            <label class="form-label" for="password2">비밀번호 확인 <span class="warning-star">*</span></label>
            <input class="form-input" type="password" id="password2" placeholder="비밀번호를 다시 입력해 주세요" v-model="password2" @input="validatePassword2">
            <p class="warning" v-if="errors.password2">{{ errors.password2 }}</p>
          </div>
    
          <div class="button-group">
            <button type="button" @click="cancelSignUp" class="cancel-button">취소</button>
            <input type="submit" value="가입하기" class="green-button">
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
  import { cloneVNode, computed, ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAccountStore } from '@/stores/accounts.js'

  const first_name = ref('')
  const last_name = ref('')
  const birth_date = ref('')
  const email = ref('')
  const password1 = ref('')
  const password2 = ref('')


  const router = useRouter()
  const accountStore = useAccountStore()
  const isVerified = ref(false)

  const today = new Date().toISOString().split('T')[0]
  const errors = ref({
    first_name: '',
    last_name: '',
    birth_date: '',
    email: '',
    password1: '',
    password2: ''
  })

  const validatePassword1 = function () {
    let isValid = true

    errors.value = {
      password1: ''
    }

    const passwordRegex = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*])[a-zA-Z\d!@#$%^&*]{8,12}$/;
    if (!passwordRegex.test(password1.value)) {
      errors.value.password1 = '비밀번호는 영문, 숫자, 특수문자를 포함하여 8~12자로 설정해 주세요'
    } else {
      if (errors.value.password1) {
      errors.value.password1 = ''
      isValid = false
      }
    }

    return isValid
  }

  const validatePassword2 = function () {
    let isValid = true

    errors.value = {
      password2: ''
    }

    const passwordRegex = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*])[a-zA-Z\d!@#$%^&*]{8,12}$/;
    if (!passwordRegex.test(password2.value)) {
      errors.value.password2 = '비밀번호는 영문, 숫자, 특수문자를 포함하여 8~12자로 설정해 주세요'
      isValid = false
    } else if (password1.value !== password2.value) {
      errors.value.password2 = '비밀번호가 일치하지 않습니다'
      isValid = false
    } else {
      if (errors.value.password2) {
        errors.value.password2 = ''
        isValid = true
      }
    }

    return isValid
  }

  const validateForm = () => {
    let isValid = true

    errors.value = {
      first_name: '',
      first_name: '',
      birth_date: '',
      email: '',
      password1: '',
      password2: ''
    }

    if (!first_name.value.trim()) {
      errors.value.first_name = '성을 입력해 주세요'
      isValid = false
    } else if (!/^[a-zA-Z가-힣0-9\s]+$/.test(first_name.value)) {
      errors.value.first_name = '성에 특수기호를 사용할 수 없습니다'
      isValid = false
    }

    if (!last_name.value.trim()) {
      errors.value.last_name = '이름을 입력해 주세요'
      isValid = false
    } else if (!/^[a-zA-Z가-힣0-9\s]+$/.test(last_name.value)) {
      errors.value.last_name = '이름에 특수기호를 사용할 수 없습니다'
      isValid = false
    }

    if (!birth_date.value) {
      errors.value.birth_date = '생년월일을 선택해 주세요'
      isValid = false
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.value)) {
      errors.value.email = '올바른 이메일 형식을 입력해 주세요'
      isValid = false
    }

    const passwordRegex = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*])[a-zA-Z\d!@#$%^&*]{8,12}$/;
    if (!password1.value) {
      errors.value.password1 = '비밀번호를 입력해 주세요'
      isValid = false
    } else if (!passwordRegex.test(password1.value)) {
      errors.value.password1 = '비밀번호는 영문, 숫자, 특수문자를 포함하여 8~12자로 설정해 주세요'
      isValid = false
    }

    if (!password2.value) {
      errors.value.password2 = '비밀번호를 입력해 주세요'
      isValid = false
    } else if (password1.value !== password2.value) {
      errors.value.password2 = '비밀번호가 일치하지 않습니다'
      isValid = false
    } else if (!passwordRegex.test(password2.value)) {
      errors.value.password2 = '비밀번호는 영문, 숫자, 특수문자를 포함하여 8~12자로 설정해 주세요'
      isValid = false
    }

    return isValid
  }

  const signUp = function () {
    if (!validateForm()) {
      return
    }

    const payload = {
      first_name: first_name.value,
      last_name: last_name.value,
      birth_date: birth_date.value,
      email: email.value,
      password: password1.value
    }
    console.log('payload:', payload)

    accountStore.signUp(payload)
    alert('회원가입이 완료되었습니다!')
    router.push('/accounts/login/')
  }

  const cancelSignUp = function () {
    // router.back()     // 뒤로가기
    router.push('/')
    console.log('취소 클릭')
  }

  const verifyEmail = () => {
    console.log('이메일 인증 클릭', email.value)
    isVerified.value = true
  }

  const verifyButtonStyle = computed(() => {
    return {
      backgroundColor: isVerified.value ? '#397203' : '#818B7E',
    }
  })

</script>

<style scoped>
  .container {
    display: flex;
    justify-content: center;
    margin: 0;
    padding: 92px 0;
    min-height: 100vh;
    min-width: 100vw;
    background: linear-gradient(135deg, #f8faf5 0%, #c0cfba 100%);
  }

  .form-wrapper {
    width: 720px;
  }

  .form-title {
    color: #253b20;
    font-size: 40px;
    font-weight: 700;
    text-align: center;
    letter-spacing: 0;
    line-height: 48px;
    white-space: nowrap;
    padding: 32px 0 56px;
  }

  .signup-form {
    background: white;
    border-radius: 16px;
    width: 90;
    padding: 44px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  }

  .form-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 24px;
  }

  .form-label {
    font-size: 16px;
    font-weight: 400;
    margin-bottom: 2%;
  }
  
  .form-input {
    border: 1px solid #d1d5db;
    border-radius: 12px;
    height: 56px;
    font-size: 16px;
    font-weight: 400;
    box-sizing: border-box;
    padding-left: 4%;
    padding-right: 4%;
  }

  .name-row {
    display: flex;
    justify-content: space-between;
    gap: 32px;
    margin-bottom: 24px;
  }

  .name-field {
    display: flex;
    flex-direction: column;
  }

  .first-name-input {
    width: 260px;
  }

  .last-name-input {
    width: 320px;
  }

  .email-row {
    display: flex;
    gap: 20px;
  }

  .email-input {
    flex: 8;
  }

  .verify-button {
    flex: 3;
    border: none;
    border-radius: 40px;
    height: 56px;
    font-size: 16px;
    font-weight: 400;
    background-color: #397203;
    color: white;
  }

  .verify-button:hover:not(:disabled) {
    background: #1b5c07;
    transform: translateY(-1px);
  }

  .verify-button:disabled {
    background: #9ca3af;
    cursor: not-allowed;
    transform: none;
  }

  .button-group {
    display: flex;
    justify-content: space-between;
    margin: 40px 40px 0;
  }

  .green-button {
    color: #FFFFFF;
    background-color: #397203;
    border: none;
    border-radius: 40px;
    height: 56px;
    width: 200px;
    font-size: 16px;
    font-weight: 400;
    box-sizing: border-box;
  }

  .green-button:hover:not(:disabled) {
    background: #1b5c07;
    transform: translateY(-1px);
  }

  .green-button:disabled {
    background: #9ca3af;
    cursor: not-allowed;
    transform: none;
  }

  .cancel-button {
    color: #000;
    background-color: #eeeeee;
    border: none;
    border-radius: 40px;
    height: 56px;
    width: 200px;
    font-size: 16px;
    font-weight: 400;
    box-sizing: border-box;
  }

  .cancel-button:hover {
    background: #e2e2e2;
    transform: translateY(-1px);
  }

  .warning-star {
    color: #ED3437;
    margin-top: 0%;
  }

  .warning {
    color: #ED3437;
    margin-top: 2%;
    margin-left: 2%;
    margin-bottom: 0%;
  }
</style>