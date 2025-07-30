<template>
  <div class="container my-5">
    <h2 class="text-primary">Welcome {{ user.name }}</h2>

    <h4 class="mt-4">📅 Upcoming Quiz</h4>

    <div v-if="quizzes.length" class="row mt-3 g-4">
      <div v-for="(quiz, index) in quizzes" :key="index + '-' + quiz.id" class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title">Quiz #{{ quiz.id }}</h5>
            <p class="card-text"><strong>Subject:</strong> {{ quiz.subject }}</p>
            <p class="card-text"><strong>Chapter:</strong> {{ quiz.chapter }}</p>
            <p class="card-text"><strong>Duration:</strong> {{ quiz.duration }} minutes</p>
            <p class="card-text"><strong>Date:</strong> {{ formatDate(quiz.date) }}</p>
            <div class="d-flex justify-content-end gap-2">
              <button class="btn btn-primary" @click="startQuiz(quiz.id)">Start</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="mt-4">No upcoming quizzes found.</div>

    <!-- 🔽 CSV Download Section -->
    <div class="mt-5">
      <h4>📥 Download Your Quiz Report</h4>
      <button
        class="btn btn-primary"
        :disabled="!user.id"
        @click="exportUserCsv">
        📥 Export My Quiz CSV
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      user: {},
      quizzes: []
    }
  },

  async mounted() {
    await this.fetchUserInfo()
    this.fetchUpcomingQuizzes()
  },

  methods: {
    async fetchUserInfo() {
      try {
        const token = localStorage.getItem('token')
        const headers = { Authorization: `Bearer ${token}` }

        const res = await axios.get('http://127.0.0.1:5000/api/user/info', { headers })
        this.user = res.data
      } catch (err) {
        console.error("Error fetching user info:", err)
      }
    },

    async fetchUpcomingQuizzes() {
      try {
        const token = localStorage.getItem('token')
        const headers = { Authorization: `Bearer ${token}` }

        const res = await axios.get('http://127.0.0.1:5000/api/user/upcoming-quizzes', { headers })
        this.quizzes = res.data
      } catch (err) {
        console.error("Error fetching quizzes:", err)
      }
    },

    startQuiz(id) {
      this.$router.push(`/quiz/start/${id}`)
    },

    formatDate(dateStr) {
      const date = new Date(dateStr)
      return date.toLocaleDateString('en-IN', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
      })
    },

    async exportUserCsv() {
      if (!this.user.id) return

      try {
        const res = await axios.get(`http://127.0.0.1:5000/api/export/user_csv/${this.user.id}`)
        const taskId = res?.data?.task_id

        if (taskId) {
          // Wait 3 seconds and try download without checking status
          setTimeout(() => {
            const filename = `user_csv_${this.user.id}.csv`
            const fileUrl = `http://127.0.0.1:5000/static/${filename}`

            const link = document.createElement('a')
            link.href = fileUrl
            link.setAttribute('download', filename)
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)
          }, 3000)
        }
      } catch (err) {
        console.error("CSV export error:", err)
      }
    }
  }
}
</script>

<style scoped>
.card {
  border-radius: 10px;
}
.card-title {
  font-weight: bold;
}
</style>
