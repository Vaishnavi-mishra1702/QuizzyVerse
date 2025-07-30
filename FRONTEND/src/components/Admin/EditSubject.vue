<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card shadow p-4" style="width: 30rem;">
      <h3 class="text-center mb-3 text-primary">Edit Subject</h3>

      <div v-if="error" class="alert alert-danger text-center">
        {{ error }}
      </div>

      <div v-if="successMessage" class="alert alert-success text-center">
        {{ successMessage }}
      </div>

      <form @submit.prevent="updateSubject" v-if="!loading">
        <div class="mb-3">
          <label for="name" class="form-label">Subject Name</label>
          <input
            v-model="formData.name"
            type="text"
            class="form-control"
            id="name"
            required
          />
        </div>

        <div class="mb-3">
          <label for="description" class="form-label">Description</label>
          <textarea
            v-model="formData.description"
            class="form-control"
            id="description"
            rows="3"
          ></textarea>
        </div>

        <div class="d-flex justify-content-between">
          <button type="submit" class="btn btn-primary" :disabled="isLoading">
            {{ isLoading ? 'Updating...' : 'Update' }}
          </button>
          <button type="button" @click="cancel" class="btn btn-secondary">
            Cancel
          </button>
        </div>

        <div class="mt-3 text-center">
          <button type="button" @click="deleteSubject" class="btn btn-danger w-100">
            🗑️ Delete Subject
          </button>
        </div>
      </form>

      <div v-else class="text-center">
        <div class="spinner-border text-primary" role="status"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const subjectId = route.params.subjectId

const formData = ref({
  name: '',
  description: ''
})

const error = ref('')
const successMessage = ref('')
const isLoading = ref(false)
const loading = ref(true)

const fetchSubject = async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    error.value = 'Unauthorized! Please login again.'
    return
  }

  try {
    const response = await axios.get(`http://127.0.0.1:5000/api/subjects/${subjectId}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    formData.value = {
      name: response.data.name,
      description: response.data.description
    }
  } catch (err) {
    error.value = 'Failed to load subject.'
  } finally {
    loading.value = false
  }
}

const updateSubject = async () => {
  error.value = ''
  successMessage.value = ''
  isLoading.value = true

  const token = localStorage.getItem('token')
  if (!token) {
    error.value = 'Unauthorized! Please login again.'
    return
  }

  try {
    await axios.put(`http://127.0.0.1:5000/api/subjects/${subjectId}`, formData.value, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      }
    })

    successMessage.value = 'Subject updated successfully!'
    setTimeout(() => router.push('/dashboard'), 1500)
  } catch (err) {
    error.value = 'Error updating subject.'
  } finally {
    isLoading.value = false
  }
}

const deleteSubject = async () => {
  if (!confirm('Are you sure you want to delete this subject?')) return

  const token = localStorage.getItem('token')
  if (!token) {
    error.value = 'Unauthorized! Please login again.'
    return
  }

  try {
    await axios.delete(`http://127.0.0.1:5000/api/subjects/${subjectId}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    alert('Subject deleted successfully!')
    router.push('/dashboard')
  } catch (err) {
    error.value = 'Error deleting subject.'
  }
}

const cancel = () => {
  router.push('/dashboard')
}

onMounted(fetchSubject)
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
}
</style>
