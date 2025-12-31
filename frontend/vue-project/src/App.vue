<template>
  <header>
    <div class="div-wrapper">
      <div class="inner">
      <router-link to="/" class="logo">JEEUN-I</router-link>
      <div class="nav-links">

      <div class="menu-div">
        <div class="menu-block">
          <router-link to="/books" class="menu-item">도서 목록</router-link>
          <div class="nav-links"></div>
          <span class="divider"></span>
        </div>

        <div class="menu-block">
          <router-link to="/test" class="menu-item">도서 추천</router-link>
          <div class="nav-links"></div>
          <span class="divider"></span>
        </div>

        <div class="menu-block">
          <router-link to="/posts" class="menu-item">포스트 작성</router-link>
          <div class="nav-links"></div>
          <span class="divider"></span>
        </div>

        <div class="menu-block" v-if="!isLogin">
          <router-link to="/accounts/login" class="menu-item">
            로그인
          </router-link>
        </div>
        <div class="menu-block" v-else>
          <button @click="handleLogout" class="menu-item">
            로그아웃
          </button>
        </div>

      </div>
      </div>
      </div>
    </div>
  </header>
  <RouterView />
</template>

<script setup>
  import { computed } from 'vue'
  import { useRouter } from 'vue-router'
  import { RouterView, RouterLink } from 'vue-router'
  import { useAccountStore  } from '@/stores/accounts'

  const router = useRouter()
  const accountStore = useAccountStore()
  const isLogin = computed(() => accountStore.isLogin)

  const handleLogout = async () => {
    try {
      await accountStore.logout()
      router.push({ name: 'LogInView' })
    } catch (e) {
      alert('로그아웃 중 오류가 발생했습니다.')
    }
  }
</script>

<style scoped>
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}

* {
  box-sizing: border-box;
}

.div-wrapper {
  position: fixed; 
  top:0; 
  left:0;
  width:100vw; height:50px;
  background: rgba(255,255,255,0.85);
  box-shadow: 0 6px 10px rgba(0,0,0,0.1);
  z-index: 999;
}

.inner {
  max-width: 1920px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  margin-left: 48px;
  font-family: "Rozha One", Helvetica, sans-serif;
  font-size: 32px;
  color: #818B7E;
  text-decoration: none;
}

.menu-div {
  margin-right: 24px;
  display: flex;
  align-items: center;
}


.menu-block {
  display: flex;
  align-items: center;
}

.menu-item {
  background: none;
  border: none;
  outline: none;

  display: inline-flex;
  align-items: center;
  justify-content: center;

  padding: 0 26px;
  color: #454E42;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
  transform-origin: center;
  text-decoration: none;
}

.menu-item:hover {
  transform: scale(1.05);
}

.divider {
  height: 24px;
  width: 1px;
  background-color: #818B7E;
  margin-right: 0;
  pointer-events: none;
}
</style>