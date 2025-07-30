<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card shadow p-4" style="width: 24rem;">
      <h3 class="text-center mb-3">Register for QuizzyVerse</h3>

      <div v-if="error" class="alert alert-danger text-center">
        {{ error }}
      </div>

      <form @submit.prevent="registerUser">
        <div class="mb-3">
          <label for="full_name" class="form-label">Full Name</label>
          <input v-model="formData.full_name" type="text" class="form-control" id="full_name" required />
        </div>

        <div class="mb-3">
          <label for="email" class="form-label">Email address</label>
          <input v-model="formData.email" type="email" class="form-control" id="email" required />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input v-model="formData.password" type="password" class="form-control" id="password" required />
        </div>

        <div class="mb-3">
          <label for="qualification" class="form-label">Qualification</label>
          <input v-model="formData.qualification" type="text" class="form-control" id="qualification" required />
        </div>

        <div class="mb-3">
          <label for="dob" class="form-label">Date of Birth</label>
          <input v-model="formData.dob" type="date" class="form-control" id="dob" required />
        </div>

        <button type="submit" class="btn btn-success w-100" :disabled="isLoading">
          {{ isLoading ? 'Registering...' : 'Register' }}
        </button>
      </form>

      <div class="text-center mt-3">
        Already have an account?
        <router-link to="/login">Login</router-link>
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
  password: '',
  full_name: '',
  qualification: '',
  dob: '',
  role: 'user'
})

const error = ref('')
const isLoading = ref(false)

const registerUser = async () => {
  error.value = ''
  isLoading.value = true

  try {
    // Clone formData and format dob
    const payload = { ...formData.value }
    payload.dob = new Date(payload.dob).toISOString().split('T')[0]

    await axios.post(
      'http://127.0.0.1:5000/api/register',
      JSON.stringify(payload),
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )
    router.push('/login')
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
