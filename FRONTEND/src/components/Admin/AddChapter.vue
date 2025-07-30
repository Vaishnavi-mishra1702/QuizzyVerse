<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card shadow p-4" style="width: 30rem;">
      <h3 class="text-center mb-3 text-primary">Add New Chapter</h3>

      <div v-if="error" class="alert alert-danger text-center">
        {{ error }}
      </div>

      <div v-if="successMessage" class="alert alert-success text-center">
        {{ successMessage }}
      </div>

      <form @submit.prevent="createChapter">
        <div class="mb-3">
          <label for="name" class="form-label">Chapter Name</label>
          <input v-model="formData.name" type="text" class="form-control" id="name" required />
        </div>

        <div class="mb-3">
          <label for="description" class="form-label">Description</label>
          <textarea v-model="formData.description" class="form-control" id="description" rows="3"></textarea>
        </div>

        <div class="d-flex justify-content-between">
          <button type="submit" class="btn btn-success" :disabled="isLoading">
            {{ isLoading ? 'Saving...' : 'Save' }}
          </button>
          <button type="button" @click="cancel" class="btn btn-secondary">
            Cancel
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const subjectId = route.params.subjectId

const formData = ref({
  name: '',
  description: ''
})

const error = ref('')
const successMessage = ref('')
const isLoading = ref(false)

const createChapter = async () => {
  error.value = ''
  successMessage.value = ''
  isLoading.value = true

  try {
    const token = localStorage.getItem('token')
    if (!token) {
      error.value = 'Unauthorized! Please login again.'
      return
    }

   await axios.post(`http://127.0.0.1:5000/api/subjects/${subjectId}/chapters`, formData.value, {
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`
  }
})


    successMessage.value = 'Chapter added successfully!'
    setTimeout(() => {
      router.push('/dashboard')
    }, 900)
  } catch (err) {
    error.value = err.response?.data?.error || 'Something went wrong. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const cancel = () => {
  router.push('/dashboard')
}
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
}
</style>
