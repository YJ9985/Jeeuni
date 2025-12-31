import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import { googleTokenLogin } from "vue3-google-login";
import api from "@/api/axios";   // ← 공통 axios 인스턴스

export const useAccountStore = defineStore("account", () => {
  const router = useRouter();

  const token = ref({
    access: localStorage.getItem("access") || null,
    refresh: localStorage.getItem("refresh") || null,
  });

  /** 공통: 토큰 세팅 + axios 헤더 등록 */
  const setToken = (access, refresh) => {
    token.value.access = access;
    token.value.refresh = refresh;

    localStorage.setItem("access", access);
    localStorage.setItem("refresh", refresh);

    api.defaults.headers.common["Authorization"] = `Bearer ${access}`;
  };

  /** 공통: 토큰 삭제 */
  const clearToken = () => {
    token.value.access = null;
    token.value.refresh = null;
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    delete api.defaults.headers.common["Authorization"];
  };

  /** 앱 시작 시 localStorage → store로 로딩 */
  const loadTokenFromStorage = () => {
    const access = localStorage.getItem("access");
    const refresh = localStorage.getItem("refresh");

    token.value.access = access;
    token.value.refresh = refresh;

    if (access) {
      api.defaults.headers.common["Authorization"] = `Bearer ${access}`;
    }
  };

  /** 회원가입 */
  const signUp = (payload) => {
    const { first_name, last_name, birth_date, email, password } = payload;

    return api
      .post("/accounts/signup/", {
        first_name,
        last_name,
        birth_date,
        email,
        password,
      })
      .then(() => {
        console.log("회원가입 완료");
      })
      .catch((err) => {
        console.log("회원가입 실패:", err.response?.data || err.message);
      });
  };

  /** 로그인 */
  const logIn = (payload) => {
    const { email, password } = payload;

    return api
      .post("/accounts/login/", { email, password })
      .then((res) => {
        setToken(res.data.access, res.data.refresh);
        return { access: res.data.access, refresh: res.data.refresh };
      })
      .catch((err) => {
        console.log("로그인 실패:", err.response?.data || err.message);
      });
  };

  /** 로그아웃 */
  const logout = async () => {
    try {
      const access = token.value.access || localStorage.getItem("access");
      const refresh = token.value.refresh || localStorage.getItem("refresh");

      if (!access || !refresh || typeof access !== "string" || typeof refresh !== "string") {
        throw new Error("access 또는 refresh 토큰이 문자열 형식이 아님");
      }

      await api.post(
        "/accounts/logout/",
        { refresh },
        {
          headers: {
            Authorization: `Bearer ${access}`,
          },
        }
      );

      clearToken();
      router.push({ name: "LogInView" });
    } catch (err) {
      console.error("로그아웃 실패:", err.response?.data || err.message);
    }
  };

  /** 구글 로그인 */
  const googleLogin = async (birth_date = "1999-01-01") => {
    try {
      const { access_token } = await googleTokenLogin();

      const res = await api.post("/accounts/signup/google/", {
        access_token,
        birth_date,
      });

      setToken(res.data.access, res.data.refresh);
      router.push({ name: "mainView" });
    } catch (err) {
      console.error("구글 로그인 실패:", err.response?.data || err.message);
      alert("구글 로그인 중 오류가 발생했습니다.");
    }
  };

  const isLogin = computed(() => !!token.value.refresh);

  return {
    // state
    token,
    isLogin,
    // actions
    signUp,
    logIn,
    logout,
    googleLogin,
    setToken,
    clearToken,
    loadTokenFromStorage,
  };
});
