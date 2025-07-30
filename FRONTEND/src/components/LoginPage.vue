
<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card shadow p-4" style="width: 24rem;">
      <h3 class="text-center mb-3">Welcome to QuizzyVerse</h3>

      <div v-if="error" class="alert alert-danger text-center">
        {{ error }}
      </div>

      <form @submit.prevent="loginUser">
        <div class="mb-3">
          <label for="email" class="form-label">Email address</label>
          <input
            v-model="formData.email"
            type="email"
            class="form-control"
            id="email"
            required
          />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            v-model="formData.password"
            type="password"
            class="form-control"
            id="password"
            required
          />
        </div>

        <button
          type="submit"
          class="btn btn-primary w-100"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Logging in...' : 'Login' }}
        </button>
      </form>

      <div class="text-center mt-3">
        Are you a new user?
        <router-link to="/register">Register</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const formData = ref({
  email: '',
  password: ''
})

const error = ref('')
const isLoading = ref(false)

const loginUser = async () => {
  error.value = ''
  isLoading.value = true

  try {
    const response = await axios.post(
      'http://127.0.0.1:5000/api/login',
      JSON.stringify(formData.value),
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )

    const token = response.data.access_token
    const role = response.data.role

    localStorage.setItem('token', token)
    localStorage.setItem('userType', role) 
     if (role === 'admin') {
      router.push('/dashboard')
    } else if (role === 'user') {
      router.push('/userdashboard')
    } else {
      error.value = 'Unknown role. Please contact support.'
    }
  } catch (err) {
    if (err.response && err.response.data && err.response.data.message) {
      error.value = err.response.data.message
    } else {
      error.value = 'Something went wrong. Please try again.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>
<style scoped>
body {
  font-family: Arial, sans-serif;
}
</style>