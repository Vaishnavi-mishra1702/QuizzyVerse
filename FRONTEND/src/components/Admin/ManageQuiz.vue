<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card shadow p-4" style="width: 30rem;">
      <h3 class="text-center mb-3 text-primary">Edit Quiz</h3>

      <div v-if="error" class="alert alert-danger text-center">
        {{ error }}
      </div>

      <div v-if="successMessage" class="alert alert-success text-center">
        {{ successMessage }}
      </div>

      <form @submit.prevent="updateQuiz" v-if="!loading">
        <div class="mb-3">
          <label for="date" class="form-label">Date of Quiz</label>
          <input
              v-model="formData.date_of_quiz"
              type="date"
              class="form-control"
              :min="minDate"
              required
            />

        </div>

       <div class="mb-3">
        <label for="time_duration" class="form-label">Time Duration (in minutes)</label>
        <input
          v-model="formData.time_duration"
          type="number"
          min="1"
          class="form-control"
          required
        />
      </div>

        <div class="mb-3">
          <label for="remarks" class="form-label">Remarks</label>
          <textarea
            v-model="formData.remarks"
            class="form-control"
            id="remarks"
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
          <button type="button" @click="deleteQuiz" class="btn btn-danger w-100">
            🗑️ Delete Quiz
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
const quizId = route.params.quizId

const formData = ref({
  date_of_quiz: '',
  time_duration: '',
  remarks: ''
})

const error = ref('')
const successMessage = ref('')
const isLoading = ref(false)
const loading = ref(true)

const fetchQuiz = async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    error.value = 'Unauthorized! Please login again.'
    return
  }

  try {
    const response = await axios.get(`http://127.0.0.1:5000/api/quizzes/${quizId}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    // ✅ Setting values from backend to form
    formData.value = {
      date_of_quiz: response.data.date_of_quiz,
      time_duration: response.data.time_duration,
      remarks: response.data.remarks || ''
    }
  } catch (err) {
    error.value = 'Failed to load quiz.'
  } finally {
    loading.value = false
  }
}

const updateQuiz = async () => {
  error.value = ''
  successMessage.value = ''
  isLoading.value = true

  const token = localStorage.getItem('token')
  if (!token) {
    error.value = 'Unauthorized! Please login again.'
    return
  }

  try {
    await axios.put(`http://127.0.0.1:5000/api/quizzes/${quizId}`, formData.value, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      }
    })

    successMessage.value = 'Quiz updated successfully!'
    setTimeout(() => router.push('/quiz'), 600)
  } catch (err) {
    error.value = 'Error updating quiz.'
  } finally {
    isLoading.value = false
  }
}

const deleteQuiz = async () => {
  if (!confirm('Are you sure you want to delete this quiz?')) return

  const token = localStorage.getItem('token')
  if (!token) {
    error.value = 'Unauthorized! Please login again.'
    return
  }

  try {
    await axios.delete(`http://127.0.0.1:5000/api/quizzes/${quizId}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    alert('Quiz deleted successfully!')
    router.push('/quiz')
  } catch (err) {
    error.value = 'Error deleting quiz.'
  }
}

const cancel = () => {
  router.push('/quiz')
}

onMounted(fetchQuiz)
const minDate = ref('')

onMounted(() => {
  const today = new Date()
  const yyyy = today.getFullYear()
  const mm = String(today.getMonth() + 1).padStart(2, '0')
  const dd = String(today.getDate()).padStart(2, '0')
  minDate.value = `${yyyy}-${mm}-${dd}`
})

</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
}
</style>
